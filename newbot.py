import json
from difflib import get_close_matches
from googleapiclient.discovery import build
# Your Google API key and Custom Search Engine ID
API_KEY = "AIzaSyCmy2LTYKc9fPlQfo_9t3ogn_2UqFWUSKI"
CSE_ID = "12cbc19a3c4bd427a"

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
        return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def search_google(query: str, api_key: str, cse_id: str) -> str:
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=1).execute()
    if 'items' in res:
        return res['items'][0]['snippet']
    return "Sorry, I couldn't find any relevant information."

def get_answer_for_question(question: str, knowledge_base: dict) -> str:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return "Sorry, I don't have an answer for that at the moment."

def find_best_match(user_input: str, questions: list[str]) -> str:
    matches = get_close_matches(user_input, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_from_google(user_input: str) -> str:
    return search_google(user_input, API_KEY, CSE_ID)

def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit":
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            new_answer: str = get_answer_from_google(user_input)
            print(f"Bot: {new_answer}")

            confirmation = input('Is this the answer you were looking for? (Yes/No): ')
            if confirmation.lower() == "yes":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank you for teaching me!")

if __name__ == "__main__":
    chat_bot()
