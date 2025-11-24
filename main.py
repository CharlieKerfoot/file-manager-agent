from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

class Agent:
    def __init__(self, model: str, tools: dict[str, dict]):
        self.model = model
        self.client = genai.Client(api_key=os.environ.get("API_KEY"))
        self.contents = []
        self.tools = tools
 
    def run(self, contents: str):
        self.contents.append({"role": "user", "parts": [{"text": contents}]})
 
        config = types.GenerateContentConfig(
            tools=[types.Tool(function_declarations=[tool["definition"] for tool in self.tools.values()])]
        )
        response = self.client.models.generate_content(model=self.model, contents=self.contents, config=config)
        if (response.candidates == None):
            print("Error: Model Output Failed")
            exit()
        self.contents.append(response.candidates[0].content)
 
        return response

read_file_definition = {
    "name": "read_file",
    "description": "Reads a file and returns its contents",
    "parameters": {
    },
}

list_dir_definition = {
    "name": "list_dir",
    "description": "Returns contents of a directory",
    "parameters": {
    }
}

move_file_definition = {
    "name": "move_dir",
    "description": "Moves a file into a different directory",
    "parameters": {
    }
}

write_file_definition = {
    "name": "write_file",
    "description": "Writes given contents in a file"
}

def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read()

def write_file(file: str, contents: str) -> bool:
    with open(file, "w") as f:
        f.write(contents)
    return True

tools = {
    "read_file": {"definition": read_file_definition, "function": read_file},
    "write_file": {},
}

def main():
    load_dotenv()
    agent = Agent(model="gemini-2.5-flash", tools=tools)
    while (True):
        print("Prompt the File Manager Agent:")
        print("(type \"exit\" to quit)\n")
        prompt = input()
        if (prompt == "exit"): exit()
        print("Generating output... It may take some time.")
        response = agent.run(contents=prompt)
        print(response.text)


if __name__ == "__main__":
    main()
