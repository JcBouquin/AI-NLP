# Copyright 2024
#
# Licensed under the Apache License, Version 2.0 (the "License

");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import sqlite3
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Optional, Sequence, cast

from parlant.adapters.db.json_file import JSONFileDocumentDatabase
from parlant.adapters.db.transient import TransientDocumentDatabase
from parlant.adapters.nlp.openai_service import OpenAIService
from parlant.core.common import DefaultBaseModel, Version, generate_id
from parlant.core.contextual_correlator import ContextualCorrelator
from parlant.core.loggers import FileLogger, Logger, LogLevel, StdoutLogger
from parlant.core.nlp.generation import GenerationInfo
from parlant.core.nlp.service import NLPService
from parlant.core.persistence.common import ObjectId
from parlant.core.persistence.document_database import BaseDocument, DocumentDatabase
from typing_extensions import Self


@dataclass(frozen=True)
class TableSchema:
    """Represents a database table schema"""
    id: str
    name: str
    description: str
    columns: dict[str, str]  # column_name: type
    example_queries: list[str]
    security_rules: list[str]


class _TableSchemaDocument(BaseDocument):
    name: str
    description: str
    columns: dict[str, str]
    example_queries: list[str]
    security_rules: list[str]


class _SQLQuerySchema(DefaultBaseModel):
    """Schema for structured SQL query generation"""
    user_question: str
    question_analysis: str
    
    # Identification des tables/colonnes pertinentes
    relevant_tables: list[str]
    relevant_columns: dict[str, list[str]]
    
    # Raisonnement
    query_strategy: str
    potential_joins: list[str]
    filters_needed: list[str]
    aggregations_needed: list[str]
    
    # Génération SQL
    sql_query_draft: str
    security_check_passed: bool
    security_issues_found: Optional[str] = None
    sql_query_final: str
    
    # Explication
    query_explanation_french: str
    expected_result_description: str
    
    # Métadonnées
    confidence: Literal["high", "medium", "low"]
    requires_human_approval: bool
    estimated_row_count: Optional[str] = None


@dataclass(frozen=True)
class SQLQueryResult:
    """Result of a SQL query execution"""
    query: str
    data: list[dict[str, Any]]
    explanation: str
    confidence: str
    row_count: int
    approved: bool
    generation_info: GenerationInfo


QueryStatus: type[Literal["success", "error", "blocked"]]


class App:
    VERSION = Version.String("0.1.0")

    def __init__(
        self,
        database: DocumentDatabase,
        service: NLPService,
        logger: Logger,
        db_path: Optional[str] = None,
    ):
        self._db = database
        self._service = service
        self.logger = logger
        self._db_path = db_path or ":memory:"
        
        self._schemas: dict[str, TableSchema] = {}
        
    async def identity_loader(self, doc: BaseDocument) -> _TableSchemaDocument:
        return cast(_TableSchemaDocument, doc)

    async def __aenter__(self, *args: Any, **kwargs: Any) -> Self:
        self._collection = await self._db.get_or_create_collection(
            "table_schemas",
            schema=_TableSchemaDocument,
            document_loader=self.identity_loader,
        )

        self._generator = await self._service.get_schematic_generator(_SQLQuerySchema)

        # Charger les schémas existants
        persisted_schemas = await self._collection.find({})

        for s in persisted_schemas:
            assert "id" in s

            self._schemas[s["id"]] = TableSchema(
                id=s["id"],
                name=s["name"],
                description=s["description"],
                columns=s["columns"],
                example_queries=s["example_queries"],
                security_rules=s["security_rules"],
            )

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool:
        return False

    async def execute_natural_language_query(
        self, question: str
    ) -> SQLQueryResult:
        """Convert natural language question to SQL and execute it"""
        
        self.logger.info(
            f'Processing natural language query: "{question}" with {len(self._schemas)} schema(s)'
        )
        
        schema_context = self._format_schema_context()

        prompt = f"""\
You are an expert SQL agent for a medical database system.

Your job is to analyze natural language questions and generate SAFE, ACCURATE SQL queries.

CRITICAL SECURITY RULES:
- ONLY SELECT queries are allowed (no INSERT, UPDATE, DELETE, DROP, ALTER, CREATE)
- Always use LIMIT 100 to prevent overwhelming results
- Never expose highly sensitive data (passwords, social security numbers, credit cards)
- Parameterized queries are preferred to prevent SQL injection
- If a query seems dangerous or inappropriate, set requires_human_approval=true

QUERY GENERATION PROCESS:
1. Analyze what the user is asking
2. Identify which tables and columns are needed
3. Determine if JOINs are required
4. Identify necessary WHERE filters
5. Check if aggregations (COUNT, SUM, AVG) are needed
6. Generate a draft SQL query
7. Perform security validation
8. Produce the final SQL query
9. Explain the query in simple French

Database Schema Information: ###
{schema_context}
###

Few-Shot Examples: ###
Example 1:
Question: "Combien de rendez-vous avons-nous aujourd'hui ?"
SQL: SELECT COUNT(*) as total FROM appointments WHERE DATE(appointment_date) = DATE('now');
Explanation: Je compte tous les rendez-vous dont la date est aujourd'hui.

Example 2:
Question: "Liste les patients du Dr. Martin"
SQL: SELECT p.first_name, p.last_name, p.email 
     FROM patients p 
     JOIN appointments a ON p.id = a.patient_id 
     JOIN doctors d ON a.doctor_id = d.id 
     WHERE d.last_name = 'Martin' 
     GROUP BY p.id 
     LIMIT 100;
Explanation: Je joins les tables patients, appointments et doctors pour trouver tous les patients qui ont eu des rendez-vous avec le Dr. Martin.

Example 3:
Question: "Quel est le médecin le plus sollicité ?"
SQL: SELECT d.first_name, d.last_name, COUNT(a.id) as appointment_count 
     FROM doctors d 
     LEFT JOIN appointments a ON d.id = a.doctor_id 
     GROUP BY d.id 
     ORDER BY appointment_count DESC 
     LIMIT 1;
Explanation: Je compte le nombre de rendez-vous par médecin et je trie par ordre décroissant pour trouver celui qui en a le plus.
###

User Question: ###
{question}
###

Generate a complete JSON response following the schema provided.
"""

        result = await self._generator.generate(
            prompt,
            hints={
                "strict": True,
                "temperature": 0.1,
            },
        )

        self.logger.debug(result.content.model_dump_json(indent=2))

        # Vérification de sécurité supplémentaire
        sql_upper = result.content.sql_query_final.upper()
        dangerous_keywords = [
            "DELETE", "DROP", "UPDATE", "INSERT", "ALTER",
            "CREATE", "TRUNCATE", "EXEC", "EXECUTE"
        ]
        
        has_dangerous = any(kw in sql_upper for kw in dangerous_keywords)
        
        if has_dangerous or not result.content.security_check_passed:
            self.logger.warning(
                f"Dangerous SQL query blocked: {result.content.sql_query_final}"
            )
            return SQLQueryResult(
                query=result.content.sql_query_final,
                data=[],
                explanation="⛔ Requête refusée pour raisons de sécurité. Seules les requêtes SELECT sont autorisées.",
                confidence="low",
                row_count=0,
                approved=False,
                generation_info=result.info,
            )

        # Vérifier si nécessite approbation humaine
        if result.content.requires_human_approval:
            self.logger.info("Query requires human approval")
            return SQLQueryResult(
                query=result.content.sql_query_final,
                data=[],
                explanation=f"⏳ Cette requête nécessite une validation humaine.\n\nRequête générée: {result.content.sql_query_final}\n\nRaison: {result.content.query_explanation_french}",
                confidence=result.content.confidence,
                row_count=0,
                approved=False,
                generation_info=result.info,
            )

        # Exécuter la requête
        try:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(result.content.sql_query_final)
            rows = cursor.fetchall()
            
            data = [dict(row) for row in rows]
            row_count = len(data)
            
            conn.close()
            
            self.logger.info(
                f'Query executed successfully: "{result.content.sql_query_final}" ({row_count} rows)'
            )
            
            return SQLQueryResult(
                query=result.content.sql_query_final,
                data=data,
                explanation=result.content.query_explanation_french,
                confidence=result.content.confidence,
                row_count=row_count,
                approved=True,
                generation_info=result.info,
            )
            
        except sqlite3.Error as e:
            self.logger.error(f"SQL execution error: {e}")
            return SQLQueryResult(
                query=result.content.sql_query_final,
                data=[],
                explanation=f"❌ Erreur lors de l'exécution de la requête: {str(e)}",
                confidence="low",
                row_count=0,
                approved=False,
                generation_info=result.info,
            )

    def _format_schema_context(self) -> str:
        """Format table schemas as context for the LLM"""
        if not self._schemas:
            return "NO SCHEMA INFORMATION AVAILABLE"

        return "\n\n".join([
            f"""\
Table: {schema.name}
Description: {schema.description}

Columns:
{self._format_columns(schema.columns)}

Example Queries:
{self._format_examples(schema.example_queries)}

Security Rules:
{self._format_rules(schema.security_rules)}
"""
            for schema in self._schemas.values()
        ])

    def _format_columns(self, columns: dict[str, str]) -> str:
        return "\n".join([f"  - {name} ({dtype})" for name, dtype in columns.items()])

    def _format_examples(self, examples: list[str]) -> str:
        return "\n".join([f"  {i+1}. {ex}" for i, ex in enumerate(examples)])

    def _format_rules(self, rules: list[str]) -> str:
        return "\n".join([f"  - {rule}" for rule in rules])

    async def create_schema(
        self,
        name: str,
        description: str,
        columns: dict[str, str],
        example_queries: list[str],
        security_rules: list[str],
    ) -> TableSchema:
        """Add a new table schema to the knowledge base"""
        new_id = generate_id()

        await self._collection.insert_one(
            _TableSchemaDocument(
                id=ObjectId(new_id),
                version=self.VERSION,
                name=name,
                description=description,
                columns=columns,
                example_queries=example_queries,
                security_rules=security_rules,
            )
        )

        schema = TableSchema(
            id=new_id,
            name=name,
            description=description,
            columns=columns,
            example_queries=example_queries,
            security_rules=security_rules,
        )

        self._schemas[schema.id] = schema
        
        self.logger.info(f'Schema added: {name}')

        return schema

    async def list_schemas(self) -> Sequence[TableSchema]:
        """List all registered table schemas"""
        return list(self._schemas.values())

    async def delete_schema(self, schema_id: str) -> bool:
        """Delete a table schema"""
        if schema_id in self._schemas:
            del self._schemas[schema_id]
            await self._collection.delete_one({"id": {"$eq": schema_id}})
            self.logger.info(f'Schema deleted: {schema_id}')
            return True
        return False


@asynccontextmanager
async def create_persistent_app(
    service: NLPService | None = None,
    db_path: str | None = None,
) -> AsyncIterator[App]:
    """Create a persistent SQL agent app with file-based storage"""
    correlator = ContextualCorrelator()
    logger = FileLogger(
        Path("parlant-sql.log"),
        correlator,
        log_level=LogLevel.DEBUG,
        logger_id="parlant-sql",
    )

    if not service:
        service = OpenAIService(logger)

    async with JSONFileDocumentDatabase(
        logger=logger,
        file_path=Path("parlant-sql-db.json"),
    ) as db:
        with correlator.scope("parlant-sql"):
            async with App(db, service, logger, db_path) as app:
                logger.info("Initialized Parlant SQL Agent")
                yield app


@asynccontextmanager
async def create_transient_app(
    db_path: str | None = None
) -> AsyncIterator[App]:
    """Create a transient SQL agent app (no persistence)"""
    correlator = ContextualCorrelator()
    logger = StdoutLogger(correlator, logger_id="parlant-sql")
    service = OpenAIService(logger)

    with correlator.scope("parlant-sql"):
        async with App(TransientDocumentDatabase(), service, logger, db_path) as app:
            yield app

