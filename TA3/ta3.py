# ============================================
# INTELLIGENT TUTORING SYSTEM
# Case-Based Reasoning (CBR)
# Dynamic User Input Version
# ============================================

# --------------------------------------------
# 1. CASE BASE: PAST STUDENT CASES
# --------------------------------------------

case_base = [
    {
        "case_id": 1,
        "problem": {
            "topic": "quadratic equations",
            "error_pattern": ["wrong formula", "sign error"],
            "difficulty": "medium",
            "score": 55
        },
        "solution": {
            "feedback": [
                "Review the quadratic formula.",
                "Check positive and negative signs carefully."
            ],
            "lesson": ["Step-by-step quadratic formula practice"],
            "intervention": [
                "Worked examples followed by guided practice."
            ]
        }
    },

    {
        "case_id": 2,
        "problem": {
            "topic": "quadratic equations",
            "error_pattern": ["wrong formula", "substitution error"],
            "difficulty": "medium",
            "score": 60
        },
        "solution": {
            "feedback": [
                "Identify a, b, and c before using the formula."
            ],
            "lesson": [
                "Identifying coefficients in quadratic equations"
            ],
            "intervention": [
                "Formula identification exercises."
            ]
        }
    },

    {
        "case_id": 3,
        "problem": {
            "topic": "linear equations",
            "error_pattern": ["transposition error", "sign error"],
            "difficulty": "easy",
            "score": 65
        },
        "solution": {
            "feedback": [
                "Remember to change the sign when moving a term."
            ],
            "lesson": [
                "Rules for solving linear equations"
            ],
            "intervention": [
                "Short exercises focusing on sign changes."
            ]
        }
    },

    {
        "case_id": 4,
        "problem": {
            "topic": "quadratic equations",
            "error_pattern": ["discriminant error", "arithmetic error"],
            "difficulty": "hard",
            "score": 48
        },
        "solution": {
            "feedback": [
                "Review how to calculate b² - 4ac.",
                "Double-check arithmetic."
            ],
            "lesson": [
                "Understanding and calculating the discriminant"
            ],
            "intervention": [
                "Discriminant drills with immediate feedback."
            ]
        }
    },

    {
        "case_id": 5,
        "problem": {
            "topic": "quadratic equations",
            "error_pattern": [
                "wrong formula",
                "sign error",
                "substitution error"
            ],
            "difficulty": "medium",
            "score": 50
        },
        "solution": {
            "feedback": [
                "Identify a, b, and c first.",
                "Apply the quadratic formula carefully."
            ],
            "lesson": [
                "Complete quadratic formula tutorial"
            ],
            "intervention": [
                "Worked example + guided practice + error checking."
            ]
        }
    }
]

# --------------------------------------------
# 2. DISPLAY AVAILABLE ERROR TYPES
# --------------------------------------------

available_errors = [
    "wrong formula",
    "sign error",
    "substitution error",
    "arithmetic error",
    "transposition error",
    "discriminant error"
]

# --------------------------------------------
# 3. GET NEW CASE FROM USER
# --------------------------------------------

def get_new_case(case_id):

    print("\n" + "=" * 60)
    print("ENTER NEW STUDENT CASE")
    print("=" * 60)

    # Topic
    topic = input("Enter math topic: ").strip().lower()

    # Difficulty
    while True:
        difficulty = input(
            "Enter difficulty (easy/medium/hard): "
        ).strip().lower()

        if difficulty in ["easy", "medium", "hard"]:
            break

        print("Invalid difficulty. Please choose easy, medium, or hard.")

    # Score
    while True:
        try:
            score = float(input("Enter student's score (0-100): "))

            if 0 <= score <= 100:
                break

            print("Score must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")

    # Error patterns
    print("\nAvailable error patterns:")

    for i, error in enumerate(available_errors, start=1):
        print(f"{i}. {error}")

    while True:
        error_input = input(
            "\nEnter error numbers separated by commas "
            "(example: 1,2,3): "
        )

        try:
            selected_numbers = [
                int(x.strip())
                for x in error_input.split(",")
            ]

            if all(
                1 <= number <= len(available_errors)
                for number in selected_numbers
            ):
                break

            print("One or more numbers are invalid.")

        except ValueError:
            print("Please enter numbers separated by commas.")

    error_pattern = [
        available_errors[number - 1]
        for number in selected_numbers
    ]

    return {
        "case_id": case_id,
        "problem": {
            "topic": topic,
            "error_pattern": error_pattern,
            "difficulty": difficulty,
            "score": score
        }
    }


# --------------------------------------------
# 4. SIMILARITY ASSESSMENT
# --------------------------------------------

def calculate_similarity(new_problem, old_problem):

    score = 0

    # Topic = 40%
    if new_problem["topic"] == old_problem["topic"]:
        score += 40

    # Error patterns = 40%
    new_errors = set(new_problem["error_pattern"])
    old_errors = set(old_problem["error_pattern"])

    if new_errors or old_errors:

        intersection = new_errors.intersection(old_errors)
        union = new_errors.union(old_errors)

        error_similarity = len(intersection) / len(union)

        score += error_similarity * 40

    # Difficulty = 10%
    if new_problem["difficulty"] == old_problem["difficulty"]:
        score += 10

    # Score similarity = 10%
    score_difference = abs(
        new_problem["score"] - old_problem["score"]
    )

    score_similarity = max(
        0,
        1 - (score_difference / 100)
    )

    score += score_similarity * 10

    return round(score, 2)


# --------------------------------------------
# 5. RETRIEVE SIMILAR CASES
# --------------------------------------------

def retrieve_cases(new_case):

    results = []

    for case in case_base:

        similarity = calculate_similarity(
            new_case["problem"],
            case["problem"]
        )

        results.append({
            "case": case,
            "similarity": similarity
        })

    # Highest similarity first
    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results


# --------------------------------------------
# 6. ADAPT SOLUTION
# --------------------------------------------

def adapt_solution(new_case, retrieved_case):

    errors = new_case["problem"]["error_pattern"]

    feedback = []
    lessons = []
    interventions = []

    # Customize feedback according to errors
    if "wrong formula" in errors:

        feedback.append(
            "Review the correct formula before starting the problem."
        )

        lessons.append(
            "Identifying and selecting the correct formula"
        )

        interventions.append(
            "Practice choosing the correct formula from several examples."
        )

    if "sign error" in errors:

        feedback.append(
            "Check positive and negative signs at every step."
        )

        lessons.append(
            "Handling positive and negative signs"
        )

        interventions.append(
            "Complete guided exercises focusing on sign changes."
        )

    if "substitution error" in errors:

        feedback.append(
            "Identify a, b, and c before substituting values."
        )

        lessons.append(
            "Correct substitution into formulas"
        )

        interventions.append(
            "Use a step-by-step substitution checklist."
        )

    if "arithmetic error" in errors:

        feedback.append(
            "Recheck calculations before submitting the final answer."
        )

        lessons.append(
            "Arithmetic accuracy"
        )

        interventions.append(
            "Complete short calculation drills."
        )

    if "transposition error" in errors:

        feedback.append(
            "Remember to change the sign when moving terms."
        )

        lessons.append(
            "Transposition rules"
        )

        interventions.append(
            "Practice moving terms across the equals sign."
        )

    if "discriminant error" in errors:

        feedback.append(
            "Review the discriminant formula b² - 4ac."
        )

        lessons.append(
            "Calculating the discriminant"
        )

        interventions.append(
            "Practice calculating discriminants step by step."
        )

    # If an error was not recognized
    if not feedback:
        feedback.append(
            "Review the student's solution step by step."
        )

    # Include successful intervention from retrieved case
    interventions.append(
        "Adapted from the successful intervention used in "
        f"Case {retrieved_case['case_id']}."
    )

    return {
        "feedback": feedback,
        "lesson": lessons,
        "intervention": interventions
    }


# --------------------------------------------
# 7. DISPLAY RESULTS
# --------------------------------------------

def display_results(new_case, ranked_cases, adapted_solution):

    print("\n" + "=" * 60)
    print("CBR ANALYSIS RESULTS")
    print("=" * 60)

    # New problem
    print("\nNEW PROBLEM DESCRIPTION")
    print("-" * 60)

    print("Topic:",
          new_case["problem"]["topic"])

    print("Difficulty:",
          new_case["problem"]["difficulty"])

    print("Score:",
          new_case["problem"]["score"])

    print("Error patterns:",
          ", ".join(new_case["problem"]["error_pattern"]))


    # Ranking
    print("\nSIMILARITY RANKING")
    print("-" * 60)

    for rank, result in enumerate(ranked_cases, start=1):

        case = result["case"]

        print(
            f"{rank}. Case {case['case_id']} "
            f"-> Similarity: {result['similarity']}%"
        )


    # Retrieved case
    best_match = ranked_cases[0]["case"]

    print("\nMOST RELEVANT PAST CASE")
    print("-" * 60)

    print("Case ID:", best_match["case_id"])

    print(
        "Similarity:",
        ranked_cases[0]["similarity"],
        "%"
    )

    print(
        "Topic:",
        best_match["problem"]["topic"]
    )

    print(
        "Errors:",
        ", ".join(
            best_match["problem"]["error_pattern"]
        )
    )


    # Adapted solution
    print("\nADAPTED FINAL SOLUTION")
    print("-" * 60)

    print("\nPersonalized Feedback:")

    for item in adapted_solution["feedback"]:
        print("  ✔", item)

    print("\nPersonalized Lessons:")

    for item in adapted_solution["lesson"]:
        print("  ✔", item)

    print("\nRecommended Intervention:")

    for item in adapted_solution["intervention"]:
        print("  ✔", item)


# --------------------------------------------
# 8. RETAIN NEW CASE
# --------------------------------------------

def retain_case(new_case, adapted_solution):

    # Add the generated solution to the case
    new_case["solution"] = adapted_solution

    # Store the new case
    case_base.append(new_case)

    print("\n" + "=" * 60)
    print("LEARNING / RETAIN STAGE")
    print("=" * 60)

    print("✔ New case saved successfully!")

    print(
        f"✔ Case {new_case['case_id']} added to the case base."
    )

    print(
        f"✔ Updated case base contains "
        f"{len(case_base)} cases."
    )


# --------------------------------------------
# 9. DISPLAY UPDATED CASE BASE
# --------------------------------------------

def display_case_base():

    print("\nUPDATED CASE BASE")
    print("=" * 60)

    for case in case_base:

        print(
            f"Case {case['case_id']} | "
            f"Topic: {case['problem']['topic']} | "
            f"Difficulty: {case['problem']['difficulty']} | "
            f"Score: {case['problem']['score']}"
        )

        print(
            "   Errors:",
            ", ".join(
                case["problem"]["error_pattern"]
            )
        )


# --------------------------------------------
# 10. MAIN PROGRAM
# --------------------------------------------

def main():

    print("=" * 60)
    print("INTELLIGENT TUTORING SYSTEM")
    print("CASE-BASED REASONING")
    print("=" * 60)

    print(
        "\nThe system currently contains",
        len(case_base),
        "past cases."
    )

    # Dynamically create new case
    new_case_id = len(case_base) + 1

    new_case = get_new_case(new_case_id)

    # Retrieve similar cases
    ranked_cases = retrieve_cases(new_case)

    # Get best case
    best_case = ranked_cases[0]["case"]

    # Adapt solution
    adapted_solution = adapt_solution(
        new_case,
        best_case
    )

    # Display results
    display_results(
        new_case,
        ranked_cases,
        adapted_solution
    )

    # Retain new case
    retain_case(
        new_case,
        adapted_solution
    )

    # Display updated case base
    display_case_base()


# --------------------------------------------
# RUN PROGRAM
# --------------------------------------------

if __name__ == "__main__":
    main()