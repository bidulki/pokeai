from config import get_settings
from openai import OpenAI
from anthropic import Anthropic
from google import genai 
from abc import *
import json

class Agent:
    def __init__(self):
        settings = get_settings()
        self.provider = settings.provider
        self.model = settings.get_current_model()

        if self.provider == "openai":
            self.client = OpenAI(api_key=settings.openai_api_key)
        elif self.provider == "anthropic":
            self.client = Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "google":
            self.client = genai.Client(api_key=settings.google_api_key, http_options={"api_version": "v1alpha"})

        self.chat_history = []

    @abstractmethod
    def get_system_prompt(self):
        # 시스템 프롬프트 로딩하는 부분
        pass
    
    def make_message(self, role, content):
        return {"role": role, "content": content}

    def add_message(self, message):
        self.chat_history.append(message)
    
    def get_response_structured_output(self, messages, format):
        # Structured Output format으로 통신 보내고 결과 받는 함수
        if self.provider == "openai":
            system_message = {"role": "system", "content": self.get_system_prompt()}
            messages = [system_message] + messages
            response = self.client.beta.chat.completions.parse(
                model=self.model, 
                messages=messages,
                response_format=format
            )
            return response.choices[0].message.parsed
        elif self.provider == "google":
            print(format)
            response = self.client.models.generate_content(
                model=self.model,
                contents=[message['content'] for message in messages],
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.get_system_prompt(),
                    response_mime_type="application/json",
                    temperature=0.7,
                    response_schema=format
                )
            )
            print(response.text)
            return json.loads(response.text)
    
    def get_response_function_calling(self, messages, tools):
        # Function Calling format으로 통신 보내고 결과 받는 함수
        if self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                system=self.get_system_prompt(),
                messages=messages,
                max_tokens=512,
                tools=tools,
                tool_choice={"type": "any"}
            )
            return response.content[0]
        elif self.provider == "google":
            response = self.client.models.generate_content(
                model=self.model,
                contents=[message['content'] for message in messages],
                config=genai.types.GenerateContentConfig(
                    system_instruction=self.get_system_prompt(),
                    tools=[genai.types.Tool(function_declarations=tools)],
                    automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(disable=False),
                    tool_config={
                        "function_calling_config": {
                            "mode": "any"
                        }
                    }
                )
            )
            return response.candidates[0].content.parts[0].function_call