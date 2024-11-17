from openai import OpenAI
from config import get_settings

class Agent:
    def __init__(self, conversation):
        settings = get_settings()
        self.model = settings.gpt_version
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.chat_history = conversation.chatHistory
        self.location = conversation.locationId
    
    def load_user_info(self, user_info):
        self.user_name = user_info.name
        self.user

    def add_chat_history(self, role, content):
        message = {"role": role, "content": content}
        self.chat_history.append(message)

    def get_response(self, messages, format):
        response = self.client.beta.chat.completions.parse(
            model=self.model, messages=messages, response_format=format
        )

        return response.choices[0].message.parsed