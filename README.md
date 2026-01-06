# Mathematics MCP Server 🧮

A Model Context Protocol (MCP) server that provides mathematical operations as tools for AI assistants like Claude. This server enables Claude to perform accurate arithmetic calculations through a standardized interface.

## 📋 Table of Contents

- [What is Mathematics MCP Server?](#what-is-mathematics-mcp-server)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Integration with Claude Desktop](#integration-with-claude-desktop)
- [Available Tools](#available-tools)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## 🎯 What is Mathematics MCP Server?

Mathematics MCP Server is a lightweight server that exposes mathematical operations through the Model Context Protocol (MCP). It allows AI assistants to perform precise calculations by calling dedicated tools rather than relying on their internal reasoning capabilities.

### Why Use This?

- **Accuracy**: Ensures precise mathematical calculations
- **Reliability**: Eliminates calculation errors that can occur with AI reasoning
- **Extensibility**: Easy to add new mathematical operations
- **Logging**: All operations are logged for debugging and audit purposes

## ✨ Features

- **8 Mathematical Operations**: Addition, subtraction, multiplication, division, modulus, power, square, and square root
- **Error Handling**: Robust error handling for edge cases (division by zero, negative square roots, etc.)
- **Comprehensive Logging**: All operations logged to both file and stderr
- **Type Safety**: Built with Pydantic models for input validation
- **MCP Compliant**: Fully compatible with the Model Context Protocol standard

## 🔧 How It Works
```
┌─────────────────┐
│  Claude Desktop │
└────────┬────────┘
         │
         │ JSON-RPC over stdio
         │
┌────────▼────────┐
│   FastMCP       │
│   Mathematics   │
│   MCP Server    │
└────────┬────────┘
         │
         │ Python Functions
         │
┌────────▼────────┐
│  Math Operations│
│  (add, subtract,│
│   multiply...)  │
└─────────────────┘
```

1. **Claude** sends a tool call request via JSON-RPC
2. **FastMCP** receives and validates the request
3. **Python functions** perform the calculation
4. **Result** is returned to Claude in structured format
5. **Logging** records the operation for debugging

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/mathematics-mcp.git
cd mathematics-mcp
```

### Step 2: Install uv (if not already installed)
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### Step 3: Install Dependencies

The project uses `pyproject.toml` for dependency management:
```bash
# Install all dependencies (uv automatically reads pyproject.toml)
uv sync

# Or using pip
pip install -e .
```

Alternatively, you can install dependencies directly:
```bash
uv pip install fastmcp pydantic
```

### Step 4: Test the Server

Using the MCP Inspector (recommended for development):
```bash
# This opens an interactive web interface to test your MCP server
uv run fastmcp dev main.py
```

Or run the server directly:
```bash
# This runs the server in production mode
uv run fastmcp run main.py
```

You should see:
```
Starting Mathematics MCP Server...
```

## 🚀 Usage

### Testing with MCP Inspector (Recommended)

The MCP Inspector provides a web-based interface to test your server:
```bash
uv run fastmcp dev main.py
```

This will:
1. Start the MCP server
2. Open a web interface in your browser
3. Allow you to test all tools interactively
4. Show request/response details in real-time

### Running the Server in Production Mode
```bash
uv run fastmcp run main.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Using with Claude Desktop

See the [Integration with Claude Desktop](#integration-with-claude-desktop) section below.

## 🖥️ Integration with Claude Desktop

### Quick Installation (Recommended)

The easiest way to integrate with Claude Desktop is using the FastMCP installer:
```bash
uv run fastmcp install claude-desktop main.py
```

This command will:
- Automatically locate your Claude Desktop configuration file
- Add the Mathematics MCP server configuration
- Use the correct paths for your system
- Restart Claude Desktop if needed

### Manual Installation (Alternative)

If you prefer to configure manually or the automatic installation doesn't work:

#### Step 1: Locate Claude Desktop Configuration

The configuration file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Update Configuration

Open the configuration file and add the Mathematics MCP server:
```json
{
  "mcpServers": {
    "mathematics": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mathematics-mcp",
        "run",
        "fastmcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/mathematics-mcp` with the actual path to your project directory.

**Example for macOS/Linux**:
```json
{
  "mcpServers": {
    "mathematics": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourusername/projects/mathematics-mcp",
        "run",
        "fastmcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Example for Windows**:
```json
{
  "mcpServers": {
    "mathematics": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourUsername\\projects\\mathematics-mcp",
        "run",
        "fastmcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Step 3: Restart Claude Desktop

1. Quit Claude Desktop completely (Cmd+Q on Mac, Alt+F4 on Windows)
2. Relaunch Claude Desktop
3. Look for the 🔌 icon in the bottom right indicating MCP servers are connected
4. Click the icon to see "mathematics" server listed

### Step 4: Verify Installation

In Claude, try asking:
- "What's 12345 + 67890?"
- "Calculate the square root of 144"
- "What's 25 to the power of 3?"

Claude should use the Mathematics MCP tools to provide accurate answers.

### Troubleshooting Installation

If the automatic installation fails:
```bash
# Check if uv is installed correctly
uv --version

# Verify the server works
uv run fastmcp dev main.py

# Try manual configuration following the steps above
```

## 🛠️ Available Tools

### 1. Addition (`add`)
```python
Input: {"a": 10, "b": 5}
Output: {"status": "success", "operation": "add", "result": 15}
```

### 2. Subtraction (`subtract`)
```python
Input: {"a": 10, "b": 5}
Output: {"status": "success", "operation": "subtract", "result": 5}
```

### 3. Multiplication (`multiply`)
```python
Input: {"a": 10, "b": 5}
Output: {"status": "success", "operation": "multiply", "result": 50}
```

### 4. Division (`divide`)
```python
Input: {"a": 10, "b": 5}
Output: {"status": "success", "operation": "divide", "result": 2.0}
```
*Note: Throws error on division by zero*

### 5. Modulus (`modulus`)
```python
Input: {"a": 10, "b": 3}
Output: {"status": "success", "operation": "modulus", "result": 1}
```
*Note: Throws error on modulus by zero*

### 6. Power (`power`)
```python
Input: {"base": 2, "exponent": 8}
Output: {"status": "success", "operation": "power", "result": 256}
```

### 7. Square (`square`)
```python
Input: {"a": 5}
Output: {"status": "success", "operation": "square", "result": 25}
```

### 8. Square Root (`sqrt`)
```python
Input: {"a": 144}
Output: {"status": "success", "operation": "sqrt", "result": 12.0}
```
*Note: Throws error on negative numbers*

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Log output from `math_mcp.log`

### Suggesting Features

1. Open an issue describing the feature
2. Explain the use case
3. Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch:
```bash
   git checkout -b feature/amazing-feature
```
3. Make your changes
4. Add tests if applicable
5. Commit with clear messages:
```bash
   git commit -m "Add: New trigonometric functions"
```
6. Push to your fork:
```bash
   git push origin feature/amazing-feature
```
7. Open a Pull Request

## 🐛 Troubleshooting

### Server Not Appearing in Claude Desktop

**Problem**: MCP server doesn't show up in Claude Desktop

**Solutions**:
1. Check the configuration file path is correct
2. Verify JSON syntax in `claude_desktop_config.json`
3. Ensure absolute paths are used (not relative paths)
4. Restart Claude Desktop completely
5. Check `math_mcp.log` for startup errors

### "Unexpected non-whitespace character after JSON" Error

**Problem**: Claude Desktop shows JSON parsing errors

**Solutions**:
1. Ensure logging is NOT writing to `sys.stdout`
2. Use `sys.stderr` or file logging only
3. Remove any `print()` statements from the code

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'fastmcp'`

**Solutions**:
1. Activate your virtual environment
2. Install dependencies: `pip install fastmcp pydantic`
3. If using venv, point to venv Python in config

### Permission Errors

**Problem**: Cannot write to log file

**Solutions**:
1. Check write permissions on the directory
2. Use a different log location:
```python
   LOG_FILE = Path.home() / "math_mcp.log"
```

### Testing Connection

To test if the server is working:
```bash
# Run the server
python main.py

# In another terminal, send a test message (requires jq)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python main.py
```

**Star ⭐ this repo if you find it helpful!**