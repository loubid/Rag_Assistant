
from app.services.router import QueryRouter


router = QueryRouter()


questions = [
    "Who is Harry Potter?",
    "Hello!",
    "What is the capital of Egypt?"
]


for question in questions:

    result = router.classify(question)

    print("\n" + "=" * 60)
    print("Question:", question)
    print("Route:", result)

