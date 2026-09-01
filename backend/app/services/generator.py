import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


class AnswerGenerator:

    def __init__(self):

        self.llm = ChatGroq(
            model=os.getenv("GROQ_MODEL"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

        self.system_prompt = """
You are a Harry Potter book assistant.

Answer the user's question using ONLY the provided context from
the Harry Potter books.

Rules:

1. Use only information found in the provided context.
2. Do not invent or assume information that is not in the context.
3. If the context does not contain enough information to answer the question,
   say that the information was not found in the provided book context.
4. Give a clear and concise answer.
5. You may mention the book name and page number when useful.
"""


    def generate(self, question: str, context: str) -> str:

        user_prompt = f"""
Context from the Harry Potter books:

{context}


Question:

{question}


Answer:
"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt),
        ]

        response = self.llm.invoke(messages)

        return response.content.strip()

