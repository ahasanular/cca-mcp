"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from typing import List, Dict, Any, Optional
import logging
from mcp.server.fastmcp import FastMCP
from code_context_analyzer.repo_system import RepositorySession
from utils.analyzer import CustomAnalyzer
from utils.enhancher import AIEnhancer


logging.basicConfig(level=logging.INFO)


# Create an MCP server
mcp = FastMCP(name="First MCP", host="0.0.0.0", port=8080)


@mcp.tool()
def cca(
    repo_url: str, branch: str = "main", max_file: int = 1000, ignore_tests: bool = True
) -> Dict[str, Any]:
    """CCA(Code Context Analyzer) is a tool to discover, analyze, summarize and show formatted files from local or github repository codebase."""
    with RepositorySession(repo_url, branch) as session:
        analyzer = CustomAnalyzer(
            session.path, max_files=max_file, ignore_tests=ignore_tests
        )
        result = analyzer.run_analysis()
        enhancer = AIEnhancer(model="deepseek-coder:6.7b")
        result = enhancer.enhance(result)

    return {"content": result}


if __name__ == "__main__":
    transport = "stdio"
    print(f"Running FastMCP server with transport ({transport}) on port 8080.")
    mcp.run(transport=transport)
