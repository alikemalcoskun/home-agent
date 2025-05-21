# https://python.langchain.com/docs/integrations/chat/openai/
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
# https://python.langchain.com/v0.1/docs/modules/model_io/output_parsers/types/json/
from langchain_core.output_parsers import JsonOutputParser

import logging
from dotenv import load_dotenv
import os

from loguru import logger



class LLMService:
    def __init__(self):
        self.model = self._build_model()
        self.json_output_parser = JsonOutputParser()

    def _build_model(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=OPENAI_API_KEY,
        )
        self.json_output_parser = JsonOutputParser()

    def invoke(self, prompt: ChatPromptTemplate, is_response_json=True, tools=[], **kwargs):
        if len(tools) > 0:
            return self.invoke_with_tools(prompt=prompt, tools=tools, **kwargs)

        messages = prompt.invoke(**kwargs)
        response = self.model.invoke(messages)
        
        response_content = response.content

        if is_response_json:
            try:
                return self.json_output_parser.parse(response_content)
            except Exception as e:
                logger.error(f"Error parsing JSON: {e}")
                # Return a default structure if parsing fails
                return {}
        
        return response_content
    
    def invoke_with_tools(self, prompt: ChatPromptTemplate, tools=[], **kwargs):
        """
            Invoke LLM tool calling loop
        """
        tools_dict = {tool.name: tool for tool in tools}
        messages = prompt.invoke(**kwargs)
        model_with_tools = self.model.bind_tools(tools)
        response = model_with_tools.invoke(messages)
        
        tool_responses = []
        if response.tool_calls:
            for tool_call in response.tool_calls:
                logger.info(f"Tool call: {tool_call}")
                selected_tool = tools_dict[tool_call["name"]]
                
                # Get the tool arguments
                tool_args = {}
                
                # If the tool has an args_schema, use it to map the arguments
                if hasattr(selected_tool, 'args_schema') and selected_tool.args_schema:
                    # Get the argument names from the schema
                    arg_names = list(selected_tool.args_schema.keys())
                    
                    # Map the tool call arguments to the function arguments
                    for i, (key, value) in enumerate(tool_call["args"].items()):
                        if key.startswith("__") and key.endswith("__"):
                            # Convert __arg1 to 0, __arg2 to 1, etc.
                            arg_index = int(key[2:-2]) - 1
                            if arg_index < len(arg_names):
                                tool_args[arg_names[arg_index]] = value
                        else:
                            # If the argument name doesn't have the __ prefix and __ suffix, use it as is
                            tool_args[key] = value
                else:
                    # If the tool doesn't have an args_schema, use the arguments as is
                    tool_args = tool_call["args"]
                
                logger.info(f"Tool args: {tool_args}")
                
                tool_response = selected_tool.invoke(tool_args)
                tool_responses.append({"name": tool_call["name"], "args": tool_args, "response": tool_response})
        
        # Add tool responses to the original prompt
        for tool_response in tool_responses:
            # Convert the response to a string and escape curly braces
            response_str = str(tool_response["response"]).replace("{", "").replace("}", "").replace("'", "").replace("\"", "").replace("[", "").replace("]", "")
            tool_message = f"{tool_response['name']}({','.join([f'{k}={v}' for k, v in tool_response['args'].items()])}): {response_str}"
            if len(prompt.messages) > 0:
                prompt = prompt[:-1] + [SystemMessage(content=tool_message)] + prompt[-1]
            else:
                prompt = prompt + [SystemMessage(content=tool_message)]
        
        return self.invoke(prompt, **kwargs)


class LLMServiceMock:
    def __init__(self):
        pass

    def invoke(self, prompt: ChatPromptTemplate, is_response_json=False, **kwargs):
        logging.info(f"Mocking LLMService invoke with kwargs: {kwargs} and is_response_json: {is_response_json}")
        return {
            "type": "mock",
        }