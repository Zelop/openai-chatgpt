import config
import openai
from utils import trim_messages
from colorama import Fore
from rich.console import Console
from rich.markdown import Markdown

console = Console()
openai.api_key = config.api_key

print("Write exit at any time to end the conversation")

sysrole = input("Insert the system role (empty for it to be an assistant): ")
if not sysrole:
    sysrole = "You are a helpful assistant."
messages = [{"role": "system", "content": sysrole}]

token_usage = 0
keep_running = not (sysrole.lower() == "exit")

while keep_running:
    print(Fore.CYAN, "You say:", Fore.BLUE, end='')
    msg = input()
    messages.append({"role": "user", "content": msg})

    if msg.lower() != "exit":
        response = openai.ChatCompletion.create(
            model=config.model,
            messages=messages
        )
        messages.append(response["choices"][0]["message"])
        print(Fore.RESET, "ChatGPT says:", Fore.YELLOW, end='')
        console.print(Markdown(response["choices"][0]["message"]["content"]))
        last_req_tokens = response["usage"]["total_tokens"]
        token_usage += last_req_tokens

        # Temporary fix to avoid going over 4096 tokens.
        if last_req_tokens > 3500:
            print(Fore.RED, "Getting close to the 4096 token limit. Trimming conversation to 1500 words (2048 tokens aprox).")
            messages = trim_messages(messages)

        if config.display_token_usage:
            print(Fore.MAGENTA, last_req_tokens, 'tokens used.')
    else:
        keep_running = False
        print(Fore.MAGENTA, f'Total of {token_usage} tokens used for a total cost of ${(0.002/1000) * token_usage}')
        print(Fore.RESET)
