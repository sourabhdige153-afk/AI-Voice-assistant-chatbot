import pygame  # Imported pygame library for handling audio playback
import random
import asyncio   # imported asyncio for asynchronous operations
import edge_tts  # Imported edge_tts for tect to speech functionality
import os
from dotenv import load_dotenv
load_dotenv()

AssistantVoice = os.getenv("AssistantVoice")

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(Text) -> None:
    file_path = r"Data/speech.mp3" # Defined the path where the speech file will be saved
    
    if os.path.exists(file_path):  # Checking if file is alredy exist
        os.remove(file_path)#If It exist, remove it to avoid overwriting errors 
        
    #created communication object to generate speech
    communicate = edge_tts.Communicate(Text, AssistantVoice, pitch='+5Hz', rate='+13%')

    await communicate.save(r"Data/speech.mp3") # it save the generated speech as an mp3 file

# Function to manage text to speech functionality
def TTS(text, func=lambda r=None: True):
    while True:

        try:
            #Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(text))

            # Initialized pygame mixture for audio playback
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data/speech.mp3")
            pygame.mixer.music.play()  # Play the audio

            # loop unitil the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:  # checking the function returns false
                    break
                pygame.time.Clock().tick(10) # Limit the loop to 10 ticks per second

            return True # Returning true if the audio played successfully
        
        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                 # Call the provided function with False to signal the end of TTS
                func(False)
                pygame.mixer.music.stop() #Stop the audio playback
                pygame.mixer.quit()       # Quit the pygame mixer

            except Exception as e:
                print(f"Error in finally block: {e}")

#It is for if the text is so long (More than 4 sentences and 250 characters), then it will take only first two sentence from text and one random response from responses to speak
def textToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".") # Split the text by periods(.) into a list of sentences

    # List of predefined responses for cases where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If the text is very long(More than 4 sentences and 250 characters), add a random message
    if len(Data) >4 and len(Text) >=250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)

    #Otherwise , jurt play the whole text    
    else:
        TTS(Text, func)

if __name__ == '__main__':
    while True:
        TTS(input("Enter the text: "))








