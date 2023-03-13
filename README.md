# openai-chatgpt

[OpenAI Documentation](https://platform.openai.com/docs/guides/chat)

Quick implementation of ChatGPT in Python.
Includes Telegram bot and OpenAI Whisper API for using Telegram voice messages.

Image generation is still a WIP.

Rename config.py.example to config.py and set it up.

**Note**: This is a terrible implementation, potentially unsafe, it works for my use case, but do **not** use this in any production environment. 
You'd also need to set up a proper database for storing chats and make sure it complies with privacy regulations.


### Usage
```
pip install -r requirements.txt  # Use a venv
python console_chat.py  # For chatgpt in console
python telegram_bot.py  # For the telegram bot
```
