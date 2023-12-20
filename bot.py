from configg import *
from temp_word import *
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from models import User
import utils
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


    def delete_msg(self, id_msg, peer_id):
        self.vk_session.method('messages.delete', {'peer_id': peer_id, 'delete_for_all': 1, 'cmids': id_msg,
                                                   'group_id': peer_id - 2000000000})


    def save_msg(self, id, msg):
        msg_s = utils.get_user_by_msg(id, msg)
        msg_s.save()


    def delete_user(self,chat_id, user_id):
        self.vk_session.method("messages.removeChatUser", {'chat_id': chat_id, 'user_id': user_id})

        # def save
    def warns(self, id, chat_id, user_name):
        fwd_user = utils.get_user_ny_id(id)
        fwd_user.warns += 1
        fwd_user.save()
        self.sender(chat_id, id, f"{user_name}, вам выдано предупреждение!\nВсего предупреждений {fwd_user.warns}/5")
        if fwd_user.warns >= 5:
            self.delete_user(chat_id,id)

    def delete_warns(self, id, chat_id, user_name):
        fwd_user = utils.get_user_ny_id(id)
        fwd_user.warns -= 1
        fwd_user.save()
        self.sender(chat_id, id, f"{user_name}, у вас снято 1 предупреждение!\nВсего предупреждений {fwd_user.warns}/5")


    def question_gpt(self, text, chat_id, user_id):
        ans_text = ''
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "дай ответ на русском языке" + f"{text}"}],
            stream=True,
        )
        for message in response:
            ans_text += message
        ans_text = f"Ответ на вопрос: \n" + ans_text
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
                    user = utils.get_user_ny_id(user_id)
                    id_msg = event.object.message['conversation_message_id']
                    print(self.vk_session.method('users.get', {'user_id': user_id}))
                    user_name = self.vk_session.method('users.get', {'user_id': user_id})[0]['first_name']
                    print(event.object)
                    fwd = self.vk_session.method('messages.getByConversationMessageId', {
                        'conversation_message_ids': msg['conversation_message_id'],
                        'peer_id': msg['peer_id']
                    })['items'][0]

                    if 'reply_message' in fwd:
                        fwd = fwd['reply_message']
                    else:
                        fwd = None

                    print(fwd)
                    if fwd != None:
                        if user.vk_id == admin_id:
                            chek_id = fwd['from_id']
                            chek_name = self.vk_session.method('users.get', {'user_id': chek_id})[0]['first_name']
                            if text_msg == "кик":
                                self.delete_user(chat_id, chek_id)
                            elif text_msg == "варн":
                                self.warns(chek_id, chat_id, chek_name)
                            elif text_msg == "-варн":
                                self.delete_warns(chek_id, chat_id, chek_name)




                    if text_msg in temp_greeting:
                        self.sender(chat_id, user_id, f"{user_name}, привет!")

                    if list(set(word_text_msg) & set(abusive_language)) != []:
                        self.sender(chat_id, user_id, f"{user_name}, при мне так не выражайтесь!")
                        self.warns(user_id,chat_id,user_name)
                        self.delete_msg(id_msg, peer_id = msg['peer_id'])
                    if list(set(word_text_msg) & set(stop_word)) != []:
                        self.save_msg(user_id, text_msg)

                    if "/чат" in word_text_msg:
                        self.question_gpt(text_msg, chat_id, user_id)
                    if text_msg == "/help":
                        self.sender(chat_id, user_id, "Я бот для помощи в модерации беседы\n"
                                                      "Мои команды:"
                                                      "\n /help - список команд"
                                                      "\n /чат + (ваш вопрос) - для отправки вопроса к chat-gpt")