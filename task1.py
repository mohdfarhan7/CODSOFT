import re

def chatbot(user_input, rules):
    for pattern, response in rules.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return response

    return "I'm sorry, I didn't understand that. Can you please rephrase?"


user_rules = {
    r"hello|hi|hey": "Hello! How can I assist you today?",
    r"how are you|how's it going": "I'm doing well, thank you! How about you?",
    r"what is your name|who are you": "I am a chatbot. You can call me ChatBot.",
    r"goodbye|bye": "Goodbye! Have a great day!",
}

while True:
    user_input = input("User: ")
    response = chatbot(user_input, user_rules)
    print("ChatBot:", response)