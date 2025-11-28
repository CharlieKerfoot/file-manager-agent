from google import genai
from google.genai import types

from typing import Any, cast

import os
from dotenv import load_dotenv

class Agent:
    def __init__(self, model: str, tools: dict[str, dict], system_instruction: str = "You are a helpful assistant in charge of managing the user's files and directories on their computer."):
        self.model = model
        self.client = genai.Client(api_key=os.environ.get("API_KEY"))
        self.contents = []
        self.tools = tools
        self.system_instruction = system_instruction
 
    def run(self, contents: str | list[dict[str, str]]):
        if isinstance(contents, list):
            self.contents.append({"role": "user", "parts": contents})
        else:
            self.contents.append({"role": "user", "parts": [{"text": contents}]})

        config = types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            tools=[types.Tool(function_declarations=[tool["definition"] for tool in self.tools.values()])]
        )
        response = self.client.models.generate_content(model=self.model, contents=self.contents, config=config)
        if (response.candidates == None):
            print("Error: Model Output Failed")
            exit()
        self.contents.append(response.candidates[0].content)

        if response.function_calls:
            functions_response_parts: list[dict] = []
            for tool_call in response.function_calls:
                print(f"[Function Call] {tool_call}")

                raw_args = tool_call.args

                if raw_args is None:
                    args = {}
                elif isinstance(raw_args, dict):
                    args = raw_args
                elif hasattr(raw_args, "to_dict"):
                    args = raw_args.to_dict()
                else:
                    try:
                        args = dict(raw_args)
                    except Exception:
                        raise ValueError(f"Could not convert function call args: {raw_args!r}")

                if tool_call.name in self.tools:
                    result_value = self.tools[tool_call.name]["function"](**args)
                    result = {"result": result_value}
                else:
                    result = {"error": "Tool not found"}
 
                print(f"[Function Response] {result}")
                functions_response_parts.append({"functionResponse": {"name": tool_call.name, "response": result}})

            return self.run(functions_response_parts)
 
        return response

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

def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path: str, contents: str) -> bool:
    with open(file_path, "w") as f:
        f.write(contents)
    return True

def rename_file_or_directory(src_path: str, new_path: str) -> bool:
    os.rename(src_path, new_path)
    return True

def remove_file(file_path: str) -> bool:
    os.remove(file_path)
    return True

def remove_directory(directory_path: str) -> bool:
    os.rmdir(directory_path)
    return True

def make_file(file_path: str) -> bool:
    open(file_path, 'a').close()
    return True

def make_dir(directory_path: str) -> bool:
    os.mkdir(directory_path)
    return True

def list_dir(directory_path: str) -> list[str]:
    full_path = os.path.expanduser(directory_path)
    return os.listdir(full_path)

tools = {
    "read_file": {"definition": read_file_definition, "function": read_file},
    "write_file": {"definition": write_file_definition, "function": write_file},
    "rename_file_or_directory": {"definition": rename_file_or_directory_definition, "function": rename_file_or_directory},
    "remove_file": {"definition": remove_file_definition, "function": remove_file},
    "remove_directory": {"definition": remove_directory_definition, "function": remove_directory},
    "make_file": {"definition": make_file_definition, "function": make_file},
    "make_dir": {"definition": make_dir_definition, "function": make_dir},
    "list_dir": {"definition": list_dir_definition, "function": list_dir},
}

def main():
    load_dotenv()
    agent = Agent(model="gemini-2.5-flash", tools=tools)
    print("Prompt the File Manager Agent:")
    print("(type \"exit\" to quit)\n")
    while (True):
        prompt = input("You: ")
        if (prompt == "exit"): exit()
        print("Generating output... It may take some time.")
        response = agent.run(contents=prompt)
        print(f"Agent: {response.text}")


if __name__ == "__main__":
    main()
