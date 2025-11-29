from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# env_vars = dotenv_values(".env")

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqAPIKey = os.getenv("GroqAPIKey")

client = Groq(api_key = GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role":"system", "content": System}
]

try:
    with open(f"Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(f"Data/ChatLog.json", "w") as f:
        dump([],f,indent=4)

def realtime_information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed.\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"

    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    no_empty_lines = [line for line in lines if line.strip()] #line.strip() will remove empty lines
    modified_answer = '\n'.join(no_empty_lines)
    return modified_answer

def chatbot(query):

    try:
        with open(r"Data/ChatLog.json","r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{query}"})

        comletion = client.chat.completions.create(
            model = "openai/gpt-oss-120b",
            messages=SystemChatBot + [{"role": "system", "content": realtime_information()}] +messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in comletion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>","") #clean up unwanted token fron the response

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error occured: {e}")
        with open(r"Data/ChatLog.json","w") as f:
            dump([],f, indent=4)
            
        return chatbot(query)

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(chatbot(user_input))






    
