# Code Context Analyzer (CCA) MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with comprehensive codebase analysis and context. This tool helps AI understand large codebases by analyzing repository structure, generating insights, and providing enhanced context through AI-powered analysis.

## Features

- **Multi-level Analysis**: Full repository, directory-specific, and overview analysis modes
- **AI Enhancement**: Integrates with Ollama for intelligent codebase insights
- **Progress Reporting**: Real-time progress updates during analysis
- **Smart Caching**: Configurable caching for improved performance on repeated requests
- **Flexible Filtering**: Include/exclude patterns for targeted analysis
- **Error Resilience**: Comprehensive error handling with fallback mechanisms

## Installation

### Prerequisites

- Python 3.13
- Ollama (for AI enhancement features)
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ahasanular/cca-mcp
cd code-context-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
Alternatively using `UV`
```bash
uv pip install -r pyproject.toml
```

3.Install and configure Ollama (optional for AI enhancement):
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the desired model
ollama pull deepseek-coder:6.7b
```

### Configuration
Configure the server using environment variables:
```bash
cp .env.template .env
```

### Usage
Starting the Server
```bash
python main.py
```
The server will start on `127.0.0.1:8000` by default.

### Available Tools
1. **analyze_repository:**
Comprehensive analysis of a complete repository with project tree and class and function level explanation with doc-string and all.
2. **analyze_directory:**
Same like `analyze_repository` but with focused analysis of a specific directory within the repository.
3. **get_repository_overview:**
Quick high-level overview of a repository.`in-progress`
4. **clear_cache:**
Clear cached analysis results.

### Progress Reporting
The server provides real-time progress updates during analysis:

1. **Initialization** (0-10%): Starting analysis and checking cache
2. **Repository Cloning** (10-30%): Cloning the repository
3. **Code Analysis** (30-70%): Analyzing code structure and patterns
4. **AI Enhancement** (70-90%): Enhancing with AI insights (if enabled)
5. **Caching** (90-100%): Storing results in cache and finalizing

### Caching
The server implements a configurable caching system with the following features:

- **Time-based expiration**: Results are cached for 1 hour by default
- **Size limits**: Maximum of 100 cached items by default
- **Selective clearing**: Clear cache for specific repositories or all repositories
- **Configurable**: Cache settings can be customized via environment variables

### Project Structure
```markdown
project/
├── main.py                # Server entry point and tool definitions
├── utils/
│   ├── analyzer.py        # Custom analysis logic
│   ├── enhancer.py        # AI enhancement functionality
│   ├── formatter.py       # Custom output formatting
│   ├── cache.py           # Caching mechanism
│   ├── settings.py        # Configuration management
│   └── models.py          # Data models
└── requirements.txt       # Dependencies
```

### Adding New Tools
1. Define the tool in `main.py` with the `@mcp.tool()` decorator
2. Add appropriate progress reporting using `ctx.report_progress()`
3. Implement error handling and caching as needed
4. Update this `README` with documentation for the new tool

### License
MIT License - see LICENSE file for details.

### Contributing
Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Support
For support or questions, please open an issue in the GitHub repository or contact the development team.