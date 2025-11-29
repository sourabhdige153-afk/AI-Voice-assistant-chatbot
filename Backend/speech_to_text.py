from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
load_dotenv()
import mtranslate as mt

inputLanguage = os.getenv("InputLanguage") 

# Html code for speech recognition interface
htmlcode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables
htmlcode = str(htmlcode).replace("recognition.lang = '';", f"recognition.lang= '{inputLanguage}';")

# Write modified html code to a file
with open(r"Data/voice.html","w") as f:
    f.write(htmlcode)

# it will get the current working directory
currentdir = os.getcwd()

# Generate the file path for the HTML file
Link = f"{currentdir}/Data/voice.html"
print("link: ",Link)

# Set chrome options for the webdriver
chrome_options = Options()
user_input = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_input}")
chrome_options.add_argument(f"--use-fake-ui-for-media-stream")
chrome_options.add_argument(f"--use-fake-device-for-media-stream")
# chrome_options.add_argument(f"--headless=new")

#Initialize the Chrome webdriver using the ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


TempDirPath = f"{currentdir}/Frontend/Files"
def setAssistantStatus(status):
    with open(f"{TempDirPath}/Status.data", "w", encoding='utf-8') as file:
        file.write(status)


# Function is for adding sybmbol at last to the query
def queryModifier(query):
    new_query = query.lower().strip()
    query_words = new_query.split()
    question_words = ["how","what","who","where","when","why","which","whose","whom","can you","what's","where's","how's"]

    #Check if the query is a question and add a question mark if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # Add a period if the query is not a question 
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()


#Function to translate text into english using mtranslate library
def universalTransalate(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()


#Function to perform speech recognition using the WebDriver
def speechRecognition():
    # open the html file in browser
    # driver.get("file:///" +Link)
    driver.get("file:///" + Link.replace("\\", "/"))

    # Added wait for wating to get html elements to fetch
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "start"))).click()

    # start speech recognition by clicking the start button
    # driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            #Get the recognized text from the HTML output element
            Text = driver.find_element(by=By.ID, value="output").text 

            if Text:
                # Stop recognition by clicking the stop button.
                driver.find_element(by=By.ID, value="end").click()   

                #If the input language is english, return the modified query
                if inputLanguage.lower() == "en" or "en" in inputLanguage.lower(): 
                    return queryModifier(Text)
                else:
                    #If the input language is not english,translate the text and return it.
                    setAssistantStatus("Translating...")
                    return queryModifier(universalTransalate(Text))
        except Exception as e:
            pass

if __name__ == "__main__":
    while True:
        Text = speechRecognition()
        print(Text)






