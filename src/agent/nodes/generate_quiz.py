from __future__ import annotations

from pydoc_data.topics import topics
from typing import Any, Dict
from src.llm_models.openai_models import openai_model
from src.agent.utils import load_prompt_template
from src.agent.state import State
from langchain_core.messages import HumanMessage, AIMessage
import json

def get_quiz_questions(topic: str, topic_information: str) -> Dict[str, Any]:
    try:
        prompt = load_prompt_template("quiz_generation").format(
            topic=topic,
            topic_information=topic_information,
        )
        quiz_questions = openai_model.invoke(prompt)
        parsed_quiz = json.loads(quiz_questions.content)
        parsed_quiz["valid"] = True
        return parsed_quiz
    except:
        breakpoint()
        print("Failed to generate quiz questions.")
        return {"valid": False, "invalid_quiz": quiz_questions.content}

def display_quiz(quiz_questions: Dict[str, Any]) -> None:
    print(quiz_questions["quiz_title"])
    print(f"Question: {quiz_questions["question"]}")
    print("Options:")
    print(f"A: {quiz_questions['options']['A']}")
    print(f"B: {quiz_questions['options']['B']}")
    print(f"C: {quiz_questions['options']['C']}")
    print(f"D: {quiz_questions['options']['D']}")
    user_answer = input("Enter your answer (A, B, C, or D):\n> ")
    while user_answer not in ["A", "B", "C", "D"]:
        print("Invalid answer. Please enter A, B, C, or D.")
        user_answer = input("Enter your answer (A, B, C, or D): ")
    if user_answer == quiz_questions["correct_answer"]:
        print("Correct!")
        print(quiz_questions["pass_message"])
    else:
        print("Incorrect!")
        print(quiz_questions["fail_message"])
    print(f"Explaination: {quiz_questions['explanation']}")

def generate_quiz(state: State):
    messages = state.get("messages", [])
    topic = state.get("topic", "")
    ai_messages = [ai_message for ai_message in messages if isinstance(ai_message, AIMessage)]
    topic_information = "\n".join([ai_message.content for ai_message in ai_messages])

    num_trials = 3
    for _ in range(num_trials):
        quiz_questions = get_quiz_questions(topic, topic_information)
        if quiz_questions["valid"]:
            break
    display_quiz(quiz_questions)
    return {}
