
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.router import QueryRouter
from app.services.retrieval import Retriever
from app.services.generator import AnswerGenerator


router = APIRouter()


# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    route: str
    answer: str


# --------------------------------------------------
# Initialize Services
# --------------------------------------------------

query_router = QueryRouter()
retriever = Retriever()
generator = AnswerGenerator()


# --------------------------------------------------
# Query Endpoint
# --------------------------------------------------

@router.post("/", response_model=QueryResponse)
def query(request: QueryRequest):

    question = request.question.strip()

    # ----------------------------------------------
    # Validate question
    # ----------------------------------------------

    if not question:
        return QueryResponse(
            question=question,
            route="off-topic",
            answer="Please provide a question."
        )

    # ----------------------------------------------
    # Step 1: Route the question
    # ----------------------------------------------

    route = query_router.classify(question)

    # ----------------------------------------------
    # Step 2: Chitchat
    # ----------------------------------------------

    if route == "chitchat":

        answer = generator.generate(
            question=question,
            context="The user is having a casual conversation."
        )

        return QueryResponse(
            question=question,
            route=route,
            answer=answer
        )

    # ----------------------------------------------
    # Step 3: Off-topic
    # ----------------------------------------------

    if route == "off-topic":

        return QueryResponse(
            question=question,
            route=route,
            answer=(
                "I can only answer questions about the Harry Potter books."
            )
        )

    # ----------------------------------------------
    # Step 4: Retrieve relevant chunks
    # ----------------------------------------------

    results = retriever.search(
        question=question,
        top_k=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # ----------------------------------------------
    # Build context
    # ----------------------------------------------

    context_parts = []

    for i, document in enumerate(documents):

        metadata = metadatas[i]

        book_name = metadata.get("book_name", "Unknown book")
        page_number = metadata.get("page_number", "Unknown page")

        context_parts.append(
            f"""
Book: {book_name}
Page: {page_number}

{document}
"""
        )

    context = "\n\n".join(context_parts)

    # ----------------------------------------------
    # Step 5: Generate final answer
    # ----------------------------------------------

    answer = generator.generate(
        question=question,
        context=context
    )

    # ----------------------------------------------
    # Return response
    # ----------------------------------------------

    return QueryResponse(
        question=question,
        route=route,
        answer=answer
    )

