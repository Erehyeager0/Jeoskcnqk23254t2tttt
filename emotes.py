import asyncio
from highrise import BaseBot
from highrise.models import User, Position, AnchorPosition

emote_list = [
    (['1', 'rest', 'REST', 'Rest'], 'sit-idle-cute', 17.06),
    (['2', 'zombie', 'ZOMBIE', 'Zombie'], 'idle_zombie', 28.75),
    (['3', 'relaxed', 'RElAXED', 'Relaxed'], 'idle_layingdown2', 20.55),
    (['4', 'attentive', 'att', 'Attentive'], 'idle_layingdown', 23.55),
    (['5', 'sleepy', 'SlEEPY', 'Sleepy'], 'idle-sleep', 22.62),
    (['6', 'pouty', 'POUT', 'Pouty', 'Pouty Face'], 'idle-sad', 24.38),
    (['7', 'posh', 'POSH', 'Posh'], 'idle-posh', 21.85),
    (['8', 'tired', 'Tired', 'Tired'], 'idle-loop-tired', 21.96),
    (['9', 'laploop', 'TapLoop', 'TapLoop'], 'idle-loop-tapdance', 6.26),
    (['10', 'shy', 'SHY', 'Shy'], 'idle-loop-shy', 16.47),
    (['11', 'bummed', 'BUMMED', 'Bummed'], 'idle-loop-sad', 6.05),
    (['12', 'Chill', 'chill', "chillin'", "Chillin'"], 'idle-loop-happy', 18.80),
    (['13', 'annoyed', 'annoyed', 'Annoyed'], 'idle-loop-annoyed', 17.06),
    (['14', 'aerobics', 'aerobic', 'Aerobics'], 'idle-loop-aerobics', 8.51),
    (['15', 'lookup', 'Loopup', 'ponder', 'Ponder'], 'idle-lookup', 22.34),
    (['16', 'heropose', 'Hero', 'Heropose', 'hero', 'Hero Pose'], 'idle-hero', 21.88),
    (['17', 'relaxing', 'RElAXING', 'Relaxing'], 'idle-floorsleeping2', 16.25),
    (['18', 'cozynap', 'nap', 'Nap', 'Cozynap', 'Cozy Nap'], 'idle-floorsleeping', 13.00),
    (['19', 'enthused', 'enthus', 'Enthused'], 'idle-enthusiastic', 15.94),
    (['20', 'beat', 'feelbeat', 'FeelTheBeat'], 'idle-dance-headbobbing', 25.37),
    (['21', 'irritated', 'irritat', 'Irritated'], 'idle-angry', 25.43),
    (['22', 'fly', 'Fly', 'I Believe I Can Fly'], 'emote-wings', 13.13),
    (['23', 'think', 'Think'], 'emote-think', 3.69),
    (['24', 'theatrical', 'theatric', 'Theatrical'], 'emote-theatrical', 8.59),
    (['25', 'tapdance', 'tap dance', 'TapDance'], 'emote-tapdance', 11.06),
    (['26', 'superrun', 'Superrun', 'Super Run'], 'emote-superrun', 6.27),
    (['27', 'super punch', 'superpunch', 'Superpunch', 'Super Punch'], 'emote-superpunch', 3.75),
    (['28', 'sumo', 'Sumo', 'Sumo Fight'], 'emote-sumo', 10.87),
    (['29', 'thumb suck', 'thumbsuck', 'Thumb suck', 'suckthumb'], 'emote-suckthumb', 4.19),
    (['30', 'splits drop', 'Splits drop', 'splits'], 'emote-splitsdrop', 4.47),
    (['31', 'snowball fight', 'Snowball fight', 'snowball'], 'emote-snowball', 5.23),
    (['32', 'snow angel', 'Snow angel', 'angel'], 'emote-snowangel', 6.22),
    (['33', 'secret handshake', 'Secret handshake', 'handshake'], 'emote-secrethandshake', 3.88),
    (['34', 'rope pull', 'Rope pull', 'rope'], 'emote-ropepull', 8.77),
    (['35', 'roll', 'Roll'], 'emote-roll', 3.56),
    (['36', 'rofl', 'ROFL'], 'emote-rofl', 6.31),
    (['37', 'robot', 'Robot'], 'emote-robot', 7.61),
    (['38', 'rainbow', 'Rainbow'], 'emote-rainbow', 2.81),
    (['39', 'proposing', 'Proposing', 'proposal'], 'emote-proposing', 4.28),
    (['40', 'peekaboo', 'Peekaboo'], 'emote-peekaboo', 3.63),
    (['41', 'peace', 'Peace'], 'emote-peace', 5.76),
    (['42', 'panic', 'Panic'], 'emote-panic', 2.85),
    (['43', 'ninja run', 'Ninja run', 'ninja'], 'emote-ninjarun', 4.75),
    (['44', 'night fever', 'Night fever', 'fever'], 'emote-nightfever', 5.49),
    (['45', 'monster fail', 'Monster fail'], 'emote-monster_fail', 4.63),
    (['46', 'model', 'Model'], 'emote-model', 6.49),
    (['47', 'flirty wave', 'Flirty wave', 'flirty'], 'emote-lust', 4.66),
    (['48', 'level up', 'Level up'], 'emote-levelup', 6.05),
    (['49', 'amused', 'Amused'], 'emote-laughing2', 5.06),
    (['50', 'laugh', 'Laugh'], 'emote-laughing', 2.69),
(["51", "ninja run", "Ninja run", "ninja"], "emote-ninjarun", 4.75),
    (["52", "night fever", "Night fever", "fever"], "emote-nightfever", 5.49),
    (["53", "monster fail", "Monster fail"], "emote-monster_fail", 4.63),
    (["54", "model", "Model"], "emote-model", 6.49),
    (["55", "flirty wave", "Flirty wave", "flirty"], "emote-lust", 4.66),
    (["56", "level up", "Level up"], "emote-levelup", 6.05),
    (["57", "amused", "Amused"], "emote-laughing2", 5.06),
    (["58", "laugh", "Laugh"], "emote-laughing", 2.69),
    (["59", "kiss", "Kiss"], "emote-kiss", 2.39),
    (["60", "super kick", "Super kick", "kick"], "emote-kicking", 4.87),
    (["61", "jump", "Jump"], "emote-jumpb", 3.58),
    (["62", "judo chop", "Judo chop"], "emote-judochop", 2.43),
    (["63", "imaginary jetpack", "Imaginary jetpack", "jetpack"], "emote-jetpack", 16.76),
    (["64", "hug yourself", "Hug yourself", "hug"], "emote-hugyourself", 4.99),
    (["65", "sweating", "Sweating"], "emote-hot", 4.35),
    (["66", "breakdance", "Breakdance"], "dance-breakdance", 17.62),
    (["67", "gangnam style", "Gangnam style", "gangnam"], "emote-gangnam", 7.28),
    (["68", "frolic", "Frolic"], "emote-frollicking", 3.70),
    (["69", "faint", "Faint"], "emote-fainting", 18.42),
    (["70", "clumsy", "Clumsy"], "emote-fail2", 6.48),
    (["71", "fall", "Fall"], "emote-fail1", 5.62),
    (["72", "face palm", "Face palm"], "emote-exasperatedb", 2.72),
    (["73", "exasperated", "Exasperated"], "emote-exasperated", 2.37),
    (["74", "elbow bump", "Elbow bump"], "emote-elbowbump", 3.80),
    (["75", "disco", "Disco"], "emote-disco", 5.37),
    (["76", "blast off", "Blast Off"], "emote-disappear", 6.2),
    (["77", "faint drop", "Faint Drop"], "emote-deathdrop", 3.76),
    (["78", "collapse", "Collapse"], "emote-death2", 4.86),
    (["79", "revival", "Revival"], "emote-death", 6.62),
    (["80", "dab", "Dab"], "emote-dab", 2.72),
    (["81", "curtsy", "Curtsy"], "emote-curtsy", 2.43),
    (["82", "confusion", "Confusion"], "emote-confused", 8.58),
    (["83", "cold", "Cold"], "emote-cold", 3.66),
    (["84", "charging", "Charging"], "emote-charging", 8.03),
    (["85", "bunny hop", "Bunny Hop"], "emote-bunnyhop", 12.38),
    (["86", "bow", "Bow"], "emote-bow", 3.34),
    (["87", "boo", "Boo"], "emote-boo", 4.5),
    (["88", "home run!", "Home Run!"], "emote-baseball", 7.25),
    (["89", "falling apart", "Falling Apart"], "emote-apart", 4.81),
    (["90", "thumbs up", "Thumbs Up"], "emoji-thumbsup", 2.7),
    (["91", "point", "Point"], "emoji-there", 2.06),
    (["92", "sneeze", "Sneeze"], "emoji-sneeze", 3.0),
    (["93", "smirk", "Smirk"], "emoji-smirking", 4.82),
    (["94", "sick", "Sick"], "emoji-sick", 5.07),
    (["95", "gasp", "Gasp"], "emoji-scared", 3.01),
    (["96", "punch", "Punch"], "emoji-punch", 1.76),
    (["97", "pray", "Pray"], "emoji-pray", 4.5),
    (["98", "stinky", "Stinky"], "emoji-poop", 4.8),
    (["99", "naughty", "Naughty"], "emoji-naughty", 4.28),
    (["100", "mind blown", "Mind Blown"], "emoji-mind-blown", 2.4),
    (["101", "sneeze", "Sneeze"], "emoji-sneeze", 3.0),
    (["102", "smirk", "Smirk"], "emoji-smirking", 4.82),
    (["103", "sick", "Sick"], "emoji-sick", 5.07),
    (["104", "gasp", "Gasp"], "emoji-scared", 3.01),
    (["105", "punch", "Punch"], "emoji-punch", 1.76),
    (["106", "pray", "Pray"], "emoji-pray", 4.5),
    (["107", "stinky", "Stinky"], "emoji-poop", 4.8),
    (["108", "naughty", "Naughty"], "emoji-naughty", 4.28),
    (["109", "mind blown", "Mind Blown"], "emoji-mind-blown", 2.4),
    (["110", "lying", "Lying"], "emoji-lying", 6.31),
    (["111", "levitate", "Levitate"], "emoji-halo", 5.84),
    (["112", "fireball lunge", "Fireball Lunge"], "emoji-hadoken", 2.72),
    (["113", "give up", "Give Up"], "emoji-give-up", 5.41),
    (["114", "tummy ache", "Tummy Ache"], "emoji-gagging", 5.5),
    (["115", "flex", "Flex"], "emoji-flex", 2.1),
    (["116", "stunned", "Stunned"], "emoji-dizzy", 4.05),
    (["117", "cursing emote", "Cursing Emote"], "emoji-cursing", 2.38),
    (["118", "sob", "Sob"], "emoji-crying", 3.7),
    (["119", "clap", "Clap"], "emoji-clapping", 2.16),
    (["120", "raise the roof", "Raise The Roof"], "emoji-celebrate", 3.41),
    (["121", "arrogance", "Arrogance"], "emoji-arrogance", 6.87),
    (["122", "angry", "Angry"], "emoji-angry", 5.76),
    (["123", "vogue hands", "Vogue Hands"], "dance-voguehands", 9.15),
    (["124", "tiktok8", "Savage Dance"], "dance-tiktok8", 10.94),
    (["125", "tiktok2", "Don't Start Now"], "dance-tiktok2", 10.39),
    (["126", "yoga flow", "Yoga Flow"], "dance-spiritual", 15.8),
    (["127", "smoothwalk", "Smoothwalk"], "dance-smoothwalk", 5.69),
    (["128", "ring on it", "Ring on It"], "dance-singleladies", 21.19),
    (["129", "let's go shopping", "Let's Go Shopping"], "dance-shoppingcart", 4.32),
    (["130", "russian dance", "Russian Dance"], "dance-russian", 10.25),
    (["131", "robotic", "Robotic"], "dance-robotic", 17.81),
    (["132", "penny's dance", "Penny's Dance"], "dance-pennywise", 1.21),
    (["133", "orange juice dance", "Orange Juice Dance"], "dance-orangejustice", 6.48),
    (["134", "rock out", "Rock Out"], "dance-metal", 15.08),
    (["135", "karate", "Karate"], "dance-martial-artist", 13.28),
    (["136", "macarena", "Macarena"], "dance-macarena", 12.21),
    (["137", "hands in the air", "Hands in the Air"], "dance-handsup", 22.28),
    (["138", "floss", "Floss"], "dance-floss", 21.33),
    (["139", "duck walk", "Duck Walk"], "dance-duckwalk", 11.75),
    (["140", "ghost float", "Ghost float", "ghost", "Ghost", "ghostfloat"], "emote-ghost-idle", 18.40),
    (["141", "breakdance", "Breakdance"], "dance-breakdance", 17.62),
    (["142", "k-pop dance", "K-Pop Dance"], "dance-blackpink", 7.15),
    (["143", "push ups", "Push Ups"], "dance-aerobics", 8.8),
    (["144", "hyped", "Hyped"], "emote-hyped", 7.49),
    (["145", "jinglebell", "Jinglebell"], "dance-jinglebell", 11),
    (["146", "nervous", "Nervous"], "idle-nervous", 21.71),
    (["147", "toilet", "Toilet"], "idle-toilet", 32.17),
    (["148", "attention", "Attention"], "emote-attention", 4.4),
    (["149", "astronaut", "Astronaut"], "emote-astronaut", 13.79),
    (["150", "eyeroll", "Eyeroll"], "emoji-eyeroll", 3.02),
    (["151", "heart eyes", "Heart Eyes"], "emote-hearteyes", 4.03),
    (["152", "swordfight", "Swordfight"], "emote-swordfight", 5.91),
    (["153", "timejump", "TimeJump"], "emote-timejump", 4.01),
    (["154", "snake", "Snake"], "emote-snake", 5.26),
    (["155", "heart fingers", "Heart Fingers"], "emote-heartfingers", 4.0),
    (["156", "heart shape", "Heart Shape"], "emote-heartshape", 6.23),
    (["157", "hug", "Hug"], "emote-hug", 3.5),
    (["158", "laugh", "Laugh"], "emote-lagughing", 1.13),
    (["159", "eyeroll", "Eyeroll"], "emoji-eyeroll", 3.02),
    (["160", "embarrassed", "Embarrassed"], "emote-embarrassed", 7.414283),
    (["161", "float", "Float"], "emote-float", 8.995302),
    (["162", "telekinesis", "Telekinesis"], "emote-telekinesis", 10.492032),
    (["163", "sexy dance", "Sexy Dance"], "dance-sexy", 12.30883),
    (["164", "puppet", "Puppet"], "emote-puppet", 16.325823),
    (["165", "fighter idle", "Fighter Idle"], "idle-fighter", 17.19123),
    (["166", "penguin dance", "Penguin Dance"], "dance-pinguin", 11.58291),
    (["167", "creepy puppet", "Creepy Puppet"], "dance-creepypuppet", 6.416121),
    (["168", "sleigh", "Sleigh"], "emote-sleigh", 11.333165),
    (["169", "maniac", "Maniac"], "emote-maniac", 4.906886),
    (["170", "energy ball", "Energy Ball"], "emote-energyball", 7.575354),
    (["171", "singing", "Singing"], "idle_singing", 10.260182),
    (["172", "frog", "Frog"], "emote-frog", 14.55257),
    (["173", "superpose", "Superpose"], "emote-superpose", 4.530791),
    (["174", "cute", "Cute"], "emote-cute", 6.170464),
    (["175", "tiktok9", "TikTok Dance 9"], "dance-tiktok9", 11.892918),
    (["176", "weird dance", "Weird Dance"], "dance-weird", 21.556237),
    (["177", "tiktok10", "TikTok Dance 10"], "dance-tiktok10", 8.225648),
    (["178", "pose 7", "Pose 7"], "emote-pose7", 4.655283),
    (["179", "pose 8", "Pose 8"], "emote-pose8", 4.808806),
    (["180", "casual dance", "Casual Dance"], "idle-dance-casual", 9.079756),
    (["181", "pose 1", "Pose 1"], "emote-pose1", 2.825795),
    (["182", "pose 3", "Pose 3"], "emote-pose3", 5.10562),
    (["183", "pose 5", "Pose 5"], "emote-pose5", 4.621532),
    (["184", "cutey", "Cutey"], "emote-cutey", 3.26032),
    (["185", "punk guitar", "Punk Guitar"], "emote-punkguitar", 9.365807),
    (["186", "zombie run", "Zombie Run"], "emote-zombierun", 9.182984),
    (["187", "fashionista", "Fashionista"], "emote-fashionista", 5.606485),
    (["188", "gravity", "Gravity"], "emote-gravity", 8.955966),
    (["189", "ice cream dance", "Ice Cream Dance"], "dance-icecream", 14.769573),
    (["190", "wrong dance", "Wrong Dance"], "dance-wrong", 12.422389),
    (["191", "uwu", "UwU"], "idle-uwu", 24.761968),
    (["192", "tiktok dance 4", "TikTok Dance 4", "sayso"], "idle-dance-tiktok4", 15.500708),
    (["193", "advanced shy", "Advanced Shy"], "emote-shy2", 4.989278),
    (["194", "anime dance", "Anime Dance"], "dance-anime", 8.46671),
    (["195", "kawaii", "Kawaii"], "dance-kawai", 10.290789),
    (["196", "scritchy", "Scritchy"], "idle-wild", 26.422824),
    (["197", "ice skating", "Ice Skating"], "emote-iceskating", 7.299156),
    (["198", "surprise big", "Surprise Big"], "emote-pose6", 5.375124),
    (["199", "celebration step", "Celebration Step"], "emote-celebrationstep", 3.353703),
    (["200", "creepycute", "Creepycute"], "emote-creepycute", 7.902453),
    (["201", "frustrated", "Frustrated"], "emote-frustrated", 5.584622),
    (["202", "pose 10", "Pose 10"], "emote-pose10", 3.989871),
    (["203", "rel", "Rel"], "sit-relaxed", 29.889858),
    (["204", "laidback", "Laid Back"], "sit-open", 24.025963),
    (["205", "star gazing", "Star Gazing"], "emote-stargaze", 1.127464),
    (["206", "slap", "Slap"], "emote-slap", 2.724945),
    (["207", "boxer", "Boxer"], "emote-boxer", 5.555702),
    (["208", "head blowup", "Head Blowup"], "emote-headblowup", 11.667537),
    (["209", "kawaii gogo", "KawaiiGoGo"], "emote-kawaiigogo", 10),
    (["210", "repose", "Repose"], "emote-repose", 1.118455),
    (["211", "tiktok7", "Tiktok7"], "idle-dance-tiktok7", 12.956484),
    (["212", "shrink", "Shrink"], "emote-shrink", 8.738784),
    (["213", "ditzy pose", "Ditzy Pose"], "emote-pose9", 4.583117),
    (["214", "teleporting", "Teleporting"], "emote-teleporting", 11.7676),
    (["215", "touch", "Touch"], "dance-touch", 11.7),
    (["216", "guitar", "Guitar"], "idle-guitar", 12.229398),
    (["217", "this is for you", "This Is For You"], "emote-gift", 5.8),
    (["218", "push it", "Push It"], "dance-employee", 8),
    (["219", "smooch", "Smooch"], "emote-kissing", 5.5),
    (["220", "wop dance", "Wop Dance"], "dance-tiktok11", 9.5),
    (["221", "cute salute", "Cute Salute"], "emote-cutesalute", 3),
    (["222", "at attention", "At Attention"], "emote-salute", 3),
]

# Function to start/stop an emote loop based on user message
async def check_and_start_emote_loop(self: BaseBot, user: User, message: str):
    if user.id == self.user.id:
        return  # Ignore if the command is from the bot itself

    cleaned_msg = message.strip().lower()

    # Stop loop
    if cleaned_msg in ("stop", "/stop", "!stop", "-stop"):
        if user.id in self.user_loops:
            self.user_loops[user.id]["task"].cancel()
            del self.user_loops[user.id]
            await self.highrise.send_whisper(user.id, "⛔ Emote loop stopped. Type any emote name or number to start again.")
        else:
            await self.highrise.send_whisper(user.id, "❌ You don't have an active emote loop.")
        return

    # Match message to emote
    selected = next((e for e in emote_list if cleaned_msg in [a.lower() for a in e[0]]), None)
    if selected:
        aliases, emote_id, duration = selected

        # Cancel existing loop
        if user.id in self.user_loops:
            self.user_loops[user.id]["task"].cancel()

        # Start new loop
        async def emote_loop():
            try:
                while True:
                    if not self.user_loops[user.id]["paused"]:
                        await self.highrise.send_emote(emote_id, user.id)
                    await asyncio.sleep(duration)
            except asyncio.CancelledError:
                pass

        task = asyncio.create_task(emote_loop())
        self.user_loops[user.id] = {
            "paused": False,
            "emote_id": emote_id,
            "duration": duration,
            "task": task
        }

        await self.highrise.send_whisper(
            user.id,
            f"✅ You are now in a loop for emote [{aliases[0]}]. Type 'stop' to end it."
        )

# Handle user movement to pause/resume loop
async def handle_user_movement(bot: BaseBot, user: User, new_position: Position | AnchorPosition):
    if user.id == bot.user.id:
        return  # Don't process bot's own movement

    if user.id not in bot.user_loops:
        return

    if not hasattr(bot, "previous_positions"):
        bot.previous_positions = {}

    prev_pos = bot.previous_positions.get(user.id)

    if prev_pos is None:
        bot.previous_positions[user.id] = new_position
        return

    def position_changed(p1, p2, threshold=0.01):
        return (
            abs(p1.x - p2.x) > threshold or
            abs(p1.y - p2.y) > threshold or
            abs(p1.z - p2.z) > threshold
        )

    if position_changed(prev_pos, new_position):
        bot.previous_positions[user.id] = new_position
        if user.id in bot.user_loops:
            bot.user_loops[user.id]["paused"] = True
    else:
        bot.previous_positions[user.id] = new_position
        if user.id in bot.user_loops:
            bot.user_loops[user.id]["paused"] = False
            



