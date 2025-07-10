import asyncio
from highrise import BotDefinition, main as hr_main
from main import Bot  # main.py'deki Bot sınıfını alıyoruz
import time
from threading import Thread
from flask import Flask

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        @self.app.route("/")
        def home():
            return "Bot çalışıyor ✅"
    def run(self):
        self.app.run(host="0.0.0.0", port=8080)
    def keep_alive(self):
        Thread(target=self.run).start()

class RunBot:
    room_id = "64159cf2bed1df28637c014f"  # Kendi room ID'ni buraya yaz
    token = "b12ccae2fb89720ec1199c5759c4d5251a76ef0ea97ad3ba8ead76648f87b2e1"  # Kendi tokenını buraya yaz

    def run_loop(self):
        definitions = [BotDefinition(Bot(), self.room_id, self.token)]
        while True:
            try:
                asyncio.run(hr_main(definitions))
            except Exception as e:
                print("Hata yakalandı:", e)
                time.sleep(3)

if __name__ == "__main__":
    WebServer().keep_alive()

    def start_bot():
        RunBot().run_loop()

    Thread(target=start_bot).start()