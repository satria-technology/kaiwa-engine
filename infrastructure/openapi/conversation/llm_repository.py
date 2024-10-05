import datetime
from openai import OpenAI

from domain.conversation.model import Message
from domain.conversation.repository import LargeLanguageModelRepository

class OpenAIPlatformLLMRepository(LargeLanguageModelRepository):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_text(self, messages: list[Message]) -> str:
        completion = self.client.chat.completions.create(
            model= self.model,
            messages=[ 
                {
                    "role": "assistant" if message.sender.name == "kaiwa" else "user",
                    "content": message.message
                } for message in reversed(messages)
            ],
        )
        return completion.choices[0].message.content