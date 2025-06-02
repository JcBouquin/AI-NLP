
"""
MCP ChatBot - Asynchronous Research Assistant
============================================

This script implements a sophisticated asynchronous MCP (Model Context Protocol) client 
that connects to multiple research servers and provides an interactive chat interface 
with Claude AI.

Key Architectural Components:
- Asynchronous multi-server connection management
- Dynamic tool discovery from connected MCP servers
- Bidirectional communication with Claude via Anthropic API
- Proper resource lifecycle management with automatic cleanup

The async nature is essential because:
1. Network I/O operations (MCP server connections) are non-blocking
2. Multiple concurrent connections can be maintained efficiently
3. User interaction doesn't block server communication
4. Graceful shutdown ensures all resources are properly released
"""


from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio

load_dotenv()

class ToolDefinition(TypedDict):
    """
    Type definition for MCP tool schemas.
    
    This TypedDict ensures consistent structure for tool definitions
    received from MCP servers, providing type safety and IDE support.
    """
    name: str
    description: str
    input_schema: dict

class MCP_ChatBot:
    """
    Asynchronous MCP ChatBot that orchestrates communication between
    Claude AI and multiple MCP research servers.
    
    This class manages:
    - Multiple concurrent MCP server connections
    - Tool discovery and mapping across servers
    - Interactive conversation loop with Claude
    - Proper async resource management and cleanup
    """

    def __init__(self):
        """
        Initialize the MCP ChatBot with async-ready components.
        
        Key async components:
        - sessions: List of active MCP connections (each is async)
        - exit_stack: Manages async context cleanup automatically
        - tool_to_session: Maps tool names to their originating async sessions
        """
        self.sessions: List[ClientSession] = []  
        self.exit_stack = AsyncExitStack()  
        self.anthropic = Anthropic()
        self.available_tools: List[ToolDefinition] = []  
        self.tool_to_session: Dict[str, ClientSession] = {}  


    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        """
        Establish asynchronous connection to a single MCP server.
        
        This async method performs several I/O operations:
        1. Creates stdio transport (launches external server process)
        2. Establishes bidirectional async communication session
        3. Performs async handshake and initialization
        4. Discovers available tools via async API call
        5. Updates internal tool registry
        
        Args:
            server_name: Human-readable server identifier (e.g., "research")
            server_config: Configuration dict with command and args for server startup
            
        Async Flow:
        - Uses 'await' for all I/O operations to prevent blocking
        - Registers with exit_stack for automatic cleanup
        - Handles connection failures gracefully without crashing
        """
        """Connect to a single MCP server."""
        try:
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )  
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )  
            await session.initialize()
            self.sessions.append(session)
            
            # List available tools for this session
            response = await session.list_tools()
            tools = response.tools
            print(f"\nConnected to {server_name} with tools:", [t.name for t in tools])
            
            for tool in tools:  
                self.tool_to_session[tool.name] = session
                self.available_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
        except Exception as e:
            print(f"Failed to connect to {server_name}: {e}")

    async def connect_to_servers(self):  
        """
        Connect to all configured MCP servers asynchronously.
        
        This method:
        1. Reads server configuration from JSON file
        2. Iterates through configured servers
        3. Establishes async connections to each server concurrently
        
        Async Benefits:
        - Multiple servers can be connected to simultaneously
        - File I/O is non-blocking
        - Failed connections don't block successful ones
        """
         
        try:
            with open("server_config.json", "r") as file:
                data = json.load(file)
            
            servers = data.get("mcpServers", {})
            
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            raise
    
    async def process_query(self, query):
        """
        Process a user query through Claude with potential MCP tool usage.
        
        This is the core async orchestration method that:
        1. Sends query to Claude with available tool catalog
        2. Processes Claude's response (text or tool calls)
        3. Routes tool calls to appropriate MCP servers asynchronously
        4. Returns results to Claude for final response formulation
        
        Async Flow:
        - Claude API calls are awaited (network I/O)
        - MCP tool calls are awaited (inter-process communication)
        - Multiple tool calls could be made in sequence
        - Conversation continues until Claude provides final text response
        
        Args:
            query: User's question or request
        """
        messages = [{'role':'user', 'content':query}]
        response = self.anthropic.messages.create(max_tokens = 2024,
                                      model = 'claude-3-7-sonnet-20250219', 
                                      tools = self.available_tools,
                                      messages = messages)
        process_query = True
        while process_query:
            assistant_content = []
            for content in response.content:
                if content.type =='text':
                    print(content.text)
                    assistant_content.append(content)
                    if(len(response.content) == 1):
                        process_query= False
                elif content.type == 'tool_use':
                    assistant_content.append(content)
                    messages.append({'role':'assistant', 'content':assistant_content})
                    tool_id = content.id
                    tool_args = content.input
                    tool_name = content.name
                    
    
                    print(f"Calling tool {tool_name} with args {tool_args}")
                    
                    # Call a tool
                    session = self.tool_to_session[tool_name] 
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    messages.append({"role": "user", 
                                      "content": [
                                          {
                                              "type": "tool_result",
                                              "tool_use_id":tool_id,
                                              "content": result.content
                                          }
                                      ]
                                    })
                    response = self.anthropic.messages.create(max_tokens = 2024,
                                      model = 'claude-3-7-sonnet-20250219', 
                                      tools = self.available_tools,
                                      messages = messages) 
                    
                    if(len(response.content) == 1 and response.content[0].type == "text"):
                        print(response.content[0].text)
                        process_query= False

    
    
    async def chat_loop(self):
        """
        Run the interactive chat interface.
        
        This async method provides the main user interaction loop:
        - Prompts user for input
        - Processes queries through Claude and MCP servers
        - Handles errors gracefully
        - Continues until user types 'quit'
        
        Async Benefits:
        - User input doesn't block other operations
        - Query processing can involve multiple async operations
        - Error handling doesn't crash the entire loop
        """
        """Run an interactive chat loop"""
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
        
                if query.lower() == 'quit':
                    break
                    
                await self.process_query(query)
                print("\n")
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):  
        """
        Cleanly close all async resources.
        
        This method ensures that:
        - All MCP server connections are properly closed
        - Subprocess handles are cleaned up
        - No resource leaks occur
        
        The AsyncExitStack automatically calls __aexit__ on all
        registered async context managers in reverse order.
        """
        await self.exit_stack.aclose()


async def main():
    """
    Main async entry point for the MCP ChatBot.
    
    This function orchestrates the complete lifecycle:
    1. Creates chatbot instance
    2. Connects to all configured MCP servers
    3. Runs interactive chat loop
    4. Ensures cleanup occurs even if errors happen
    
    The try/finally pattern ensures proper cleanup regardless
    of how the program terminates (normal exit, Ctrl+C, error).
    """
    chatbot = MCP_ChatBot()
    try:
        
        await chatbot.connect_to_servers()  
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()  


if __name__ == "__main__":
    """
    Program entry point - launches the async event loop.
    
    asyncio.run() creates an event loop, runs the main coroutine,
    and properly cleans up the event loop when done.
    
    This is the standard pattern for async Python applications.
    """
    asyncio.run(main())
