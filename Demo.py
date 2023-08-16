import json, uuid


def generate_question_json(question_text, session_number, topic_number, question_number):
    # Generate unique UUID for question_id
    question_id = str(uuid.uuid4())

    # Construct question key
    question_key = f"session{session_number:02}_t{topic_number:02}__{question_number:02}"

    # Extract options from question text
    options_start = question_text.find("\na) ")
    options_end = question_text.find("\nAnswer: ")
    options_text = question_text[options_start:options_end].strip()
    options = [option.strip() for option in options_text.split("\n") if option.strip()]

    # Extract correct answer from question text
    answer_start = question_text.find("\nAnswer: ")
    answer_end = question_text.find(".", answer_start)
    correct_answer = question_text[answer_start + 8:answer_end].strip()

    # Find the correct option
    correct_option = None
    for option_text in options:
        if option_text.startswith(correct_answer):
            correct_option = option_text.strip()
            break

    # Find the explanation
    explanation_start = question_text.find("Explanation: ", answer_end)
    explanation_end = question_text.find("\n", explanation_start)
    explanation_content = question_text[explanation_start + 13: explanation_end].strip()

    # Find the tag_name
    tags_start = question_text.find("Tag Names: ", explanation_end)
    tag_names = question_text[tags_start + 11: ].strip()

    # Construct question JSON object
    question_json = {
        "question_key": question_key,
        "question_id": question_id,
        "explanation_for_answer": {
            "content": explanation_content,
            "content_type": "TEXT"
        },
        "skills": [],
        "toughness": "EASY",
        "question_type": "MULTIPLE_CHOICE",
        "question": {
            "content": question_text[:options_start].strip(),
            "content_type": "MARKDOWN",
            "tag_names": json.loads(tag_names),
            "multimedia": []
        },
        "options": []
    }

    # Construct options JSON objects
    for option_text in options:
        is_correct = option_text == correct_option
        content = option_text[3:].strip()
        option_json = {
            "content": content,
            "content_type": "TEXT",
            "is_correct": is_correct,
            "multimedia": []
        }
        question_json["options"].append(option_json)

    return question_json


def generate_questions_from_file(file_path):
    with open(file_path, "r") as file:
        questions_str = file.read()
        questions_start = questions_str.index("1.")
        questions = questions_str[questions_start:].split("\n\n")
        questions_json = []
        for i, question in enumerate(questions):
            question_number = i + 1
            session_number = 1
            topic_number = 1
            question_json = generate_question_json(question, session_number, topic_number, question_number)
            questions_json.append(question_json)
        return questions_json


# Session and topic numbers
session_number = 1
topic_number = 1


def generate_json_file(questions_json, file_path):
    with open(file_path, "w") as file:
        json.dump(questions_json, file, indent=4)
    print("File generated successfully.")


if __name__ == "__main__":
    # Generate JSON representation of questions from the input text file
    file_name = input("Enter file name(without extension): ")
    questions_json = generate_questions_from_file("./parent_file/" + file_name + ".txt")

    # Write the JSON data to a new JSON file
    generate_json_file(questions_json, "./output_json/" + file_name + ".json")