from config import *
from temp_word import *
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import re
from vk_api.longpoll import VkLongPoll, VkEventType
import g4f


class MyLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


class VkBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=tok)
        self.longpoll = MyLongPoll(self.vk_session, 223900454)

    def sender(self, id, user_id, text):
        self.vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})

    def delete(self, id_msg, peer_id):
        self.vk_session.method('messages.delete', {'peer_id': peer_id, 'delete_for_all': 1, 'cmids': id_msg,
                                                   'group_id': peer_id - 2000000000})

    def question_gpt(self, text, chat_id, user_id):
        ans_text = ''
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "дай ответ на русском языке" + f"{text}"}],
            stream=True,
        )
        for message in response:
            ans_text += message
        ans_text = f"Ответ на вопрос: " + ans_text
        self.sender(chat_id, user_id, ans_text)
    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    chat_id = event.chat_id
                    msg = event.object.message
                    text_msg = msg['text'].lower()
                    word_text_msg = text_msg.split()
                    user_id = msg['from_id']
                    id_msg = event.object.message['conversation_message_id']
                    user_name = self.vk_session.method('users.get', {'user_id': user_id})[0]['first_name']
                    print(event.object)

                    if text_msg in temp_greeting:
                        self.sender(chat_id, user_id, f"{user_name}, привет!")

                    if list(set(word_text_msg) & set(abusive_language)) != []:
                        self.sender(chat_id, user_id, f"ЭЭЭЭЭЭЖЭЭ")
                        # self.delete(id_msg, peer_id = msg['peer_id'])

                    if "/stats" in word_text_msg:
                        self.sender(chat_id, user_id, f"{user_name}, всего {msg['conversation_message_id']} сообщений в этом чате!)")

                    if "/вопрос" in word_text_msg:
                        self.question_gpt(text_msg, chat_id, user_id)



if __name__ == '__main__':
    VkBot().run()
