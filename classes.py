import json
import os
import random
import pygame
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GameDataManager:
    def __init__(self):
        self.save_path = os.path.join(BASE_DIR, "save_data.json")
        self.item_path = os.path.join(BASE_DIR, "item_packs.json")
        self.modifier_path = os.path.join(BASE_DIR, "modifier_packs.json")
        self.relic_path = os.path.join(BASE_DIR, "relic_items.json")
        self.boss_path = os.path.join(BASE_DIR, "bosses.json")
        self.seed_path = os.path.join(BASE_DIR, "seeds.json")
        self.upgrade_path = os.path.join(BASE_DIR, "upgrades.json")
        self.save_data = self._load_save_data()
        self.item_data = self._load_item_data()
        self.modifier_data = self._load_modifier_data()
        self.relic_data = self._load_relic_data()
        self.boss_data = self._load_boss_data()
        self.seed_data = self._load_seed_data()
        self.upgrade_data = self._load_upgrade_data()
        self._merge_missing_categories()
        self._merge_missing_items()
        self._merge_missing_modifiers()
        self._merge_missing_relics()
        self._merge_missing_bosses()
        self._merge_missing_upgrades()

        self.save_data["packs"]["Beginner"]["unlocked"] = True
        self.save_data["packs_m"]["Beginner"]["unlocked"] = True

    def _load_save_data(self):
        with open(self.save_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_item_data(self):
        with open(self.item_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_modifier_data(self):
        with open(self.modifier_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_relic_data(self):
        with open(self.relic_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_boss_data(self):
        with open(self.boss_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_seed_data(self):
        with open(self.seed_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def _load_upgrade_data(self):
        with open(self.upgrade_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _merge_missing_categories(self):

        # Statistics Section
        if "statistics" not in self.save_data:
            self.save_data["statistics"] = { }

        statistics_parts = ["pebbles", "seeds", "total rolls", "wins", "mass"]

        for stat in statistics_parts:
            if stat not in self.save_data["statistics"]:
                self.save_data["statistics"][stat] = 0

        # List Sections
        list_parts = ["equipped", "equipped_m", "equipped_r", "seeds"]

        for part in list_parts:
            if part not in self.save_data:
                self.save_data[part] = []

        # Dictionary Sections
        dictionary_parts = ["packs", "packs_m", "items", "modifiers", "relics", "bosses", "upgrade_boards"]

        for part in dictionary_parts:
            if part not in self.save_data:
                self.save_data[part] = {}

        # Farmlands Section
        if "farmlands" not in self.save_data:
            self.save_data["farmlands"] = {
                i+1: {
                    "unlocked": False,
                    "seed": None,
                    "time": None
                } for i in range(4)
            }

        self.save_data["farmlands"]["1"]["unlocked"] = True

    def _merge_missing_items(self):
        for pack in self.item_data:
            if pack not in self.save_data["packs"]:
                self.save_data["packs"][pack] = {"unlocked": False}
            for item in self.item_data[pack]:
                if item not in self.save_data["items"]:
                    self.save_data["items"][item] = {"used": False}
        self.save()

    def _merge_missing_modifiers(self):
        for pack in self.modifier_data:
            if pack not in self.save_data["packs_m"]:
                self.save_data["packs_m"][pack] = {"unlocked": False}
            for modifier in self.modifier_data[pack]:
                if modifier not in self.save_data["modifiers"]:
                    self.save_data["modifiers"][modifier] = {"used": False}
        self.save()

    def _merge_missing_relics(self):
        for relic in self.relic_data:
            if relic not in self.save_data["relics"]:
                self.save_data["relics"][relic] = {"unlocked": False}

    def _merge_missing_bosses(self):
        for boss in self.boss_data:
            if boss not in self.save_data["bosses"]:
                self.save_data["bosses"][boss] = {"kills": 0}

    def _merge_missing_upgrades(self):
        for upgrade_board in self.upgrade_data:
            if upgrade_board not in self.save_data["upgrade_boards"]:
                self.save_data["upgrade_boards"][upgrade_board] = {}
            for upgrade in self.upgrade_data[upgrade_board]:
                if upgrade not in self.save_data["upgrade_boards"][upgrade_board]:
                    self.save_data["upgrade_boards"][upgrade_board][upgrade] = {"bought": 0}

    def save(self):
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.save_data, f, indent=4)

    def unlock_pack(self, pack):
        self.save_data["packs"][pack]["unlocked"] = True

    def unlock_pack_m(self, pack):
        self.save_data["packs_m"][pack]["unlocked"] = True

    def unlock_relic(self, relic):
        self.save_data["relics"][relic]["unlocked"] = True

    def equip_pack(self, pack):
        if pack in self.save_data["equipped"]:
            self.save_data["equipped"].remove(pack)
        elif self.save_data["packs"][pack]["unlocked"] is True and pack not in self.save_data["equipped"]:
            self.save_data["equipped"].append(pack)
        self.save()

    def equip_pack_m(self, pack):
        if pack in self.save_data["equipped_m"]:
            self.save_data["equipped_m"].remove(pack)
        elif self.save_data["packs_m"][pack]["unlocked"] is True and pack not in self.save_data["equipped_m"]:
            self.save_data["equipped_m"].append(pack)
        self.save()

    def equip_relic(self, relic):
        if relic in self.save_data["equipped_r"]:
            self.save_data["equipped_r"].remove(relic)
        elif self.save_data["relics"][relic]["unlocked"] is True and relic not in self.save_data["equipped_r"]:
            self.save_data["equipped_r"].append(relic)
        self.save()

    def add_seed(self, seed):
        seed = seed.capitalize()
        if seed in self.seed_data:
            self.save_data["seeds"].append(seed)
        self.save()

    def remove_seed(self, seed):
        seed = seed.capitalize()
        if seed in self.save_data["seeds"]:
            self.save_data["seeds"].remove(seed)
        self.save()

    def plant_seed(self, seed, plot):
        seed = seed.capitalize()
        if seed in self.save_data["seeds"] and self.save_data["farmlands"][str(plot)]["seed"] == None and self.save_data["farmlands"][str(plot)]["unlocked"] == True:
            self.save_data["farmlands"][str(plot)]["seed"] = seed
            self.save_data["farmlands"][str(plot)]["time"] = time.time()
            self.remove_seed(seed)
            return True
        else:
            return False
        
    def unplant_seed(self, plot):
        if self.save_data["farmlands"][str(plot)]["seed"] != None:
            self.save_data["farmlands"][str(plot)]["seed"] = None
            self.save_data["farmlands"][str(plot)]["time"] = 0
            self.save()

    def harvest_seed(self, plot):
        if self.save_data["farmlands"][str(plot)]["seed"] != None:
            time_taken = time.time() - self.save_data["farmlands"][str(plot)]["time"]
            if time_taken > self.seed_data[self.save_data["farmlands"][str(plot)]["seed"]]["Time"]:
                self.add_mass(self.seed_data[self.save_data["farmlands"][str(plot)]["seed"]]["Mass"])
                self.save_data["farmlands"][str(plot)]["seed"] = None
                self.save_data["farmlands"][str(plot)]["time"] = 0
                self.save()
                return True
            else:
                return False

    def unlock_farmland(self, plot):
        self.save_data["farmlands"][str(plot)]["unlocked"] = True
        self.save()

    def buy_upgrade(self, board, upgrade, price):
        if self.save_data["upgrade_boards"][board][upgrade]["bought"] != self.upgrade_data[board][upgrade]["Max"]:
            self.save_data["upgrade_boards"][board][upgrade]["bought"] += 1
            self.add_mass(-price)
        self.save()

    def used_item(self, item):
        self.save_data["items"][item]["used"] = True

    def used_modifier(self, modifier):
        self.save_data["modifiers"][modifier]["used"] = True

    def add_pebbles(self, amount):
        self.save_data["statistics"]["pebbles"] += amount

    def add_seeds(self, amount):
        self.save_data["statistics"]["seeds"] += amount

    def add_rolls(self, amount):
        self.save_data["statistics"]["total rolls"] += amount

    def add_wins(self, amount):
        self.save_data["statistics"]["wins"] += amount

    def add_mass(self, amount):
        self.save_data["statistics"]["mass"] += amount

class AudioManager:
    def __init__(self):
        self.audio_path = os.path.join(BASE_DIR, "audio")
        pygame.mixer.init()
        self.sounds = {}
        self._populate_audio()

    def _populate_audio(self):
        for file in os.listdir(self.audio_path):
            if file.lower().endswith((".wav",".mp3",".ogg")):
                name = os.path.splitext(file)[0].lower()
                path = os.path.join(self.audio_path, file)
                self.sounds[name] = pygame.mixer.Sound(path)
        print(f"Loaded {len(self.sounds)} sounds from '{self.audio_path}'")

    def play_audio(self, name, loop=False, fade_ms=0):
        """
        Plays an audio file from the "audio" folder without the extension (ex. ".wav", ".mp3")

        Loop makes the audio loop

        Fade_ms changes how long it takes for the audio to fully kick in, in ms
        """
        sound = self.sounds.get(name.lower())
        if sound:
            if loop:
                sound.play(loops=-1, fade_ms=fade_ms)
            else:
                sound.play(loops=0, fade_ms=fade_ms)

    def stop_audio(self, name, fade_ms=0):
        """
        Stops currently playing audio, the audio is specified without extension (ex. ".wav", ".mp3")

        Fade_ms change how long it takes for the audio to fully dissapear, in ms
        """
        sound = self.sounds.get(name.lower())
        if sound:
            sound.fadeout(fade_ms)

class Color:
    BOLD = "\033[1m"
    END = "\033[0m"
    HEADER = '\033[37m'
    GRAY = '\033[90m'
    ITALIC = '\033[3m'

    PEBBLE = '\033[38:5:214m'
    SEED = '\033[38:5:70m'
    MASS = '\033[38:5:62m'
    DAMAGE = '\033[48:5:88m'
    MULT = '\033[48:5:53m'
    EXTRA = '\033[48:5:63m'

    SPROUT = '\033[38:5:107m'
    VINE = '\033[38:5:34m'
    BLOSSOM = '\033[38:5:211m'
    #???
    GOURD = '\033[38:5:202m'

    @staticmethod
    def RAINBOW(text, start=-1):
        rainbow_parts = ["\033[38:5:196m", #RED
                     "\033[38:5:202m", #RED-ORANGE
                     "\033[38:5:208m", #ORANGE
                     "\033[38:5:214m", #ORANGE-YELLOW
                     "\033[38:5:226m", #YELLOW
                     "\033[38:5:154m", #YELLOW-GREEN
                     "\033[38:5:46m", #GREEN
                     "\033[38:5:48m", #GREEN-CYAN
                     "\033[38:5:51m", #CYAN
                     "\033[38:5:33m", #CYAN-BLUE
                     "\033[38:5:21m", #BLUE
                     "\033[38:5:57m", #BLUE-PURPLE
                     "\033[38:5:93m", #PURPLE
                     "\033[38:5:129m", #PURPLE-PINK
                     "\033[38:5:201m", #PINK
                     "\033[38:5:198m"] #PINK-RED

        final_text = ""

        if start == -1:
            start = random.randint(0, len(rainbow_parts) - 1)

        for i, char in enumerate(text):
            final_text += rainbow_parts[(start + i) % len(rainbow_parts)] + char

        return final_text + "\033[0m"
