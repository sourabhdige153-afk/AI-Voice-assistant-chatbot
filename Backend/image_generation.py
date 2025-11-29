import asyncio
from random import randint
from PIL import Image
import requests
import os                                     # to perform system functionality
from dotenv import load_dotenv   
load_dotenv()
from time import sleep

HuggingFaceAPIKey = os.getenv("HuggingFaceAPIKey")

def open_image(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    Files = [f"{prompt}{i}.jpg" for i in range(1,5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}

#async function to send a query to hugging face api
async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers , json=payload)
        print(f"Resonse: {response.content}")
        return response.content
    except Exception as e:
        print(f"Excepyion occures: {e}")


#aync function to generate images based on the givrn prompt
async def generate_images(prompt: str):
    tasks = []

    #Create 4 images generation tasks
    for _ in range(4):
        payload ={
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
        }

        task = asyncio.create_task(query(payload))
        tasks.append(task)
    
    #wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        with open(rf"Data/{prompt.replace(' ','_')}{i + 1}.jpg", 'wb') as f:
            f.write(image_bytes)


# Wrapper function to generate and open image
def GnerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the asynch image generation
    open_image(prompt)                    # open the generted image


# Main loop to monitor fr image generation requests
while True:

    try:
        # Read the prompt and status from the ImageGeneration.data file
        with open(f"Frontend/Files/ImageGeneration.data", "r") as f:
            data= f.read()

        prompt, status = data.split(",")

        # If the status indicates an image generation request
        if status == "True":
            print("Generating images.....")
            Imagestatus = GnerateImages(prompt=prompt)

            # Reset the status in the file after generating images
            with open(f"Frontend/Files/ImageGeneration.data", "w") as f:
                print("opening file to change data")
                f.write("False,False")
                break                     # Break the while loop after processing the request of imege generation
        else:
            sleep(1)    # Wait for 1 second before checking again

    except:
        pass

            



