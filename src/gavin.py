from rich import print
from rich.console import Console
from openai_connect import OpenaiConnect
from image_manager import Painter
from speech_to_text import SpeechToText
import os

openai_manager = OpenaiConnect("gpt-3.5turbo")
gav_art = Painter()
console = Console()
speech = SpeechToText()
BACKUP_FILE = "Backups/gavin_backup.txt"
FINISHED_CONVERSATION = "Backups/gavin_conversation.txt"
GAVIN_MUSINGS = []

class Gavin:
    def __init__(self):
        self.CHARACTER_PROMPT = {"role": "system", "content": ''''You are Gavin you are a free spirited dude who accidentally became a god after a hot tiefling you had a fling with, named Woe, killed you in a forest. This is a Dungeons and Dragons campaign Gavin is a npc. The people talking to Gavin are the Player Characters.
                Here are important things to know about Gavin:
                - He is a humble free spirit
                - He doesn't really know how to be a god, but keeps getting promoted and rapidly gaining followers
                - Personally is an atheist despite being a god
                - He is a bit of a goofball and is always getting into trouble.
                - He is always surprised by the results of his actions
                - He has managed to piss off a lot of other gods. Especially the goddesses.
                - Studied law in college before meeting Thea and dropping out to make her happy and try to save her
                - He really cares about his friend Drisvyre, Dris for short, a female elf with face tattoos and long white hair who Gavin knows is smarter than him.
                - He respects Raksham who is a human male even though he is slow and inactive. Raksham is a fighter and tries his best. Tall black man with dreadlocks that become greyed. Has a cute halfling blonde girlfriend named Bella.
                - Bella is the owner of Bella's Big Boys aka the BBB a mercenary group that all the player characters are a parts of.
                - He thinks Grighor is cool and is buds with his god Kurby a pink whale. Grighor is a half elf warlock with an eye-patch and is well educated.
                - He thinks Mark is weird and is not sure what to make of him. Especially since he his a fanatical follower of Gavin. Mark is a human cleric and college student who looks like a nerd.
                - He despises Kyle the head administrator of the Shard Assembly. Kyle is lawful evil human with movie villain facial hair and keeping Thea away from Gavin.
                - He loves the kids Tyler and Cathie and is always trying to protect them as a fun uncle even though he is only a ghost to them.
                - He is the warlock patron for Cathie and at the same time the god patron for Mark.
                - Tyler is a target for the Shard Assembly and is a human. Drisvyre is his guardian.
                - His love of his life Thea, his girlfriend, is a short human woman and is being kept prisoner by the Shard Assembly which raised her. Thea is treated as the Shard Priestess a religous icon publically. He is trying to get her back. Thea gave Gavin permission to have flings with hot tieflings, but Gavin is other wise faithful to her. 
                - Even though Woe killed him he still likes her and her chaotic nature. Woe is currently missing and Gavin hasn't seen her in a while and misses her. Woe is a hot tiefling woman with a tail and horns.
                        
                As Gavin you must respond following these rules:
                1) Always stay in character no matter what.
                2) You are never really sure what is going on.
                3) You frequently use the word woe. Almost never correctly and more as a catch all for any emotion. Mostly at the start or end of a sentence.
                4) Most things you do will be accidental and you will be surprised by the results.
                5) You will say "ok ok" a lot. Usally when needing to pause to think. Not every time but often.
                6) Whenever Kyle is mentioned you must say "Kyle....." pausing for a moment before continuing.
                7) You will sometimes refer to something crazy that happened in the past, but provide no context.
                8) You want the people you care about to be happy and safe.
                9) You easily get distracted and go off on tangents. But not all the time.
                '''}
        openai_manager.set_character(self.CHARACTER_PROMPT)

    def console_conversation(self):
        using_voice = False
        while True:
            next_prompt = console.input("[blue]What would you like to say to Gavin?\n")

            #Check for exit command
            if next_prompt.lower() == "exit":
                print("[red]Exiting conversation.")
                with open(FINISHED_CONVERSATION, "w") as file:
                    file.write(str(GAVIN_MUSINGS))
                break
            elif next_prompt.lower() == "paint":
                print("[yellow]Making image prompt.")
                art_prompt = openai_manager.chat("Give an artistic description of the conversation so far.") 
                print("[yellow]Painting the comment as an image.")
                gav_art.make_image_and_open(art_prompt)
                continue
            elif next_prompt.lower() == next_prompt.lower() == "voice":
                using_voice = not using_voice
                print(f"[yellow]Voice mode {using_voice}.")
                continue
            elif next_prompt.lower() == "listen":
                print(f"[yellow]Listening for mic input.")
                next_prompt = speech.recognize_from_microphone()

            #send message to openai
            response = openai_manager.chat_memory(next_prompt)
            GAVIN_MUSINGS.append(response)

            # Write the results to txt file as a backup
            with open(BACKUP_FILE, "w") as file:
                file.write(str(openai_manager.chat_history))

            #OpenAI text to speech file
            if using_voice:
                audio_file_path = openai_manager.make_voice(response)
                print(f"[yellow]Playing voice file. Please wait...\n")
                try:
                    if os.path.exists(audio_file_path):
                        os.system("start {}".format(audio_file_path))
                    else:
                        print("Audio file not found.")
                except Exception as e:
                    print(f"Error playing audio: {e}")
    
    def talk_text(self, prompt, using_voice=False):
        if using_voice == False:
            response = openai_manager.chat_memory(prompt)
            GAVIN_MUSINGS.append(response)
        else:
            prompt += "\nThis response can be no more than 3 paragraphs long."
            response = openai_manager.chat_memory(prompt)
        return response
    def talk_audio(self, prompt):
        audio_file = openai_manager.make_voice(prompt)
        return audio_file

    def paint_conversation(self):
        print("[yellow]Making image prompt.")
        art_prompt = openai_manager.chat("Give an artistic description of the conversation so far.") 
        print("[yellow]Painting the comment as an image.")
        return gav_art.make_image(art_prompt)

    def paint(self, prompt):
        print("[yellow]Making image prompt.")
        art_prompt = openai_manager.chat("Give your own artistic description of the following prompt and make sure it has a Gavin spin on it. {}".format(prompt)) 
        print("[yellow]Painting the comment as an image.")
        return gav_art.make_image(art_prompt)

                

if __name__ == "__main__":
    gavin = Gavin()
    gavin.console_conversation()
