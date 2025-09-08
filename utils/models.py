from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request model for analysis operations."""

    repo_url: str = Field(..., description="GitHub URL or local path to repository")
    branch: str = Field("main", description="Branch to analyze")
    max_files: int = Field(1000, description="Maximum number of files to process")
    ignore_tests: bool = Field(True, description="Whether to ignore test files")
    include_patterns: Optional[List[str]] = Field(
        None, description="File patterns to include"
    )
    exclude_patterns: Optional[List[str]] = Field(
        None, description="File patterns to exclude"
    )
    use_cache: bool = Field(True, description="Whether to use cached results")
    enhance_with_ai: bool = Field(
        True, description="Whether to enhance with AI insights"
    )


class EnhancementRequest(BaseModel):
    """Request model for AI enhancement."""

    model: str = Field(
        "deepseek-coder:6.7b", description="AI model to use for enhancement"
    )
    include_architecture: bool = Field(
        True, description="Include architecture analysis"
    )
    include_issues: bool = Field(True, description="Include potential issues")
    include_recommendations: bool = Field(True, description="Include recommendations")


class AnalysisResult(BaseModel):
    """Result model for analysis operations."""

    status: str = Field(..., description="Analysis status")
    repository: Dict[str, str] = Field(..., description="Repository information")
    structure: Dict[str, Any] = Field(..., description="Code structure analysis")
    summary: Optional[Dict[str, Any]] = Field(None, description="AI-enhanced summary")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Analysis metadata"
    )
    error: Optional[str] = Field(None, description="Error message if analysis failed")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "repository": {
                    "url": "https://github.com/example/repo",
                    "branch": "main",
                },
                "structure": {
                    "file_count": 150,
                    "language_breakdown": {"Python": 120, "JavaScript": 30},
                    "directory_tree": {"src": {"main.py": {}, "utils": {}}},
                },
                "summary": {
                    "architecture": "Microservices architecture with...",
                    "key_components": ["API Gateway", "User Service"],
                    "issues": ["Missing tests for User Service"],
                    "recommendations": ["Add integration tests", "Update dependencies"],
                },
                "metadata": {"analysis_time": 45.2, "files_processed": 150},
            }
        }
