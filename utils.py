import datetime
from models import User, Msg

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