from openai import OpenAI
from config import get_settings
from entity import User, UserAction

class Agent:
    def __init__(self, conversation):
        settings = get_settings()
        self.model = settings.gpt_version
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.chat_history = conversation.chatHistory
        self.location = conversation.locationId
        self.user = User(conversation.userInfo)
        self.user_action = UserAction(conversation.userAction)
    
    def load_user_info(self, user_info):
        self.user_name = user_info.name
        self.user

    def make_message(self, role, content):
        message = {"role": role, "content": content}
        return message
    
    def add_messages(self, messages, new_messages):
        for message in new_messages:
            messages.append(message)
        return messages

    def user_action_message(self, name):
        action_type =  self.user_action.action
        if action_type=="chat":
            content = self.user_action.chat
            message = self.make_message("user", content)
        elif action_type=="battle":
            content = f"{self.user.name}이 {name}에게 승부를 걸어왔다."
            message = self.make_message("system", content)
        elif action_type=="give":
            content = f"{self.user.name}이 {name}에게 {self.user_action.item.name}을 건네주었다."
            message = self.make_message("system", content)
        elif action_type=="catch":
            content = f"{self.user.name}이 몬스터볼을 {name}에게 던졌다."
            message = self.make_message("system", content)
        
        return message

    def get_response(self, messages, format):
        response = self.client.beta.chat.completions.parse(
            model=self.model, messages=messages, response_format=format
        )
        return response.choices[0].message.parsed