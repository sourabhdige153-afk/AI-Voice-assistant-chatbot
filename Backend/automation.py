from AppOpener import close, open as appopen  #import functions to open and close apps
from webbrowser import open as webopen        #import webbrowser to open webbrowser
from pywhatkit import search, playonyt        # for Google search and Youtube playback
from bs4 import BeautifulSoup                 # Beautifulsoup for parsing HTML Content
# from rich import print                        # Import ricg for styled console output
from groq import Groq                         #import groq for AI Chat Functionality
import webbrowser                             # Webbrowser for opening URLs
import subprocess                             # Subprocess for interacting with system
import requests                               # Import request for making HTTP rquests
import keyboard                               # import keyboard for keyboard-related actions
import os                                     # to perform system functionality
from dotenv import load_dotenv                # to load values from .env file
import asyncio                                # To perform multiple task at a single time
load_dotenv()

Username = os.getenv("Username")
GroqApiKey = os.getenv("GroqAPIKey")

classes = ["zCubwf","hgKElc", "LTKOO", "sY7ric","Z0LcW", "gsrt vk_bk FzWSb YmPhnf", "'pclquee","tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
# user_input ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

client = Groq(api_key=GroqApiKey)

# professional responses for user interactions 
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else i can help uou with.",
    "I'm at your service for my additional questions or support you may need-don't hesitate to ask."
]

messages = []

systemChatBot = [{"role": "system", "content": f"Hello , I am {Username}, You're a content writer. You have to write content like letter"}]

def GoogleSearch(Topic):
    search(Topic)   # Use pywhatkit's to perform Google Search
    return True

def content(Topic):

     #Notepad function to open file in notepad
    def OpenNotePad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, File])  #Open the file in notepad

    #Function to generate content using AI Chatbot
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f'{prompt}'}) 

        completion = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages=systemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "") # Remove unwanted tokens fron the response

        messages.append({"role": "assistant", "content": Answer})

        return Answer
    
    Topic: str = Topic.replace("Content ", "")  #Remove "Content " from the topic
    ContentByAI = ContentWriterAI(Topic)        # Generate contntent using ai

    # Save the genetrated content to a text file.
    with open(rf"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)             #write the content to the file

    OpenNotePad(rf"Data/{Topic.lower().replace(' ', '')}.txt")  # open the file in notepad

    return True

def YoutubeSearch(Topic):
    url = f"https://www.youtube.com/results?search_query={Topic}" # Constructed youtuve search url
    webbrowser.open(url)
    return True


def PlayYoutube(query):
    playonyt(query)      # the playwhatkit's playonyt function to play
    return True

# PlayYoutube("saiyara")

#Function to open application or releavent webpage
def OpenApp(app, sess=requests.Session()):

    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  #Attempt to open the app
        return True
    
    except:
        #Nested function to extrxt links from html content
        print("error occured, fetching html link")
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # find releaventv links
            return [link.get('href') for link in links]      #return the links
        
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"  #construct the Google Search URL
            headers = {"User-Agent": useragent}              # used predefined user agent
            response = sess.get(url, headers=headers,allow_redirects=True)         #Perform the get request

            if response.status_code == 200:
                print("Response code: ", response.status_code)
                print("Resonse text: ",response)
                return response.text
            else:
                print("Falied to retrieve search results.")
            return None
        

        html = search_google(app)           #perform the google search
        links = extract_links(html)

        if links:
            link = links[0]   #extract the first link fron the search results
            webopen(link)                   #Open the link in a web browser

        return True


#Function to close an application
def closeapp(app):

    if "chrome" in app:
        pass                  #Skip if the app is chrome bcz selenium drive running our html file chrome, if we close chrome then that html paage will also get close
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app
            return True
        except:
             return False

# closeapp("settings")
#Function to execute syetem level command
def system(command):

    #nested function to mute the system volume
    def mute():
        keyboard.press_and_release("volume mute")
    
    #nested function to unmute the system volume
    def unmute():
        keyboard.press_and_release("volume mute")

    # Nested function to increase voulme
    def volume_up():
        keyboard.press_and_release("volume up")

    # Nested function to decrease voulme
    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True


#asynchronous function to translate and execute user commands (to perform multiple tasks at single go)
async def translateAndExecute(commands: list[str]):
    print("*********************")
    funcs = []     # list to store asnchronous tasks

    for command in commands:

        if command.startswith("open "):   #Handle open commands

            if "open it" in command:       #ignore 'open it' commands
                pass
            
            if "open file" == command:     #ignore 'open file' commands
                pass

            else:
                print("Flow is herr")
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # it weill schedule app opening
                funcs.append(fun)

        elif command.startswith("general "):  # placeholder for general command
            pass

        elif command.startswith("realtime "):  #Placholder for real time commands
            pass

        elif command.startswith("close "):  # handle close commands
            fun = asyncio.to_thread(closeapp, command.removeprefix("close "))  #Schedule app closing
            funcs.append(fun)

        elif command.startswith("play "):     #Handle play commands
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # Schedule youtube playback
            funcs.append(fun)
        
        elif command.startswith("content "):  #Handle 'content' commands
            fun = asyncio.to_thread(content, command.removeprefix("content "))   #schedule content commands 
            funcs.append(fun)

        elif command.startswith("google search "): # Handle Google search commands
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) #Schedule google search
            funcs.append(fun)
        
        elif command.startswith("youtube search"):  #Handle YouTube Serch
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search"))  #schedule youtube search
            funcs.append(fun)

        elif command.startswith("system "):   #Handle system sommands
            fun = asyncio.to_thread(system, command.removeprefix("system "))          # schedule system commands
            funcs.append(fun) 

        else:
            print(f"No Functions Found for {command}")

    results = await asyncio.gather(*funcs) #Excecute all tasks concurrently

    for result in results:  # process the results
        if isinstance(result, str):
            yield result
        else:
            yield result


#Asynchronous function to automate command execution
async def Automation(commands: list[str]):

    async for result in translateAndExecute(commands):  #translate and execute commands
        pass

    return True

if __name__ == '__main__':
    asyncio.run(Automation(["open notepad", "play haye me mar hi jawa","open settings"]))
    asyncio.run(Automation(["close notepad", "close settings","close google chrome"]))

    











    

        

    








