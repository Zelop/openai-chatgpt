

def trim_messages(msg_list):
    word_counter = 0
    ret_list = []
    msg_list.reverse()
    for i in msg_list:
        word_counter += len(i['content'].split(' '))
        if word_counter > 1500:
            break
        ret_list.append(i)
    ret_list.reverse()
    return ret_list
