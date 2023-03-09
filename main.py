import config
import openai
openai.api_key = config.api_key

print("Write exit at any time to end the conversation")

sysrole = input("Insert the system role: (empty for it to be an assistant.)")
if not sysrole:
    sysrole = "You are a helpful assistant."
messages = [{"role": "system", "content": sysrole}]

token_usage = 0

keep_running = not (sysrole.lower() == "exit")

while keep_running:
    msg = input("You say: ")
    messages.append({"role": "user", "content": msg})

    if msg.lower() != "exit":
        response = openai.ChatCompletion.create(
            model=config.model,
            messages=messages
        )
        messages.append(response["choices"][0]["message"])
        print("ChatGPT says:", response["choices"][0]["message"]["content"])
        token_usage += response["usage"]["total_tokens"]
        if config.display_token_usage:
            print(f'{response["usage"]["total_tokens"]} tokens used.')
    else:
        keep_running = False
        print(f'Total of {token_usage} tokens used for a total cost of ${(0.002/1000) * token_usage}')
