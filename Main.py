from Frontend.GUI import (
GraphicalUserInterface,
setAssistantStatus,
showTextToScreen,
tempDirectoryPath,
setMicrophoneStatus,
AnswerModifier,
queryModifier,
getMicrophoneStatus,
getAssistantStatus)
from  Backend.model import firstLayerDMM
from Backend.realtime_search_engine import realtimeSearchEngine
from Backend.automation import Automation
from Backend.speech_to_text import speechRecognition
from Backend.chatbot import chatbot
from Backend.text_to_speech import textToSpeech
from dotenv import load_dotenv
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
load_dotenv()

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you? 
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''

subprocess = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def showDefaultChatIfNoChats():
    File = open(r"Data/ChatLog.json", "r", encoding="utf-8")
    if len(File.read()) < 5:
        with open(tempDirectoryPath('Database.data'), 'w', encoding="utf-8") as file:
            file.write("")
        
        with open(tempDirectoryPath('Responses.data'), "w", encoding="utf-8") as file:
            file.write(DefaultMessage)

def readChatLogJson():
    with open(f"Data\ChatLog.json", 'r', encoding="utf-8") as file:
        chat_data = json.load(file)
    return chat_data

def chatLogIntegration():
    json_data = readChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog  += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant {entry['content']}\n"
    
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(tempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))

def showChatsOnGUI():
    File = open(tempDirectoryPath("Database.data"), "r", encoding="utf-8")
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split("\n")
        result = "\n".join(lines)
        File.close()
        File = open(tempDirectoryPath("Responses.data"), "w", encoding="utf-8")
        File.write(result)
        File.close()

def initialExecution():
    setMicrophoneStatus("False")
    showTextToScreen("")
    showDefaultChatIfNoChats()
    chatLogIntegration()
    showChatsOnGUI

initialExecution()

def mainExcecution():
    
    TaskExecution = False
    ImageExecution = False
    ImaageGenerationQuery = ""

    setAssistantStatus("Listening ... ")
    Query = speechRecognition()
    print(f"query: {Query}")
    showTextToScreen(f"{Username} : {Query}")
    setAssistantStatus("Thinking ... ")
    Decision = firstLayerDMM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    general = any([i for i in Decision if i.startswith("general")])
    realtime = any([i for i in Decision if i.startswith("realtime")])
    
    merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    

    for queries in Decision:
        if "generate " in queries:
            ImaageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution == True

    if ImageExecution == True:

        with open(r"Frontend/Files/ImageGeneration.data", "w") as file:
            file.write(f"{ImaageGenerationQuery},True")

        try:
            p1 = subprocess.Popen(['python', r'Backend/image_generation.py'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  stdin=subprocess.PIPE, shell=False)
            subprocess.append(p1)

        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if general and realtime or realtime:
        setAssistantStatus("Searching ... ")
        Answer = realtimeSearchEngine(queryModifier(merged_query))
        showTextToScreen(f"{Assistantname} : {Answer}")
        setAssistantStatus("Answering ... ")
        textToSpeech(Answer)
        return True
    
    else:
        for queries in Decision:
             
              if "general" in queries:
                  setAssistantStatus("Thinking ... ")
                  queryfinal = queries.replace("general ", "")
                  Answer = chatbot(queryModifier(queryfinal))
                  showTextToScreen(f"{Assistantname} : {Answer}")
                  setAssistantStatus("Answering ... ")
                  textToSpeech(Answer)
                  return True
              
              elif "realtime" in queries:
                  setAssistantStatus("Searching ... ")
                  queryfinal = queries.replace("realtime ", "")
                  Answer = realtimeSearchEngine(queryModifier(queryfinal))
                  showTextToScreen(Answer)
                  setAssistantStatus("Answering ... ")
                  textToSpeech(Answer)
                  return True
              
              elif "exit" in queries:
                  queryfinal = "Okay, Bye"
                  Answer = chatbot(queryfinal(queryfinal))
                  showTextToScreen(f"{Assistantname} : {Answer}")
                  setAssistantStatus("Answering ... ")
                  textToSpeech(Answer)
                  setAssistantStatus("Answering ... ")
                  os._exit(1)

def FirstThread():
    
    while True:

        currentStatus = getMicrophoneStatus()

        if currentStatus == "True":
            mainExcecution()
        
        else:
            AIStatus = getAssistantStatus()

            if "Available ... " in AIStatus:
                sleep(0.1)

            else:
                setAssistantStatus("Available ... ")


def SecondThread():

    GraphicalUserInterface()


if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()





