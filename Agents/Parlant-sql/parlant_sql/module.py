# Copyright 2024
#
# Licensed under the Apache License, Version 2.0 (the "License");
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

"""Parlant module for SQL query tool"""

from typing import Any

from parlant.core.services.tools.service_registry import ServicePlugin, ToolContext, ToolResult
from parlant.core.loggers import Logger

from .app import create_persistent_app


class SqlQueryPlugin(ServicePlugin):
    """Plugin for SQL query functionality"""
    
    def __init__(self, logger: Logger, db_path: str | None = None):
        self._logger = logger
        self._db_path = db_path or "medical_database.db"
        self._app = None
        
    async def initialize(self) -> None:
        """Initialize the SQL query service"""
        self._logger.info("Initializing Parlant SQL Query Plugin...")
        # L'app sera créé à la demande pour éviter les problèmes de contexte
        
    async def cleanup(self) -> None:
        """Cleanup resources"""
        self._logger.info("Cleaning up Parlant SQL Query Plugin...")
        if self._app:
            await self._app.__aexit__(None, None, None)
    
    def get_tool_schemas(self) -> dict[str, Any]:
        """Return tool schemas for Parlant"""
        return {
            "sql_query": {
                "name": "sql_query",
                "description": "Query the medical database using natural language. "
                              "Converts natural language questions into SQL queries and returns the results. "
                              "Use this for questions about appointments, patients, doctors, statistics, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The natural language question to convert to SQL"
                        }
                    },
                    "required": ["question"]
                }
            }
        }
    
    async def execute_tool(
        self,
        tool_name: str,
        context: ToolContext,
        **kwargs: Any
    ) -> ToolResult:
        """Execute a tool"""
        if tool_name != "sql_query":
            return ToolResult(
                success=False,
                error=f"Unknown tool: {tool_name}"
            )
        
        question = kwargs.get("question")
        if not question:
            return ToolResult(
                success=False,
                error="Missing required parameter: question"
            )
        
        # Créer l'app si nécessaire
        if not self._app:
            from .app import create_persistent_app
            self._app_context = create_persistent_app(db_path=self._db_path)
            self._app = await self._app_context.__aenter__()
        
        try:
            result = await self._app.execute_natural_language_query(question)
            
            if not result.approved:
                return ToolResult(
                    success=False,
                    data={
                        "query": result.query,
                        "explanation": result.explanation,
                        "reason": "Query was blocked or requires approval"
                    }
                )
            
            # Formater les résultats pour l'agent
            formatted_response = self._format_results(result)
            
            return ToolResult(
                success=True,
                data={
                    "answer": formatted_response,
                    "query": result.query,
                    "row_count": result.row_count,
                    "confidence": result.confidence
                }
            )
            
        except Exception as e:
            self._logger.error(f"Error executing SQL query: {e}")
            return ToolResult(
                success=False,
                error=str(e)
            )
    
    def _format_results(self, result) -> str:
        """Format query results for natural language response"""
        if result.row_count == 0:
            return f"{result.explanation}\n\nAucun résultat trouvé."
        
        response = f"{result.explanation}\n\n"
        
        if result.row_count == 1:
            # Résultat unique - format simple
            row = result.data[0]
            if len(row) == 1:
                # Une seule valeur (COUNT, SUM, etc.)
                value = list(row.values())[0]
                response += f"Résultat: **{value}**"
            else:
                # Plusieurs colonnes
                for key, value in row.items():
                    response += f"- {key}: {value}\n"
        elif result.row_count <= 10:
            # Plusieurs résultats (< 10) - liste formatée
            response += f"**{result.row_count} résultat(s):**\n\n"
            for i, row in enumerate(result.data, 1):
                response += f"{i}. "
                response += ", ".join([f"{k}: {v}" for k, v in row.items()])
                response += "\n"
        else:
            # Beaucoup de résultats - résumé
            response += f"**{result.row_count} résultats trouvés.**\n\n"
            response += "Premiers résultats:\n"
            for i, row in enumerate(result.data[:5], 1):
                response += f"{i}. "
                response += ", ".join([f"{k}: {v}" for k, v in row.items()])
                response += "\n"
            response += f"\n... et {result.row_count - 5} autres résultats."
        
        return response.strip()


# Point d'entrée pour Parlant
async def create_plugin(logger: Logger, **config: Any) -> SqlQueryPlugin:
    """Factory function to create the plugin"""
    db_path = config.get("db_path", "medical_database.db")
    plugin = SqlQueryPlugin(logger, db_path)
    await plugin.initialize()
    return plugin

