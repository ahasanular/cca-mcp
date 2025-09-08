import asyncio
import functools
import logging
import os
import time
from enum import Enum
from typing import Any, Dict, List, Optional

from code_context_analyzer.repo_system import RepositorySession
from mcp.server.fastmcp import Context, FastMCP

from utils.analyzer import CustomAnalyzer
from utils.cache import AnalysisCache
from utils.enhancer import AIEnhancer
from utils.settings import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP(
    name="Code Context Analyzer (CCA)",
    host=DEFAULT_CONFIG["server_host"],
    port=DEFAULT_CONFIG["server_port"],
)

# Initialize cache
cache = AnalysisCache()


class AnalysisType(Enum):
    FULL_REPO = "full_repository"
    DIRECTORY = "directory"
    FILE = "file"


@mcp.tool()
async def analyze_repository(
    repo_url: str,
    branch: str = "main",
    max_files: int = 1000,
    ignore_tests: bool = True,
    ignore_patterns: List[str] = [],
    use_cache: bool = True,
    enhance_with_ai: bool = True,
    model: str = DEFAULT_CONFIG["model"],
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Analyze a complete repository to provide structured context for AI assistants.

    -param repo_url: GitHub URL or local path to repository
    -param branch: Branch to analyze (default: "main")
    -param max_files: Maximum number of files to process
    -param ignore_tests: Whether to ignore test files
    -param include_patterns: File patterns to include in analysis
    -param exclude_patterns: File patterns to exclude from analysis
    -param use_cache: Whether to use cached results if available
    -param enhance_with_ai: Whether to enhance with AI insights
    -param model: AI model to use for enhancement

    -return: Structured analysis results with repository context
    """
    await ctx.report_progress(0, 100, "Starting repository analysis")

    try:
        # Check cache first
        cache_key = f"{repo_url}:{branch}:{max_files}"
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                await ctx.report_progress(100, 100, "Returning cached results")
                return cached_result

        await ctx.report_progress(10, 100, "Cloning repository")
        with RepositorySession(repo_url, branch) as session:
            await ctx.report_progress(30, 100, "Analyzing code structure")

            analyzer = CustomAnalyzer(
                session.path,
                max_files=max_files,
                ignore_tests=ignore_tests,
                ignore=ignore_patterns,
            )

            # Run analysis in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, analyzer.run_analysis)

            if enhance_with_ai:
                await ctx.report_progress(70, 100, "Enhancing with AI insights")
                enhancer = AIEnhancer(model=model)
                enhanced_result = await enhancer.enhance(result)
                result["ai_enhancement"] = enhanced_result

            # Cache the result
            await ctx.report_progress(90, 100, "Caching results")
            cache.set(cache_key, result)

            await ctx.report_progress(100, 100, "Analysis complete")
            return result

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        await ctx.report_progress(100, 100, f"Error: {str(e)}")
        return {"error": str(e), "repo_url": repo_url}


@mcp.tool()
async def analyze_directory(
    repo_url: str,
    directory_path: str,
    branch: str = "main",
    max_depth: int = 3,
    ignore_patterns: Optional[List[str]] = None,
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Analyze a specific directory within a repository.

    -param repo_url: GitHub URL or local path to repository
    -param directory_path: Path to directory within repository
    -param branch: Branch to analyze (default: "main")
    -param max_depth: Maximum depth to traverse in directory
    -param include_patterns: File patterns to include in analysis
    -param exclude_patterns: File patterns to exclude from analysis
    -return: Structured analysis results for the specific directory
    """

    try:
        await ctx.report_progress(
            0, 100, f"Starting directory analysis: {directory_path}"
        )
        with RepositorySession(repo_url, branch) as session:
            await ctx.report_progress(30, 100, "Analyzing directory structure")

            tg_path = os.path.join(session.path, directory_path)
            await ctx.report_progress(40, 100, f"Analyzing directory >> {tg_path}")
            analyzer = CustomAnalyzer(
                tg_path,
                max_files=500,  # Lower limit for directory analysis
                ignore_tests=True,
                ignore=ignore_patterns,
                # target_path=directory_path,
                # max_depth=max_depth
            )
            loop = asyncio.get_event_loop()

            result = await loop.run_in_executor(None, analyzer.run_analysis)

            await ctx.report_progress(100, 100, "Directory analysis complete")
            return result

    except Exception as e:
        logger.error(f"Directory analysis failed: {str(e)}")
        await ctx.report_progress(100, 100, f"Error: {str(e)}")
        return {"error": str(e), "repo_url": repo_url, "directory": directory_path}


@mcp.tool()
async def get_repository_overview(
    repo_url: str,
    branch: str = "main",
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Get a high-level overview of a repository without detailed analysis.

    -param repo_url: GitHub URL or local path to repository
    -param branch: Branch to analyze (default: "main")
    -return: High-level repository overview
    """
    await ctx.report_progress(0, 100, "Starting repository analysis")

    try:
        await ctx.report_progress(20, 100, "Cloning repository")
        with RepositorySession(repo_url, branch) as session:
            await ctx.report_progress(50, 100, "Generating overview")

            analyzer = CustomAnalyzer(session.path, max_files=100)
            overview = await asyncio.get_event_loop().run_in_executor(
                None, analyzer.generate_overview
            )

            await ctx.report_progress(100, 100, "Overview complete")
            return overview

    except Exception as e:
        logger.error(f"Overview generation failed: {str(e)}")
        await ctx.report_progress(100, 100, f"Error: {str(e)}")
        return {"error": str(e), "repo_url": repo_url}


@mcp.tool()
async def clear_cache(
    repo_url: Optional[str] = None,
    ctx: Context = None,
) -> Dict[str, Any]:
    """
    Clear cached analysis results.
    -param repo_url: GitHub URL or local path to repository
    -return: Cache analysis results
    """
    try:
        if repo_url:
            await ctx.report_progress(0, 100, f"Clearing cache for {repo_url}")
            cache.clear_repository(repo_url)
            await ctx.report_progress(100, 100, "Cache cleared")
            return {"status": "success", "message": f"Cache cleared for {repo_url}"}
        else:
            await ctx.report_progress(0, 100, "Clearing all cache")
            cache.clear_all()
            await ctx.report_progress(100, 100, "All cache cleared")
            return {"status": "success", "message": "All cache cleared"}
    except Exception as e:
        await ctx.report_progress(100, 100, f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    transport = DEFAULT_CONFIG["transport"]
    mcp.run(transport=transport)
