from openai import OpenAI
from dotenv import dotenv_values
from rich import print
import tiktoken
from datetime import datetime

# Load variables from .env file
env_vars = dotenv_values(".env")
key = env_vars["OPENAI_API_KEY"]

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
  """Returns the number of tokens used by a list of messages.
  Copied with minor changes from: https://platform.openai.com/docs/guides/chat/managing-tokens """
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      print(f"Number of tokens: {num_tokens}")
      return num_tokens
  except Exception:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
      #See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


class OpenaiConnect:
  def __init__(self, model="gpt-3.5-turbo"):
    self.chat_history = []
    self.model = model
    try:
      self.client = OpenAI(api_key=key)
    except TypeError:
      exit("Error: API key not found")

  def set_character(self, character_prompt):
    self.CHARACTER_PROMPT = character_prompt
    self.chat_history.append(self.CHARACTER_PROMPT)

  def chat(self, prompt=""):
    #Add in a validation check for the prompt
    chatting = []
    chatting.append(self.CHARACTER_PROMPT)
    chatting.append({"role": "user", "content": prompt})
    if num_tokens_from_messages(chatting) > 8000:
      print("The length of this chat question is too large for the GPT model")
      return

    completion = self.client.chat.completions.create(
      model=self.model,
      messages=chatting,
      temperature=1.1
    )
    response = completion.choices[0].message.content
    print(f"[green]\n{response}\n")
    return response
  
  def chat_memory(self, prompt=""):
    #Add in a validation check for the prompt
    self.chat_history.append({"role": "user", "content": prompt})
    if num_tokens_from_messages(self.chat_history) > 8000:
      self.chat_history.pop(1)
      print("The length of this chat question is too large for the GPT model")
      return
    completion = self.client.chat.completions.create(
      model=self.model,
      messages=self.chat_history,
      temperature=1.1
    )
    response = completion.choices[0].message.content
    print(f"[green]\n{response}\n")
    self.chat_history.append({"role": "assistant", "content": response})
    return response
  
  def make_image(self, prompt="", number_of_images=1):
    #Add in a validation check for the prompt
    completion = self.client.images.generate(
      model=self.model,
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=number_of_images
    )
    response = completion.data[0].url
    return response
  
  def make_voice(self, prompt=""):
    #Add in a validation check for the prompt
    completion = self.client.audio.speech.create(
      model= "tts-1",
      voice="echo",
      input=prompt
    )
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"Audio/voice_{current_datetime}.opus"
    completion.stream_to_file(file_name)
    return file_name
    