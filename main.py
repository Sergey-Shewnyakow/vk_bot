from bot import VkBot
from dotenv import load_dotenv

if __name__ == '__main__':
    while 1:
        try:
            VkBot().run()
        except:
            print("Error")