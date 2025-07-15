
from highrise import *
from highrise.models import *
from highrise import BaseBot
from highrise.__main__ import BotDefinition, main as highrise_main
from asyncio import run as arun
from flask import Flask
from threading import Thread

from emotes import*
from kiy import (
    item_hairfront,
    item_hairback,
    item_facehair,
    item_eyebrow,
    item_eye,
    item_nose,
    item_mouth,
    item_shirt,
    item_bottom,
    item_shoes,
    item_accessory,
    item_freckle
)
import random
import asyncio
import time
import importlib
from datetime import datetime

# Create emote_mapping dictionary from emote_list
# Create emote_mapping dictionary from emote_list
emote_mapping = {}
secili_emote = {}
paid_emotes = {}

for emote_data in emote_list:
    aliases, emote_id, duration = emote_data
    # Use first alias as the main key
    main_key = aliases[0].lower()
    emote_info = {"value": emote_id, "time": duration}

    # Add all aliases to emote_mapping
    for alias in aliases:
        emote_mapping[alias.lower()] = emote_info

    # Add to secili_emote (appears to be used for random selection)
    secili_emote[main_key] = emote_info

    # Add to paid_emotes as well
    paid_emotes[main_key] = emote_info

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.emote_looping = False
        self.user_emote_tasks = {}
        self.user_emote_loops = {}
        self.loop_task = None
        self.is_teleporting_dict = {}
        self.following_user = None
        self.following_user_id = None
        self.kus = {}
        self.user_positions = {} 
        self.position_tasks = {} 

    haricler = ["","","","","","",","] 

    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        print(f"{user.username} emote gönderdi: {emote_id}")

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.user_id = session_metadata.user_id  # Botun kendi ID'sini kaydet
        print("Emote botu başarıyla bağlandı ✅")

        await self.highrise.tg.create_task(
            self.highrise.teleport(session_metadata.user_id, Position(4, 0, 4, "FrontRight"))
        )

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await self.highrise.chat(f"@{user.username},🔥Inferno Club'a🔥 Hoşgeldin!")
        try:
            emote_name = random.choice(list(secili_emote.keys()))
            emote_info = secili_emote[emote_name]
            emote_to_send = emote_info["value"]
            await self.highrise.send_emote(emote_to_send, user.id)
        except Exception as e:
            print(f"Kullanıcıya emote gönderilirken hata oluştu {user.id}: {e}")

    async def on_user_leave(self, user: User):
        user_id = user.id
        farewell_message = f"Hoşça kal @{user.username}, yine bekleriz 🙏🏻👋🏻"
        if user_id in self.user_emote_loops:
            await self.stop_emote_loop(user_id)
        await self.highrise.chat(farewell_message)

    async def on_chat(self, user: User, message: str) -> None:
        message = message.strip().lower()

        # Emote başlat / durdur
        if message in emote_mapping:
            await self.start_emote_loop(user.id, message)
            return

        if message == "stop":
            await self.stop_emote_loop(user.id)
            return

        if message.startswith("!botem "):
            emote_name = message[7:].strip()
            if emote_name in emote_mapping:
                await self.start_emote_loop(self.user_id, emote_name)  # Bot kendine emote yapacak
                await self.highrise.send_whisper(user.id, f"Bot '{emote_name}' emote döngüsüne başladı.")
            else:
                await self.highrise.send_whisper(user.id, f"❌ '{emote_name}' isimli emote bulunamadı.")
            return

        if message.startswith("!with "):
            try:
                parts = message.split()
                if len(parts) < 3:
            await self.highrise.send_whisper(user.id, "❌ Kullanım: !with @kullaniciadi emoteadı")
            return

        mentioned = parts[1].lstrip("@")
        emote_name = " ".join(parts[2:]).strip()

        # Emote geçerli mi kontrol et
        if emote_name not in emote_mapping:
            await self.highrise.send_whisper(user.id, f"❌ '{emote_name}' adlı emote bulunamadı.")
            return

        # Oda kullanıcılarını al
        room_users = await self.highrise.get_room_users()
        target_user = None
        for u, _ in room_users.content:
            if u.username.lower() == mentioned.lower():
                target_user = u
                break

        if not target_user:
            await self.highrise.send_whisper(user.id, f"❌ @{mentioned} odada bulunamadı.")
            return

        # Her iki kullanıcıya aynı anda başlat
        await self.start_emote_loop(user.id, emote_name)
        await self.start_emote_loop(target_user.id, emote_name)

        await self.highrise.send_whisper(user.id, f"✅ Sen ve @{mentioned}, '{emote_name}' emote'unu aynı anda yapıyorsunuz.")
                await self.highrise.send_whisper(target_user.id, f"🎭 @{user.username} ile birlikte '{emote_name}' emote'unu yapmaya başladın!")

            except Exception as e:
                await self.highrise.send_whisper(user.id, f"⚠️ Bir hata oluştu: {e}")
            return

        # Kıyafet değiştir
        if message.startswith("degistir"):
            hair_active_palette = random.randint(0, 82)
            skin_active_palette = random.randint(0, 88)
            eye_active_palette = random.randint(0, 49)
            lip_active_palette = random.randint(0, 58)

            outfit = [
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=skin_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_shirt), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_bottom), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_accessory), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_shoes), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_freckle), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_eye), account_bound=False, active_palette=eye_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_mouth), account_bound=False, active_palette=lip_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_nose), account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id=random.choice(item_hairback), account_bound=False, active_palette=hair_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_hairfront), account_bound=False, active_palette=hair_active_palette),
                Item(type='clothing', amount=1, id=random.choice(item_eyebrow), account_bound=False, active_palette=hair_active_palette)
            ]
            await self.highrise.set_outfit(outfit=outfit)
            return

        # Bot kendini kullanıcıya ışınlar
        if message == "!bot" and await self.is_user_allowed(user):
            try:
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.content:
                    if u.id == user.id:
                        await self.highrise.teleport(self.user_id, pos)
                        break
            except Exception as e:
                print(f"Bot teleport hatası: {e}")
            return

        # Hazır konumlar
        ready_locations = {
            "": Position(7, 15, 9),
            "hapis": Position(14, 0, 16),
            "mapus": Position(14, 0, 27),
            "": Position(4, 16, 2),
        }

        if message in ready_locations:
            try:
                await self.highrise.teleport(user.id, ready_locations[message])
            except Exception as e:
                print(f"Teleport hatası: {e}")
            return

        # Yetkili kullanıcı mı kontrolü
        if await self.is_user_allowed(user):
            if message.startswith("!tp "):
                parts = message.split()
                if len(parts) >= 2:
                    target_username = parts[1].lstrip("@")
                    target_location = parts[2] if len(parts) > 2 else None

                    room_users = await self.highrise.get_room_users()
                    target_user = next((u for u, _ in room_users.content if u.username.lower() == target_username.lower()), None)

                    if not target_user:
                        await self.highrise.send_whisper(user.id, f"❌ {target_username} odada bulunamadı.")
                    elif target_location and target_location in ready_locations:
                        await self.highrise.teleport(target_user.id, ready_locations[target_location])
                        await self.highrise.send_whisper(user.id, f"✅ {target_username}, '{target_location}' konumuna ışınlandı.")
                        await self.highrise.send_whisper(target_user.id, f"📍 {user.username} seni '{target_location}' konumuna ışınladı.")
                    else:
                        target_pos = next((pos for u, pos in room_users.content if u.username.lower() == target_username.lower()), None)
                        if target_pos:
                            await self.highrise.teleport(user.id, target_pos)
                        await self.highrise.send_whisper(user.id, f"✅ {target_username} kullanıcısına ışınlandın.")
                else:
                    await self.highrise.send_whisper(user.id, "⚠️ Kullanım: !tp @kullanici [konum]")
                return

            elif message.startswith("!gel "):
                target_username = message[5:].strip().lstrip("@")
                room_users = await self.highrise.get_room_users()
                target_user = next((u for u, _ in room_users.content if u.username.lower() == target_username.lower()), None)

                if target_user:
                    user_pos = next((pos for u, pos in room_users.content if u.id == user.id), None)
                    if user_pos:
                        await self.highrise.teleport(target_user.id, user_pos)
                    await self.highrise.send_whisper(user.id, f"✅ {target_username} yanına ışınlandı.")
                    await self.highrise.send_whisper(target_user.id, f"📍 {user.username} seni yanına ışınladı.")
                else:
                    await self.highrise.send_whisper(user.id, f"❌ {target_username} odada bulunamadı.")
                return

            elif message.startswith("!goto "):
                loc = message[6:].strip().lower()
                if loc in ready_locations:
                    await self.highrise.teleport(user.id, ready_locations[loc])
                    await self.highrise.send_whisper(user.id, f"✅ '{loc}' konumuna ışınlandın.")
                else:
                    await self.highrise.send_whisper(user.id, f"❌ '{loc}' konumu bulunamadı.")
                return

            elif message.startswith("!bringall "):
                hedef = message[10:].strip().lower()

                # Eğer hedef hazır konumsa
                if hedef in ready_locations:
                    room_users = await self.highrise.get_room_users()
                    for u, _ in room_users.content:
                        if u.id != self.user_id:  # Bot kendini ışınlamasın
                            try:
                                await self.highrise.teleport(u.id, ready_locations[hedef])
                            except Exception:
                                pass
                    await self.highrise.send_whisper(user.id, f"✅ Tüm kullanıcılar '{hedef}' konumuna taşındı.")

                else:
                    # Kullanıcıya ışınlama modu
                    target_user = None
                    room_users = await self.highrise.get_room_users()
                    for u, pos in room_users.content:
                        if u.username.lower() == hedef and u.id != self.user_id:
                            target_user = (u, pos)
                            break

                    if target_user:
                        for u, _ in room_users.content:
                            if u.id != self.user_id and u.id != target_user[0].id:
                                try:
                                    await self.highrise.teleport(u.id, target_user[1])
                                except Exception:
                                    pass
                        await self.highrise.send_whisper(user.id, f"✅ Tüm kullanıcılar {target_user[0].username} kullanıcısının yanına taşındı.")
                    else:
                        await self.highrise.send_whisper(user.id, f"❌ '{hedef}' konumu veya kullanıcı bulunamadı.")
                return

            elif message.startswith("!say "):
                text = message[5:].strip()
                if text:
                    await self.highrise.chat(text)
                else:
                    await self.highrise.send_whisper(user.id, "⚠️ Boş mesaj gönderilemez.")
                return

            elif message in ["-helpmod", "!helpmod"]:
                await self.highrise.send_whisper(user.id,
                    "🔒 **Moderatör Komutları:**\n"
                    "🧍‍♂️ `!tp @kullanici` → Belirttiğin kullanıcıya ışınlanırsın.\n"
                    "📍 `!tp @kullanici konum` → Kullanıcıyı hazır konuma ışınlarsın.\n"
                    "📥 `!gel @kullanici` → Kullanıcıyı yanına ışınlarsın.\n"
                    "Carterers'in selamı var 🌚")

                await self.highrise.send_whisper(user.id,
                    "🧲 `!bringall konum` → Herkesi belirli bir konuma ışınlarsın.\n"
                                                 "🤖 `!bot` → Bot kendini yanına ışınlar.\n"
                    "🗣️ `!say mesaj` → Bot ile odaya mesaj gönder.\n"
                    "Carterers'in selamı var 🌚")
                return

        # Yetkisiz kullanıcı komut denediğinde uyar
        restricted_cmds = [
            "!tp", "!gel", "!kick", "!ban", "!unban", "!mute", "!unmute",
            "!promote", "!demote", "!announce", "!say", "!bringall", "!goto", "!listbans"
        ]
        if any(message.startswith(cmd) for cmd in restricted_cmds):
            await self.highrise.send_whisper(user.id, "❌ Bu komutu kullanmak için yetkin yok.")

        

            isimler1 = [
                "\n1 - ",
                "\n2 - ",
                "\n3 - ",
                "\n4 - ",
                "\n5 - ",
            ]
            isimler2 = [
                "\n6 - ",
                "\n7 - ",
                "\n8 - ",
                "\n9 - ",
                "\n10 - ",
            ]
            isimler3 = [
                "\n11 - ",
                "\n12 - ",
                "\n13 - ",
                "\n14 - ",
                "\n15 - ",
            ]
            isimler4 = [
                "\n16 - ",
                "\n17 - ",
                "\n18 - ",
                "\n19 - ",
                "\n20 - ",
            ]
            isimler5 = [
                "\n21 - ",
                "\n22 - ",
                "\n23 - ",
                "\n24 - ",
                "\n25 - ",
                "\n26 - "
            ]


            if message.lower().startswith("banlist"):
                  await self.highrise.chat("\n".join(isimler1))
                  await self.highrise.chat("\n".join(isimler2))
                  await self.highrise.chat("\n".join(isimler3))
                  await self.highrise.chat("\n".join(isimler4))
                  await self.highrise.chat("\n".join(isimler5))
                  await self.highrise.chat(f"\n\nBot sahibini takip edin: @Carterers")

    async def start_emote_loop(self, user_id: str, emote_name: str) -> None:
        if user_id in self.user_emote_tasks:
            current_task = self.user_emote_tasks[user_id]
            if not current_task.done():
                if getattr(current_task, "emote_name", None) == emote_name:
                    return  # Aynı emote zaten çalışıyor
                else:
                    current_task.cancel()
                    try:
                        await current_task
                    except asyncio.CancelledError:
                        pass
            self.user_emote_tasks.pop(user_id, None)

        task = asyncio.create_task(self._emote_loop(user_id, emote_name))
        task.emote_name = emote_name
        self.user_emote_tasks[user_id] = task

    # Emote döngüsünü gerçekleştiren iç task
    async def _emote_loop(self, user_id: str, emote_name: str) -> None:
        if emote_name not in emote_mapping:
            return
        emote_info = emote_mapping[emote_name]
        emote_to_send = emote_info["value"]
        emote_time = emote_info["time"]

        while True:
            try:
                await self.highrise.send_emote(emote_to_send, user_id)
            except Exception as e:
                if "Target user not in room" in str(e):
                    print(f"{user_id} odada değil, emote gönderme durduruluyor.")
                    break
            await asyncio.sleep(emote_time)

    # Emote döngüsünü durdur
    async def stop_emote_loop(self, user_id: str) -> None:
        if user_id in self.user_emote_tasks:
            task = self.user_emote_tasks[user_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            self.user_emote_tasks.pop(user_id, None)

    async def is_user_allowed(self, user: User) -> bool:
        user_privileges = await self.highrise.get_room_privilege(user.id)
        return user_privileges.moderator or user.username in ["Carterers", "mhrmws", "Elifmisim.m00", "Ayshee2", "mhrmws_", "revenqee"]

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        message = f"{sender.username} tarafından {receiver.username} adlı kişiye {tip.amount} miktarında hediye gönderildi! 🎁 Teşekkürler!"
        await self.highrise.chat(message)

    async def run(self, room_id, token) -> None:
        from highrise import BotDefinition
        from highrise.__main__ import main as highrise_main
        definitions = [BotDefinition(self, room_id, token)]
        await highrise_main(definitions)

    async def shutdown(self):
        # Task'ları iptal et
        for task in asyncio.all_tasks():
            task.cancel()
        # Cancel edilenleri bekle
        await asyncio.gather(*asyncio.all_tasks(), return_exceptions=True)

class WebServer():
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Bot çalışıyor ✅"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

# BOT BAŞLATICI
if __name__ == "__main__":
    WebServer().keep_alive()  # 🔁 Web server'ı başlat

    room_id = "64159cf2bed1df28637c014f"
    bot_token = "b12ccae2fb89720ec1199c5759c4d5251a76ef0ea97ad3ba8ead76648f87b2e1"
    bot = Bot()

    definitions = [BotDefinition(bot, room_id, bot_token)]
    asyncio.run(highrise_main(definitions))