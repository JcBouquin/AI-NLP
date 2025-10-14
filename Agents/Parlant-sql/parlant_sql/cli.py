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

"""Command-line interface for Parlant SQL"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import click

from .app import create_persistent_app


@click.group()
def cli():
    """Parlant SQL - Text-to-SQL tool for Parlant agents"""
    pass


@cli.command()
@click.option(
    "--name",
    "-n",
    required=True,
    help="Name of the database table"
)
@click.option(
    "--description",
    "-d",
    required=True,
    help="Description of what this table contains"
)
@click.option(
    "--columns",
    "-c",
    required=True,
    multiple=True,
    help="Column definition in format 'name:type' (can be specified multiple times)"
)
@click.option(
    "--example",
    "-e",
    multiple=True,
    help="Example SQL query (can be specified multiple times)"
)
@click.option(
    "--rule",
    "-r",
    multiple=True,
    help="Security rule (can be specified multiple times)"
)
def add_schema(
    name: str,
    description: str,
    columns: tuple[str, ...],
    example: tuple[str, ...],
    rule: tuple[str, ...],
):
    """Add a new table schema to the knowledge base"""
    
    # Parse columns
    parsed_columns = {}
    for col in columns:
        if ":" not in col:
            click.echo(f"Error: Column must be in format 'name:type', got: {col}", err=True)
            sys.exit(1)
        col_name, col_type = col.split(":", 1)
        parsed_columns[col_name.strip()] = col_type.strip()
    
    async def _add():
        async with create_persistent_app() as app:
            schema = await app.create_schema(
                name=name,
                description=description,
                columns=parsed_columns,
                example_queries=list(example) if example else [],
                security_rules=list(rule) if rule else [],
            )
            click.echo(f"✅ Schema added: {schema.name} (ID: {schema.id})")
    
    asyncio.run(_add())


@cli.command()
def list_schemas():
    """List all registered table schemas"""
    
    async def _list():
        async with create_persistent_app() as app:
            schemas = await app.list_schemas()
            
            if not schemas:
                click.echo("No schemas registered yet.")
                return
            
            click.echo(f"\n📊 {len(schemas)} schema(s) registered:\n")
            for schema in schemas:
                click.echo(f"Table: {schema.name}")
                click.echo(f"  ID: {schema.id}")
                click.echo(f"  Description: {schema.description}")
                click.echo(f"  Columns: {len(schema.columns)}")
                click.echo(f"  Examples: {len(schema.example_queries)}")
                click.echo(f"  Rules: {len(schema.security_rules)}")
                click.echo()
    
    asyncio.run(_list())


@cli.command()
@click.argument("schema_id")
def delete_schema(schema_id: str):
    """Delete a table schema by ID"""
    
    async def _delete():
        async with create_persistent_app() as app:
            success = await app.delete_schema(schema_id)
            if success:
                click.echo(f"✅ Schema deleted: {schema_id}")
            else:
                click.echo(f"❌ Schema not found: {schema_id}", err=True)
                sys.exit(1)
    
    asyncio.run(_delete())


@cli.command()
@click.option(
    "--question",
    "-q",
    required=True,
    help="Natural language question to query the database"
)
@click.option(
    "--db-path",
    "-db",
    default="medical_database.db",
    help="Path to the SQLite database file"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format"
)
def query(question: str, db_path: str, format: str):
    """Execute a natural language query"""
    
    async def _query():
        async with create_persistent_app(db_path=db_path) as app:
            result = await app.execute_natural_language_query(question)
            
            if format == "json":
                output = {
                    "query": result.query,
                    "data": result.data,
                    "explanation": result.explanation,
                    "confidence": result.confidence,
                    "row_count": result.row_count,
                    "approved": result.approved,
                }
                click.echo(json.dumps(output, indent=2, ensure_ascii=False))
            else:
                click.echo(f"\n📊 Question: {question}\n")
                click.echo(f"🔍 SQL Generated:\n{result.query}\n")
                click.echo(f"💡 Explanation:\n{result.explanation}\n")
                
                if not result.approved:
                    click.echo("⛔ Query was not executed (security or approval required)")
                    return
                
                click.echo(f"✅ Results ({result.row_count} row(s)):")
                if result.data:
                    for i, row in enumerate(result.data[:10], 1):
                        click.echo(f"  {i}. {dict(row)}")
                    if result.row_count > 10:
                        click.echo(f"  ... and {result.row_count - 10} more")
                else:
                    click.echo("  (no results)")
                
                click.echo(f"\n🎯 Confidence: {result.confidence}")
    
    asyncio.run(_query())


@cli.command()
@click.option(
    "--db-path",
    "-db",
    default="medical_database.db",
    help="Path to the SQLite database file"
)
def interactive(db_path: str):
    """Start an interactive SQL query session"""
    
    click.echo("🤖 Parlant SQL Interactive Mode")
    click.echo("Type 'quit' or 'exit' to end the session\n")
    
    async def _session():
        async with create_persistent_app(db_path=db_path) as app:
            while True:
                try:
                    question = click.prompt("Question", type=str)
                    
                    if question.lower() in ["quit", "exit", "q"]:
                        click.echo("Goodbye! 👋")
                        break
                    
                    result = await app.execute_natural_language_query(question)
                    
                    click.echo(f"\n🔍 SQL: {result.query}")
                    click.echo(f"💡 {result.explanation}")
                    
                    if result.approved and result.data:
                        click.echo(f"✅ {result.row_count} result(s):")
                        for i, row in enumerate(result.data[:5], 1):
                            click.echo(f"  {i}. {dict(row)}")
                        if result.row_count > 5:
                            click.echo(f"  ... and {result.row_count - 5} more")
                    elif not result.approved:
                        click.echo("⛔ Query blocked")
                    else:
                        click.echo("(no results)")
                    
                    click.echo()
                    
                except (KeyboardInterrupt, EOFError):
                    click.echo("\nGoodbye! 👋")
                    break
                except Exception as e:
                    click.echo(f"❌ Error: {e}", err=True)
    
    asyncio.run(_session())


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()

