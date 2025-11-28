from google import genai
from google.genai import types
import os
from typing import Any

class Agent:
    def __init__(self, model: str, tools: dict[str, dict], system_instruction: str = "You are a helpful assistant in charge of managing the user's files and directories on their computer."):
        self.model = model
        self.client = genai.Client(api_key=os.environ.get("API_KEY"))
        self.contents = []
        self.tools = tools
        self.system_instruction = system_instruction
        self.trace = []

    def clear_trace(self):
        self.trace = []
 
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
            return "Error: Model Output Failed"
            
        self.contents.append(response.candidates[0].content)

        if response.function_calls:
            functions_response_parts: list[dict] = []
            for tool_call in response.function_calls:
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
 
                self.trace.append({
                    "name": tool_call.name,
                    "args": args,
                    "result": result
                })
                functions_response_parts.append({"functionResponse": {"name": tool_call.name, "response": result}})

            return self.run(functions_response_parts)
 
        return response
