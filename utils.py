import openai
import config
import pickle

openai.api_key = config.api_key


def starting_role():
    sysrole = config.sysrole
    if not sysrole:
        sysrole = "You are a helpful assistant."
    return [{"role": "system", "content": sysrole}]


def trim_messages(msg_list):
    role = msg_list[0]["content"]
    word_counter = 0
    ret_list = []
    msg_list.reverse()
    for i in msg_list:
        word_counter += len(i['content'].split(' '))
        if word_counter > 1500:
            break
        ret_list.append(i)
    ret_list.append({"role": "system", "content": role})
    ret_list.reverse()
    return ret_list


async def get_text_from_audio(audiofile):
    audio_file = open(audiofile, "rb")
    if config.translate_voice:
        return openai.Audio.translate("whisper-1", audio_file)
    else:
        return openai.Audio.transcribe("whisper-1", audio_file)


async def clear_db(update):
    with open("chats/" + str(update.message.chat_id) + ".dump", 'wb') as pfile:
            pickle.dump(starting_role(), pfile)
    print("Db " + str(update.message.chat_id) + " cleaned up.")


async def send_chat_msg(update, audiotext=None):
    if not audiotext:
        msg = update.message.text
    else:
        msg = audiotext
    with open("chats/" + str(update.message.chat_id) + ".dump", 'rb') as pfile:
        data = pickle.load(pfile)
    data.append({"role": "user", "content": msg})
    response = openai.ChatCompletion.create(
            model=config.model,
            messages=data
        )
    data.append(response["choices"][0]["message"])
    print(response["usage"]["total_tokens"], "tokens sent.")
    if response["usage"]["total_tokens"] > 3500:
        print("Getting close to the 4096 token limit. Trimming conversation to 1500 words (2048 tokens approx).")
        data = trim_messages(data)
    with open("chats/" + str(update.message.chat_id) + ".dump", 'wb') as pfile:
        pickle.dump(data, pfile)

    return response["choices"][0]["message"]["content"]
