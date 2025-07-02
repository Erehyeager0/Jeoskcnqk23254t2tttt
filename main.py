from highrise import *
from highrise.models import *
from asyncio import run as arun
from flask import Flask
from threading import Thread
from highrise.__main__ import *
from emotes import*
import random
import asyncio
import time

class Bot(BaseBot):
    def __init__(self):
        super().__init__()
        self.emote_looping = False
        self.user_emote_loops = {}
        self.loop_task = None
        self.is_teleporting_dict = {}
        self.following_user = None
        self.following_user_id = None
        self.kus = {}
        self.user_positions = {} 
        self.position_tasks = {} 
        
    haricler = ["","","Carterers","","","",","] 

    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        print(f"{user.username} emote gönderdi: {emote_id}")
        
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.user_id = session_metadata.user_id  # Botun kendi ID'sini kaydet
        print("Emote botu başarıyla bağlandı ✅")
        
        await self.highrise.tg.create_task(
            self.highrise.teleport(session_metadata.user_id, Position(4, 0, 4, "FrontLeft"))
        )
    
    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await self.highrise.chat(f"@{user.username}, odaya hoşgeldin! 🎉🎊")
        try:
            emote_name = random.choice(list(secili_emote.keys()))
            emote_info = secili_emote[emote_name]
            emote_to_send = emote_info["value"]
            await self.send_emote(emote_to_send, user.id)
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

        # Eğer emote adı geçerliyse, önceki emote durdurulup yenisi başlatılır
        if message in emote_mapping:
            await self.start_emote_loop(user.id, message)

        # Eğer mesaj "stop" ise, emote döngüsünü durdur
        if message == "stop":
            await self.stop_emote_loop(user.id)

        if message.lower().startswith("rest"):
            await self.highrise.send_emote("sit-idle-cute")
        if message == "!bot" and await self.is_user_allowed(user):
            try:
                room_users = await self.highrise.get_room_users()
                for u, pos in room_users.content:
                    if u.id == user.id:
                        await self.highrise.teleport(self.user_id, pos)
                        break
            except Exception as e:
                print(f"Bot teleport hatası: {e}")
        teleport_locations = {
            "k1": Position(10.5, 2.25, 13.0),
            "k2": Position(10.5, 12.9, 3.5),
            "k3": Position(5.0, 7.0, 8.0),  # İstediğin koordinatları buraya yazabilirsin
        }

        if message in teleport_locations:
            try:
                await self.highrise.teleport(user.id, teleport_locations[message])
            except Exception as e:
                print(f"Teleport hatası: {e}")
                        # Moderation commands
        if not await self.is_user_allowed(user):
            pass
        else:
            if message.startswith("!kick "):
                target_name = message[6:].strip()
                await self.kick_user(target_name, user)
            elif message.startswith("!mute "):
                target_name = message[6:].strip()
                await self.mute_user(target_name, user)
            elif message.startswith("!unmute "):
                target_name = message[8:].strip()
                await self.unmute_user(target_name, user)
            elif message.startswith("!ban "):
                target_name = message[5:].strip()
                await self.ban_user(target_name, user)
            elif message.startswith("!unban "):
                target_name = message[7:].strip()
                await self.unban_user(target_name, user)
            elif message.startswith("!promote "):
                target_name = message[9:].strip()
                await self.promote_user(target_name, user)
            elif message.startswith("!demote "):
                target_name = message[8:].strip()
                await self.demote_user(target_name, user)
            elif message.startswith("!announce "):
                ann_msg = message[10:].strip()
                await self.announce_message(ann_msg, user)
            elif message == "!listbans":
                await self.list_bans(user)
            elif message.startswith("!teleport "):
                target_name = message[10:].strip()
                await self.teleport_to_user(user, target_name)
                async def kick_user(self, target_username: str, requester: User):
        room_users = (await self.highrise.get_room_users()).content
        target_user = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
        if target_user:
            await self.highrise.kick(target_user.id)
            await self.highrise.send_whisper(requester.id, f"{target_username} odadan atıldı.")
        else:
            await self.highrise.send_whisper(requester.id, f"{target_username} bulunamadı.")

    async def mute_user(self, target_username: str, requester: User):
        # Bu fonksiyonun içini API'ne göre doldurman gerekebilir.
        # Örnek olarak sadece whisper ile bilgilendirme yapıyoruz.
        await self.highrise.send_whisper(requester.id, f"{target_username} susturuldu (simülasyon).")

    async def unmute_user(self, target_username: str, requester: User):
        await self.highrise.send_whisper(requester.id, f"{target_username} susturma kaldırıldı (simülasyon).")

    async def ban_user(self, target_username: str, requester: User):
        room_users = (await self.highrise.get_room_users()).content
        target_user = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
        if target_user:
            await self.highrise.ban(target_user.id)
            await self.highrise.send_whisper(requester.id, f"{target_username} banlandı.")
        else:
            await self.highrise.send_whisper(requester.id, f"{target_username} bulunamadı.")

    async def unban_user(self, target_username: str, requester: User):
        # Highrise API'de ban kaldırma nasıl yapılıyorsa oraya göre implement et.
        await self.highrise.send_whisper(requester.id, f"{target_username} ban kaldırıldı (simülasyon).")

    async def promote_user(self, target_username: str, requester: User):
        room_users = (await self.highrise.get_room_users()).content
        target_user = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
        if target_user:
            await self.highrise.set_room_privilege(target_user.id, moderator=True)
            await self.highrise.send_whisper(requester.id, f"{target_username} moderatör yapıldı.")
        else:
            await self.highrise.send_whisper(requester.id, f"{target_username} bulunamadı.")

    async def demote_user(self, target_username: str, requester: User):
        room_users = (await self.highrise.get_room_users()).content
        target_user = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
        if target_user:
            await self.highrise.set_room_privilege(target_user.id, moderator=False)
            await self.highrise.send_whisper(requester.id, f"{target_username} moderatörlükten çıkarıldı.")
        else:
            await self.highrise.send_whisper(requester.id, f"{target_username} bulunamadı.")

    async def announce_message(self, message: str, requester: User):
        await self.highrise.chat(f"** Duyuru: {message} **")

    async def list_bans(self, requester: User):
        bans = await self.highrise.get_bans()
        if bans:
            ban_list = "\n".join([ban.username for ban in bans])
            await self.highrise.send_whisper(requester.id, f"Banlı kullanıcılar:\n{ban_list}")
        else:
            await self.highrise.send_whisper(requester.id, "Banlı kullanıcı yok.")

    async def teleport_to_user_old(self, requester: User, target_username: str):
        room_users = (await self.highrise.get_room_users()).content
        target_user = next((u for u, _ in room_users if u.username.lower() == target_username.lower()), None)
        if target_user:
            target_pos = next(pos for u, pos in room_users if u.id == target_user.id)
            await self.highrise.teleport(requester.id, target_pos)
            await self.highrise.send_whisper(requester.id, f"{target_username}'ya teleport oldunuz.")
        else:
            await self.highrise.send_whisper(requester.id, f"{target_username} bulunamadı.")

    async def start_emote_loop(self, user_id: str, emote_name: str) -> None:
        # Önceki emote varsa onu durdur
        if user_id in self.user_emote_loops:
            await self.stop_emote_loop(user_id)

        # Yeni emote başlat
        self.user_emote_loops[user_id] = emote_name

        if emote_name in emote_mapping:
            emote_info = emote_mapping[emote_name]
            emote_to_send = emote_info["value"]
            emote_time = emote_info["time"]

            while self.user_emote_loops.get(user_id) == emote_name:
                try:
                    await self.highrise.send_emote(emote_to_send, user_id)
                except Exception as e:
                    if "Target user not in room" in str(e):
                        print(f"{user_id} odada değil, emote gönderme durduruluyor.")
                        break
                await asyncio.sleep(emote_time)

    async def stop_emote_loop(self, user_id: str) -> None:
        if user_id in self.user_emote_loops:
            self.user_emote_loops.pop(user_id)
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


        message = message.lower()

        teleport_locations = {            "طلعني": Position(
            10.5, 11.7, 7.5),
                        "فوق": Position(10.5, 6, 3.5),
                        "k1": Position(
            10.5, 2.25, 13.0),
                              "k2": Position(
            10.5, 12.9, 3.5),
        } 
        for location_name, position in teleport_locations.items():
            if message ==(location_name):
                try:
                    await self.teleport(user, position)
                except:
                    print("Teleporlanma sırasında hata oluştu")
                  
        if message.lower().startswith("sustur") and await self.is_user_allowed(user):
            target_username = message.split("@")[-1].strip()
            room_users = await self.highrise.get_room_users()
            user_info = next((info for info in room_users.content if info[0].username.lower() == target_username.lower()), None)

            if user_info:
                target_user_obj, initial_position = user_info
                task = asyncio.create_task(self.reset_target_position(target_user_obj, initial_position))

                if target_user_obj.id not in self.position_tasks:
                    self.position_tasks[target_user_obj.id] = []
                self.position_tasks[target_user_obj.id].append(task)

        elif message.lower().startswith("banla") and await self.is_user_allowed(user):
            target_username = message.split("@")[-1].strip()
            room_users = await self.highrise.get_room_users()
            target_user_obj = next((user_obj for user_obj, _ in room_users.content if user_obj.username.lower() == target_username.lower()), None)

            if target_user_obj:
                tasks = self.position_tasks.pop(target_user_obj.id, [])
                for task in tasks:
                    task.cancel()
                print(f"{target_username} için pozisyon izleme döngüsü sonlandırıldı.")
            else:
                print(f"Kullanıcı {target_username} odada bulunamadı.")

        if message.lower().startswith("ik"):
            target_username = message.split("@")[-1].strip()
            await self.userinfo(user, target_username)


        if message.startswith("+x") or message.startswith("-x"):
            await self.adjust_position(user, message, 'x')
        elif message.startswith("+y") or message.startswith("-y"):
            await self.adjust_position(user, message, 'y')
        elif message.startswith("+z") or message.startswith("-z"):
            await self.adjust_position(user, message, 'z')
              
      
        allowed_commands = ["de", "değiş","değis","degiş"] 
        if any(message.lower().startswith(command) for command in allowed_commands) and await self.is_user_allowed(user):
            target_username = message.split("@")[-1].strip()

        
            if target_username not in self.haricler:
                await self.switch_users(user, target_username)
            else:
                print(f"{target_username} engellenenler listesinde olduğu için işlem yapılmayacak.")

        if message.lower().startswith("teleport") or message.lower().startswith("tp"):
          target_username = message.split("@")[-1].strip()
          await self.teleport_to_user(user, target_username)
        if await self.is_user_allowed(user) and message.lower().startswith("br"):
            target_username = message.split("@")[-1].strip()
            if target_username not in self.haricler:
                await self.teleport_user_next_to(target_username, user)
        if message.lower().startswith("--") and await self.is_user_allowed(user):
            parts = message.split()
            if len(parts) == 2 and parts[1].startswith("@"):
                target_username = parts[1][1:]
                target_user = None

                room_users = (await self.highrise.get_room_users()).content
                for room_user, _ in room_users:
                    if room_user.username.lower() == target_username and room_user.username.lower() not in self.haricler:
                        target_user = room_user
                        break

                if target_user:
                    try:
                        kl = Position(random.randint(0, 40), random.randint(0, 40), random.randint(0, 40))
                        await self.teleport(target_user, kl)
                    except Exception as e:
                        print(f"Teleport yapılırken hata oluştu: {e}")
                else:
                    print(f"Kullanıcı adı '{target_username}' odada bulunamadı.")

        if message.lower() == "full rtp" or message.lower() == "full rtp2":
            if user.id not in self.kus:
                self.kus[user.id] = False

            if not self.kus[user.id]:
                self.kus[user.id] = True

                try:
                    while self.kus.get(user.id, False):
                        kl = Position(random.randint(0, 29), random.randint(0, 29), random.randint(0, 29))
                        await self.teleport(user, kl)

                        await asyncio.sleep(0.7)
                except Exception as e:
                    print(f"Teleport sırasında hata oluştu: {e}")

        if message.lower() == "dur" or message.lower() == "stop":
            if user.id in self.kus: 
                self.kus[user.id] = False

        if message.lower().startswith("?!;") and await self.is_user_allowed(user):
            target_username = message.split("@")[-1].strip().lower()

            if target_username not in self.haricler:
                room_users = (await self.highrise.get_room_users()).content
                target_user = next((u for u, _ in room_users if u.username.lower() == target_username), None)

                if target_user:
                    if target_user.id not in self.is_teleporting_dict:
                        self.is_teleporting_dict[target_user.id] = True

                        try:
                            while self.is_teleporting_dict.get(target_user.id, False):
                                kl = Position(random.randint(0, 39), random.randint(0, 29), random.randint(0, 39))
                                await self.teleport(target_user, kl)
                                await asyncio.sleep(1)
                        except Exception as e:
                            print(f"Teleport yapılırken hata oluştu: {e}")

                        self.is_teleporting_dict.pop(target_user.id, None)
                        final_position = Position(4.0, 0.0, 9.5, "FrontRight")
                        await self.teleport(target_user, final_position)
                    

        if message.lower().startswith("?!;:") and await self.is_user_allowed(user):
            target_username = message.split("@")[-1].strip().lower()

            room_users = (await self.highrise.get_room_users()).content
            target_user = next((u for u, _ in room_users if u.username.lower() == target_username), None)

            if target_user:
                self.is_teleporting_dict.pop(target_user.id, None)
                

        if message.lower() == "?!;:''" and await self.is_user_allowed(user):
            if self.following_user is not None:
                await self.highrise.chat("Gözüm üstünde, geliyorum")
            else:
                await self.follow(user)

        if message.lower() == "?!;:a" and await self.is_user_allowed(user):
            if self.following_user is not None:
                await self.highrise.chat("Gözüm üstünde duruyorum 💋 ")
                self.following_user = None
            else:
                await self.highrise.chat("Gözüm üstünde duruyorum 💋 ")
              
        if message.lower().startswith("kick") and await self.is_user_allowed(user):
            parts = message.split()
            if len(parts) != 2:
                return
            if "@" not in parts[1]:
                username = parts[1]
            else:
                username = parts[1][1:]

            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() == username.lower():
                    user_id = room_user.id
                    break

            if "user_id" not in locals():
                return

            try:
                await self.highrise.moderate_room(user_id, "kick")
            except Exception as e:
                return


      
        message = message.strip().lower()
        user_id = user.id
      
        if message.startswith(""):
            emote_name = message.replace("", "").strip()
            if user_id in self.user_emote_loops and self.user_emote_loops[user_id] == emote_name:
                await self.stop_emote_loop(user_id)
            else:
                await self.start_emote_loop(user_id, emote_name)
                
        if message == "stop" or message == "dur" or message == "0":
            if user_id in self.user_emote_loops:
                await self.stop_emote_loop(user_id)
                
        if message == "durmuske":
            if user_id not in self.user_emote_loops:
                await self.start_random_emote_loop(user_id)
                
        if message == "stop" or message == "dur":
            if user_id in self.user_emote_loops:
                if self.user_emote_loops[user_id] == "abekaynana":
                    await self.stop_random_emote_loop(user_id)
     

        message = message.strip().lower()

        if "@" in message:
            parts = message.split("@")
            if len(parts) < 2:
                return

            emote_name = parts[0].strip()
            target_username = parts[1].strip()

            if emote_name in emote_mapping:
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                usernames = [user.username.lower() for user in users]

                if target_username not in usernames:
                    return

                user_id = next((u.id for u in users if u.username.lower() == target_username), None)
                if not user_id:
                    return

                await self.handle_emote_command(user.id, emote_name)
                await self.handle_emote_command(user_id, emote_name)


        for emote_name, emote_info in emote_mapping.items():
            if message.lower() == emote_name.lower():
                try:
                    emote_to_send = emote_info["value"]
                    await self.highrise.send_emote(emote_to_send, user.id)
                except Exception as e:
                    print(f"Emote gönderilirken hata: {e}")
        
        if message.lower().startswith("all ") and await self.is_user_allowed(user):
            emote_name = message.replace("all ", "").strip()
            if emote_name in emote_mapping:
                emote_to_send = emote_mapping[emote_name]["value"]
                room_users = (await self.highrise.get_room_users()).content
                tasks = []
                for room_user, _ in room_users:
                    tasks.append(self.highrise.send_emote(emote_to_send, room_user.id))
                try:
                    await asyncio.gather(*tasks)
                except Exception as e:
                    error_message = f"Emote gönderilirken hata oluştu: {e}"
                    await self.highrise.send_whisper(user.id, error_message)
            else:
                await self.highrise.send_whisper(user.id, f"Geçersiz emote adı: {emote_name}")
    
        message = message.strip().lower()

        try:
            if message.lstrip().startswith(("babubabu")):
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                usernames = [user.username.lower() for user in users]
                parts = message[1:].split()
                args = parts[1:]

                if len(args) >= 1 and args[0][0] == "@" and args[0][1:].lower() in usernames:
                    user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)

                    if message.lower().startswith("m?!"):
                        await self.highrise.send_emote("emote-telekinesis", user.id)
                        await self.highrise.send_emote("emote-gravity", user_id)
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
          
        if message.startswith("rd") or message.startswith("!grts"):
            try:
                emote_name = random.choice(list(secili_emote.keys()))
                emote_to_send = secili_emote[emote_name]["value"]
                await self.highrise.send_emote(emote_to_send, user.id)
            except:
                print("Dans emote gönderilirken bir hata oluştu.")


# Numaralı emojiler numaralı emojiler
  
    async def handle_emote_command(self, user_id: str, emote_name: str) -> None:
        if emote_name in emote_mapping:
            emote_info = emote_mapping[emote_name]
            emote_to_send = emote_info["value"]

            try:
                await self.highrise.send_emote(emote_to_send, user_id)
            except Exception as e:
                print(f"Emote gönderilirken hata oluştu: {e}")


    async def start_emote_loop(self, user_id: str, emote_name: str) -> None:
        if emote_name in emote_mapping:
            self.user_emote_loops[user_id] = emote_name
            emote_info = emote_mapping[emote_name]
            emote_to_send = emote_info["value"]
            emote_time = emote_info["time"]

            while self.user_emote_loops.get(user_id) == emote_name:
                try:
                    await self.highrise.send_emote(emote_to_send, user_id)
                except Exception as e:
                    if "Target user not in room" in str(e):
                        print(f"{user_id} odada değil, emote gönderme durduruluyor.")
                        break
                await asyncio.sleep(emote_time)

    async def stop_emote_loop(self, user_id: str) -> None:
        if user_id in self.user_emote_loops:
            self.user_emote_loops.pop(user_id)


# Ücretli emojiler ücretli emojiler ücretli emojiler
  
    async def emote_loop(self):
        while True:
            try:
                emote_name = random.choice(list(paid_emotes.keys()))
                emote_to_send = paid_emotes[emote_name]["value"]
                emote_time = paid_emotes[emote_name]["time"]
                
                await self.highrise.send_emote(emote_id=emote_to_send)
                await asyncio.sleep(emote_time)
            except Exception as e:
                print("Emote gönderilirken hata oluştu:", e) 


# Ulti Ulti Ulti Ulti Ulti Ulti Ulti

    async def start_random_emote_loop(self, user_id: str) -> None:
        self.user_emote_loops[user_id] = "dans"
        while self.user_emote_loops.get(user_id) == "dans":
            try:
                emote_name = random.choice(list(secili_emote.keys()))
                emote_info = secili_emote[emote_name]
                emote_to_send = emote_info["value"]
                emote_time = emote_info["time"]
                await self.highrise.send_emote(emote_to_send, user_id)
                await asyncio.sleep(emote_time)
            except Exception as e:
                print(f"Rastgele emote gönderilirken hata oluştu: {e}")

    async def stop_random_emote_loop(self, user_id: str) -> None:
        if user_id in self.user_emote_loops:
            del self.user_emote_loops[user_id]



# Genel Genel Genel Genel Genel

    async def send_emote(self, emote_to_send: str, user_id: str) -> None:
        await self.highrise.send_emote(emote_to_send, user_id)
      


    async def on_whisper(self, user: User, message: str) -> None:
        """Oda fısıltısı alındığında."""
        if await self.is_user_allowed(user) and message.startswith(''):
            try:
                xxx = message[0:]
                await self.highrise.chat(xxx)
            except:
                print("Hata oluştu 3")
  
    async def is_user_allowed(self, user: User) -> bool:
        user_privileges = await self.highrise.get_room_privilege(user.id)
        return user_privileges.moderator or user.username in ["Carterers"]

# gellllbbb

    async def moderate_room(
        self,
        user_id: str,
        action: Literal["kick", "ban", "unban", "mute"],
        action_length: int | None = None,
    ) -> None:
        """Odada kullanıcıyı moderatör işlemi yap."""
  
    async def userinfo(self, user: User, target_username: str) -> None:
        user_info = await self.webapi.get_users(username=target_username, limit=1)

        if not user_info.users:
            await self.highrise.chat("Kullanıcı bulunamadı, lütfen geçerli bir kullanıcı belirtin")
            return

        user_id = user_info.users[0].user_id

        user_info = await self.webapi.get_user(user_id)

        number_of_followers = user_info.user.num_followers
        number_of_friends = user_info.user.num_friends
        country_code = user_info.user.country_code
        outfit = user_info.user.outfit
        bio = user_info.user.bio
        active_room = user_info.user.active_room
        crew = user_info.user.crew
        number_of_following = user_info.user.num_following
        joined_at = user_info.user.joined_at.strftime("%d/%m/%Y %H:%M:%S")

        joined_date = user_info.user.joined_at.date()
        today = datetime.now().date()
        days_played = (today - joined_date).days

        last_login = user_info.user.last_online_in.strftime("%d/%m/%Y %H:%M:%S") if user_info.user.last_online_in else "Son giriş bilgisi mevcut değil"

        await self.highrise.chat(f"""Kullanıcı adı: {target_username}\nTakipçi sayısı: {number_of_followers}\nArkadaş sayısı: {number_of_friends}\nKatılım tarihi: {joined_at}\nOynanan gün sayısı: {days_played}""")

    async def follow(self, user: User, message: str = ""):
        self.following_user = user  
        while self.following_user == user:
            room_users = (await self.highrise.get_room_users()).content
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    break
            if user_position is not None and isinstance(user_position, Position):
                nearby_position = Position(user_position.x + 1.0, user_position.y, user_position.z)
                await self.highrise.walk_to(nearby_position)
            
            await asyncio.sleep(0.5) 
  
    async def adjust_position(self, user: User, message: str, axis: str) -> None:
        try:
            adjustment = int(message[2:])
            if message.startswith("-"):
                adjustment *= -1

            room_users = await self.highrise.get_room_users()
            user_position = None

            for user_obj, user_position in room_users.content:
                if user_obj.id == user.id:
                    break

            if user_position:
                new_position = None

                if axis == 'x':
                    new_position = Position(user_position.x + adjustment, user_position.y, user_position.z, user_position.facing)
                elif axis == 'y':
                    new_position = Position(user_position.x, user_position.y + adjustment, user_position.z, user_position.facing)
                elif axis == 'z':
                    new_position = Position(user_position.x, user_position.y, user_position.z + adjustment, user_position.facing)
                else:
                    print(f"Desteklenmeyen eksen: {axis}")
                    return

                await self.teleport(user, new_position)

        except ValueError:
            print("Geçersiz pozisyon ayarı. Lütfen +x/-x, +y/-y veya +z/-z ardından bir tam sayı girin.")
        except Exception as e:
            print(f"Pozisyon ayarlanırken hata oluştu: {e}")
  
    async def switch_users(self, user: User, target_username: str) -> None:
        try:
            room_users = await self.highrise.get_room_users()

            maker_position = None
            for maker_user, maker_position in room_users.content:
                if maker_user.id == user.id:
                    break

            target_position = None
            for target_user, position in room_users.content:
                if target_user.username.lower() == target_username.lower():
                    target_position = position
                    break

            if maker_position and target_position:
                await self.teleport(user, Position(target_position.x + 0.0001, target_position.y, target_position.z, target_position.facing))

                await self.teleport(target_user, Position(maker_position.x + 0.0001, maker_position.y, maker_position.z, maker_position.facing))

        except Exception as e:
            print(f"Kullanıcı değiştirirken hata oluştu: {e}")

    async def teleport(self, user: User, position: Position):
        try:
            await self.highrise.teleport(user.id, position)
        except Exception as e:
            print(f"Teleport hatası yakalandı: {e}")

    async def teleport_to_user(self, user: User, target_username: str) -> None:
        try:
            room_users = await self.highrise.get_room_users()
            for target, position in room_users.content:
                if target.username.lower() == target_username.lower():
                    z = position.z
                    new_z = z - 1
                    await self.teleport(user, Position(position.x, position.y, new_z, position.facing))
                    break
        except Exception as e:
            print(f"{target_username} kullanıcısına teleport olurken hata oluştu: {e}")

    async def teleport_user_next_to(self, target_username: str, requester_user: User) -> None:
        try:

            room_users = await self.highrise.get_room_users()
            requester_position = None
            for user, position in room_users.content:
                if user.id == requester_user.id:
                    requester_position = position
                    break

            for user, position in room_users.content:
                if user.username.lower() == target_username.lower():
                    z = requester_position.z
                    new_z = z + 1  
                    await self.teleport(user, Position(requester_position.x, requester_position.y, new_z, requester_position.facing))
                    break
        except Exception as e:
            print(f"{target_username} kullanıcısını {requester_user.username} yanına teleport ederken hata oluştu: {e}")

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        message = f"{sender.username} tarafından {receiver.username} adlı kişiye {tip.amount} miktarında hediye gönderildi! 🎁 Teşekkürler!"
        await self.highrise.chat(message)
  
    async def reset_target_position(self, target_user_obj: User, initial_position: Position) -> None:
        try:
            while True:
                room_users = await self.highrise.get_room_users()
                current_position = next((position for user, position in room_users.content if user.id == target_user_obj.id), None)

                if current_position and current_position != initial_position:
                    await self.teleport(target_user_obj, initial_position)

                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Pozisyon takibi sırasında hata oluştu: {e}")  

    async def run(self, room_id, token) -> None:
        await __main__.main(self, room_id, token)
class WebServer():

  def __init__(self):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index() -> str:
      return "Canlı"

  def run(self) -> None:
    self.app.run(host='0.0.0.0', port=8080)

  def keep_alive(self):
    t = Thread(target=self.run)
    t.start()
    
class RunBot():
  room_id = "64159cf2bed1df28637c014f" 
  bot_token = "984cb68cc036809bfdaf82e47417d89bcb7e1534440bd998a65f8af97e703ddc"
  bot_file = "main"
  bot_class = "Bot"

  def __init__(self) -> None:
    self.definitions = [
        BotDefinition(
            getattr(import_module(self.bot_file), self.bot_class)(),
            self.room_id, self.bot_token)
    ] 

  def run_loop(self) -> None:
    while True:
      try:
        arun(main(self.definitions)) 
      except Exception as e:
        import traceback
        print("Bir hata yakalandı:")
        traceback.print_exc()
        time.sleep(1)
        continue


if __name__ == "__main__":
  WebServer().keep_alive()

  RunBot().run_loop()               