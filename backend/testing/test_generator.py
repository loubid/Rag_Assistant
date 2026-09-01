from app.services.generator import AnswerGenerator


generator = AnswerGenerator()


question = "Who is Harry Potter?"


context = """
Harry Potter is a boy who defeated He-Who-Must-Not-Be-Named.
He has a scar on his forehead caused by the curse with which
You-Know-Who attempted to kill him.

Harry Potter attends Hogwarts School of Witchcraft and Wizardry.
"""


answer = generator.generate(
    question=question,
    context=context
)


print("\n" + "=" * 70)
print("GENERATED ANSWER")
print("=" * 70)

print(answer)

