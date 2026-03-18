import json
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from logger import get_logger
from config import MCP_CONFIG_PATH

logger = get_logger("mcp")

class MCPManager:
    def __init__(self):
        self.config_path = MCP_CONFIG_PATH
        self.servers = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f).get("mcpServers", {})
        except Exception as e:
            logger.error(f"Error loading MCP config: {e}")
            return {}

    async def list_tools(self):
        """Lists available tools from all configured servers."""
        all_tools = []
        for name, config in self.servers.items():
            try:
                # Basic info from config
                all_tools.append({
                    "server": name,
                    "command": f"{config.get('command')} {' '.join(config.get('args', []))}",
                    "description": f"MCP Tool from {name}"
                })
            except Exception as e:
                logger.error(f"Error listing MCP tool for {name}: {e}")
        return all_tools

    async def call_tool(self, server_name, tool_name, arguments):
        """Executes an MCP tool and returns the result."""
        config = self.servers.get(server_name)
        if not config:
            return f"ERROR: MCP server {server_name} not found."

        server_params = StdioServerParameters(
            command=config.get("command"),
            args=config.get("args", []),
            env={**os.environ, **config.get("env", {})}
        )

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments)
                    return result.content
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name} on {server_name}: {e}")
            return f"ERROR: {str(e)}"

mcp_manager = MCPManager()
