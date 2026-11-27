import random
from sympy import symbols, integrate, diff, simplify

x = symbols("x")

def _demo_bank(chapter):
    bank = []
    if chapter in ("Differentiation", "Applications of Derivatives"):
        bank = [
            ("Find the derivative of x^3 - 4x^2 + 5x - 7.", "3*x**2 - 8*x + 5",
             "Differentiate term by term using d(x^n)/dx = n*x^(n-1). Therefore, the derivative is 3x² - 8x + 5."),
            ("Differentiate sin(x) + cos(x).", "cos(x) - sin(x)",
             "Using d(sin x)/dx = cos x and d(cos x)/dx = -sin x, the result is cos x - sin x."),
        ]
    elif chapter in ("Integration", "Definite Integrals"):
        bank = [
            ("Evaluate ∫(3x² + 2x + 1) dx.", "x³ + x² + x + C",
             "Integrate term by term: ∫3x² dx = x³, ∫2x dx = x², and ∫1 dx = x. Add the constant C."),
            ("Evaluate ∫cos(x) dx.", "sin(x) + C",
             "Since the derivative of sin(x) is cos(x), the integral is sin(x) + C."),
        ]
    elif chapter == "Matrices":
        bank = [
            ("If A = [[1, 2], [3, 4]], find det(A).", "-2",
             "For a 2×2 matrix [[a,b],[c,d]], det(A)=ad-bc. Here, 1×4 - 2×3 = 4 - 6 = -2."),
            ("What is the order of a matrix having 3 rows and 2 columns?", "3 × 2",
             "The order of a matrix is written as number of rows × number of columns. Hence, the order is 3 × 2."),
        ]
    elif chapter == "Complex Numbers":
        bank = [
            ("Simplify (3 + 2i) + (1 - 5i).", "4 - 3i",
             "Add real parts and imaginary parts separately: (3+1) + (2i-5i) = 4-3i."),
            ("Find i².", "-1",
             "By the definition of the imaginary unit i, i² = -1."),
        ]
    elif chapter in ("Straight Lines",):
        bank = [
            ("Find the slope of the line 2x + 3y - 6 = 0.", "-2/3",
             "Write the equation as 3y = -2x + 6, so y = (-2/3)x + 2. The slope is -2/3."),
        ]
    elif chapter in ("Probability",):
        bank = [
            ("A fair die is rolled once. Find the probability of getting an even number.", "1/2",
             "The sample space is {1,2,3,4,5,6}. Even outcomes are {2,4,6}. Thus P(E)=3/6=1/2."),
        ]
    else:
        bank = [
            (f"State the main mathematical idea used in {chapter}.", "Depends on the relevant theorem or definition.",
             f"Identify the definitions and standard results in {chapter}. Apply the relevant theorem, show each algebraic step, and verify the final result.")
        ]
    return bank

def generate_questions(year, subject, chapter, count, qtypes, difficulty):
    bank = _demo_bank(chapter)
    result = []
    for i in range(count):
        base = bank[i % len(bank)]
        qtype = qtypes[i % len(qtypes)]
        level = difficulty if difficulty != "Mixed" else ["Easy", "Medium", "Hard"][i % 3]
        question, answer, solution = base
        # Do not disguise repeated demo questions as new questions.
        if i >= len(bank):
            question = f"Practice variation {i+1}: {question}"
        options = []
        if qtype == "MCQ":
            options = [f"(A) {answer}", "(B) 0", "(C) 1", "(D) None of these"]
        result.append({
            "type": qtype, "question": question, "answer": answer,
            "solution": solution, "difficulty": level, "options": options
        })
    return result
