import datetime
from models import User, Msg, Imp_Msg

def get_user_ny_id(user_id):
    try:
        return User().get(vk_id = user_id)
    except:
        User(
            vk_id = user_id,
            warns = 0
        ).save()
        return User().get(vk_id = user_id)

def get_user_by_msg(user_id, msg):
    Msg(
        vk_id = user_id,
        msg = msg
    ).save()
    return Msg().get(vk_id=user_id)

def set_imp_msg(user_id, msg):
    Imp_Msg(
        vk_id = user_id,
        msg = msg
    ).save()
    return Imp_Msg().get(vk_id=user_id)

def get_all_imp_msgs():
    all_msgs = Imp_Msg.select().order_by(Imp_Msg.timestamp)
    return '\n'.join([f"{msg.id}:   {msg.msg.replace('+важное', '')}" for msg in all_msgs])

def delete_imp_msg_by_id(msg_id):
    try:
        msg = Imp_Msg.get_by_id(msg_id)
        msg_text = msg.msg
        msg.delete_instance()
        print(f"Сообщение с DB ID {msg_id} и текстом '{msg_text}' успешно удалено.")
    except Imp_Msg.DoesNotExist:
        print(f"Сообщение с DB ID {msg_id} не найдено.")
