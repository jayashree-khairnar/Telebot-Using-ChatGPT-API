from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import sys

class Reference:
    """
    A class to store previous response from the chatGPT API.
    """
    def __init__(self) -> None:  
        self.response = ""   

# Load environment variables
load_dotenv()

# Set up the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a reference object to store the previous response
reference = Reference()

# Set up the telegram token 
TOKEN = os.getenv("TOKEN")

# Model used in chatGPT
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """
    A function to clear the previous conversation and context.
    """
    reference.response = ""


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    A handler to welcome the user and clear past conversations and text.
    """
    clear_past()
    await message.reply("Hello! \nI'm chatGPT Telegram Bot. \nHow can I assist you?")


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear past conversation and context.
    """ 
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the menu.
    """
    help_command = """
    Hi there, I'm chatGPT Telegram Bot! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu
    """

    await message.reply(help_command)

@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")  # user's message
    response = openai.ChatCompletion.create(    # chat conversation using OpenAI  
        model = MODEL_NAME,
        messages = [
            # whatever response getting from the chatGPT, storing it in a Reference class
            {"role" : "assistant", "content" : reference.response}, # role assistant
            {"role" : "user", "content" : message.text} # user query
        ]
    )

    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}") # output from chatGPT
    # for each execution it'll create different id's
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)