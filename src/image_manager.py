from openai_connect import OpenaiConnect
import requests
import os

class Painter:
    def __init__(self):
        self.manager = OpenaiConnect("dall-e-3")

    def make_image(self, prompt):
        """Make an image and save it locally. Returns the path to the image."""
        url = self.manager.make_image(prompt)
        response = requests.get(url)
        with open("art/local_image.jpg", "wb") as f:
            f.write(response.content)
        print("Image successfully saved locally!")
        return "art/local_image.jpg"

    def make_image_and_open(self, prompt):
        """Make an image and open it locally. Windows only."""
        url = self.manager.make_image(prompt)
        response = requests.get(url)
        with open("art/local_image.jpg", "wb") as f:
            f.write(response.content)
        print("Image successfully saved locally!")

        try:
            if(os.path.exists("art/local_image.jpg")):
                # Open the image windows only
                os.system("start art/local_image.jpg")
            else:
                print("Image not found.")
        except Exception as e:
            print(f"Error opening image: {e}")
            
if __name__ == "__main__":
    gav_art = Painter()
    gav_art.make_image_and_open("A painting of a hamster training to become a surfing master.")