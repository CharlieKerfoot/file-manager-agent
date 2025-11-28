import os
import glob

def read_file(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(file_path: str, contents: str) -> str:
    try:
        with open(file_path, "w") as f:
            f.write(contents)
        return "Success"
    except Exception as e:
        return f"Error writing file: {e}"

def rename_file_or_directory(src_path: str, new_path: str) -> str:
    try:
        os.rename(src_path, new_path)
        return "Success"
    except Exception as e:
        return f"Error renaming: {e}"

def remove_file(file_path: str) -> str:
    try:
        os.remove(file_path)
        return "Success"
    except Exception as e:
        return f"Error removing file: {e}"

def remove_directory(directory_path: str) -> str:
    try:
        os.rmdir(directory_path)
        return "Success"
    except Exception as e:
        return f"Error removing directory: {e}"

def make_file(file_path: str) -> str:
    try:
        open(file_path, 'a').close()
        return "Success"
    except Exception as e:
        return f"Error creating file: {e}"

def make_dir(directory_path: str) -> str:
    try:
        os.mkdir(directory_path)
        return "Success"
    except Exception as e:
        return f"Error creating directory: {e}"

def list_dir(directory_path: str) -> str | list[str]:
    try:
        full_path = os.path.expanduser(directory_path)
        return os.listdir(full_path)
    except Exception as e:
        return f"Error listing directory: {e}"

def search_files(directory_path: str, pattern: str) -> str | list[str]:
    try:
        full_path = os.path.expanduser(directory_path)
        search_pattern = os.path.join(full_path, "**", pattern)
        files = glob.glob(search_pattern, recursive=True)
        return files
    except Exception as e:
        return f"Error searching files: {e}"

read_file_definition = {
    "name": "read_file",
    "description": "Reads a file and returns its contents",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read.",
            }
        },
        "required": ["file_path"],
    },
}

write_file_definition = {
    "name": "write_file",
    "description": "Writes given contents in a file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write.",
            },
            "contents": {
                "type": "string",
                "description": "The contents string to write in the file.",
            }
        },
        "required": ["file_path", "contents"],
    },
}

rename_file_or_directory_definition = {
    "name": "rename_file_or_directory",
    "description": "Renames source file or directory to the new path name. Can also be used to move files or directories.",
    "parameters": {
        "type": "object",
        "properties": {
            "src_path": {
                "type": "string",
                "description": "Path to the file or directory.",
            },
            "new_path": {
                "type": "string",
                "description": "New path name or path for the file or directory to be moved to.",
            }
        },
        "required": ["src_path", "new_path"],
    },
}

remove_file_definition = {
    "name": "remove_file",
    "description": "Removes a file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file.",
            }
        },
        "required": ["file_path"],
    },
}

remove_directory_definition = {
    "name": "remove_directory",
    "description": "Removes (deletes) a directory path",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "Path to the directory.",
            }
        },
        "required": ["directory_path"],
    },
}

make_file_definition = {
    "name": "make_file",
    "description": "Creates a file at a given path",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path where the new file is created.",
            }
        },
        "required": ["file_path"],
    },
}

make_dir_definition = {
    "name": "make_dir",
    "description": "Creates a directory at a given path",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "Path where the new directory is created.",
            }
        },
        "required": ["directory_path"],
    },
}

list_dir_definition = {
    "name": "list_dir",
    "description": "Returns contents of a directory",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "Path to the directory.",
            }
        },
        "required": ["directory_path"],
    },
}

search_files_definition = {
    "name": "search_files",
    "description": "Searches for files matching a pattern in a directory recursively",
    "parameters": {
        "type": "object",
        "properties": {
            "directory_path": {
                "type": "string",
                "description": "Path to the directory to search in.",
            },
            "pattern": {
                "type": "string",
                "description": "Glob pattern to match files (e.g., '*.py').",
            }
        },
        "required": ["directory_path", "pattern"],
    },
}

tools_map = {
    "read_file": {"definition": read_file_definition, "function": read_file},
    "write_file": {"definition": write_file_definition, "function": write_file},
    "rename_file_or_directory": {"definition": rename_file_or_directory_definition, "function": rename_file_or_directory},
    "remove_file": {"definition": remove_file_definition, "function": remove_file},
    "remove_directory": {"definition": remove_directory_definition, "function": remove_directory},
    "make_file": {"definition": make_file_definition, "function": make_file},
    "make_dir": {"definition": make_dir_definition, "function": make_dir},
    "list_dir": {"definition": list_dir_definition, "function": list_dir},
    "search_files": {"definition": search_files_definition, "function": search_files},
}
