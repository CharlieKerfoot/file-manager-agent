# File Manager Agent

A powerful CLI-based AI agent that helps you manage your files and directories using natural language commands. Built with Google's Gemini API and Python.

## Features

- **Natural Language Interface**: Interact with your file system using plain English.
- **File Operations**: Read, write, create, delete, rename, and move files and directories.
- **Search Capabilities**: Recursively search for files using glob patterns.
- **Rich UI**: Modern command-line interface with colored output, spinners, and execution traces using the `rich` library.
- **Safety**: Execution trace shows exactly what tools are being called and their results.

## Prerequisites

- Python 3.12+
- `uv` (recommended) or `pip`
- Google Gemini API Key

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd cli-agent
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API key:

   ```bash
   API_KEY=your_google_gemini_api_key
   ```

3. **Install dependencies:**
   Using `uv` (recommended):

   ```bash
   uv sync
   ```

   Or using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   _(Note: You may need to generate requirements.txt from pyproject.toml if not using uv)_

## Usage

Run the agent using `uv`:

```bash
uv run main.py
```

Or with python directly if dependencies are installed:

```bash
python main.py
```

### Example Commands

- "Create a new directory called 'notes' and add a file named 'ideas.txt' with some startup ideas."
- "Find all python files in the current directory."
- "Rename 'old_project' to 'archive/old_project'."
- "Read the contents of 'README.md'."

## Project Structure

- `main.py`: Entry point of the application. Handles the CLI loop and UI.
- `agent.py`: Contains the `Agent` class which manages the interaction with the Gemini API.
- `tools.py`: Definitions and implementations of the file system tools (read, write, list, etc.).
- `pyproject.toml`: Project configuration and dependencies.

## Tools Available

- `read_file`: Read content of a file.
- `write_file`: Write content to a file.
- `make_file`: Create a new empty file.
- `make_dir`: Create a new directory.
- `list_dir`: List contents of a directory.
- `rename_file_or_directory`: Rename or move files/directories.
- `remove_file`: Delete a file.
- `remove_directory`: Delete a directory.
- `search_files`: Search for files matching a pattern.

## License

[MIT License](LICENSE)
