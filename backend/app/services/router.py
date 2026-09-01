
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


class QueryRouter:

    def __init__(self):

        self.llm = ChatGroq(
            model=os.getenv("GROQ_MODEL"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

        self.system_prompt = """
You classify messages for a Harry Potter book search system.

Return exactly one label and nothing else:

retrieve - questions about the books, characters, places, or events

chitchat - greetings, thanks, or casual conversation

off-topic - anything unrelated to the books
"""


    def classify(self, query: str) -> str:

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=query),
        ]

        response = self.llm.invoke(messages)

        route = response.content.strip().lower()

        # Take only the first line
        route = route.splitlines()[0].strip(" `.,:")

        # Safety check
        if route not in {
            "retrieve",
            "chitchat",
            "off-topic"
        }:
            route = "off-topic"

        return route
