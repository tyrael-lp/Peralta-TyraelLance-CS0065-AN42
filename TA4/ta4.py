# Dictionary
facts = {
    # Category 1: Environment
    "temperature": 32,
    "is_raining": False,
    "humidity": 85,

    # Category 2: Appliance status
    "aircon_on": False,
    "fan_on": False,

    # Category 3: Presence and actions
    "person_present": True,
    "window_open": True
}


# Rule Based Reasoning
# Rule 1
def rule_hot(facts):
    if facts["temperature"] > 30:
        return "Turn on the aircon."
    return None


# Rule 2
def rule_humid(facts):
    if facts["humidity"] > 80:
        return "Turn on the fan."
    return None


# Rule 3
def rule_raining(facts):
    if facts["is_raining"]:
        return "Close the window."
    return None


# Rule 4
def rule_person_present(facts):
    if facts["person_present"] and not facts["aircon_on"]:
        return "Check the aircon."
    return None


# Inference engine
def inference_engine(facts, rules):
    actions = []

    for rule in rules:
        result = rule(facts)

        if result is not None:
            actions.append(result)

    return actions


rules = [
    rule_hot,
    rule_humid,
    rule_raining,
    rule_person_present
]

rbr_actions = inference_engine(facts, rules)

print("RULE-BASED REASONING ACTIONS:")
for action in rbr_actions:
    print("-", action)


# Case base containing previous problems and solutions
case_base = [
    {
        "problem": {
            "temperature_high": True,
            "humidity_high": True,
            "aircon_not_working": False
        },
        "solution": "Turn on the aircon and fan."
    },
    {
        "problem": {
            "temperature_high": False,
            "humidity_high": True,
            "aircon_not_working": False
        },
        "solution": "Turn on the fan."
    },
    {
        "problem": {
            "temperature_high": True,
            "humidity_high": False,
            "aircon_not_working": True
        },
        "solution": "Check the aircon power cable."
    }
]


# Current problem
new_problem = {
    "temperature_high": facts["temperature"] > 30,
    "humidity_high": facts["humidity"] > 80,
    "aircon_not_working": True
}


# Retrieve Step

def calculate_similarity(problem1, problem2):
    matching_features = 0

    for feature in problem1:
        if feature in problem2 and problem1[feature] == problem2[feature]:
            matching_features += 1

    return matching_features


def retrieve_most_similar_case(problem, case_base):
    most_similar_case = None
    highest_similarity = -1

    for case in case_base:
        similarity = calculate_similarity(problem, case["problem"])

        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_case = case

    return most_similar_case


# Reuse Step

similar_case = retrieve_most_similar_case(new_problem, case_base)

reused_solution = similar_case["solution"]

print("\nCASE-BASED REASONING:")
print("New problem:", new_problem)
print("Retrieved solution:", reused_solution)


# Revise Step

print("\nREVISE STEP")
print("Suggested solution:", reused_solution)

revision = input(
    "Enter a revised solution, or press Enter to keep the original: "
).strip()

if revision != "":
    final_solution = revision
else:
    final_solution = reused_solution

print("Final solution:", final_solution)


# Retain Step

new_case = {
    "problem": new_problem,
    "solution": final_solution
}

case_base.append(new_case)

print("\nRETAIN STEP")
print("New case has been added to the case base.")
print("Total number of cases:", len(case_base))