"""

"The greatest gourd of them all is the gourd yet harvested" 
- Jhon Calender 2137


"""

import time
import random
import math
import backend_handler as bh
from classes import GameDataManager, AudioManager, Color

game_data = GameDataManager()
save_data = game_data.save_data
item_data = game_data.item_data
modifier_data = game_data.modifier_data
relic_data = game_data.relic_data
boss_data = game_data.boss_data

audio = AudioManager()

empty = {
    "": 0,
    "Tag": "Empty"
}

vowels = 'aeio'

gourd_enemies = ("Gourd",
                 "Gourd's Father",
                 "Gourd's Dog",
                 "Gourd's Late Mother",
                 "Gourd's Second Cousin",
                 "Gourd's Yoyo",
                 "Gourd's Pet Rat",
                 "Gourd's Identical Twin",
                 "Gourd's Doppelgänger")

gourd_bosses = []

for boss in boss_data.keys():
    gourd_bosses.append(boss)

def deck_builder():
    while True:
        bh.clear_screen()
        print(Color.HEADER + Color.BOLD + "DECK BUILDER\n" + Color.END)
        available_packs = []
        available_packs_m = []
        for pack_name, pack in save_data["packs"].items():
            if pack["unlocked"]:
                available_packs.append(pack_name)
        for pack_name, pack in save_data["packs_m"].items():
            if pack["unlocked"]:
                available_packs_m.append(pack_name)
        for i in range(len(available_packs) + len(available_packs_m)):
            if i < len(available_packs):
                print(f"{i+1}. {available_packs[i]} Pack {'[ON]' if available_packs[i] in save_data['equipped'] else ''}")
            else:
                print(f"{i+1}. {available_packs_m[i - len(available_packs)]} Pack(M) {'[ON]' if available_packs_m[i - len(available_packs)] in save_data['equipped_m'] else ''}")
        print(f"\nPebble Multiplier: {Color.MULT}X{1 + len(save_data["equipped"]) / 10}{Color.END}")
        print(f"Extra Seeds: {Color.EXTRA}+{math.floor((len(list(i for i in save_data["equipped"])) + len(list(i for i in save_data["equipped_m"]))) / 10)}{Color.END}")
        print(f"{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        if choice.lower() == "exit":
            break
        else:
            try:
                if int(choice) > len(available_packs):
                    game_data.equip_pack_m(available_packs_m[int(choice) - 1 - len(available_packs)])
                elif int(choice) > 0:
                    game_data.equip_pack(available_packs[int(choice) - 1])
            except:
                pass

def shop(listings, m_listing):
    #audio.stop_audio("Town", 100)
    #audio.play_audio("GourdShop", True, 100)
    while True:
        bh.clear_screen()
        print(Color.HEADER + Color.BOLD + "SHOP" + Color.END)
        print(f"{Color.PEBBLE}₲{save_data['statistics']['pebbles']}{Color.END}\n")
        line_1 = ""
        line_2 = ""
        line_1_length = 0
        line_2_length = 0
        for i, (listing, listing_data) in enumerate(listings.items(), start=1):
            listing_text = (f"{i}. {listing} Pack [₲{listing_data['price']}]" if listing_data["purchased"] is False else Color.ITALIC + Color.GRAY + f"{i}. {listing} Pack [Purchased]" + Color.END)
            if i == 1:
                line_1 += listing_text
                line_1_length += len(line_1)
                if listing_data["purchased"]:
                    line_1_length -= len(Color.ITALIC + Color.GRAY + Color.END)
            elif i == 2:
                line_2 += listing_text
                line_2_length += len(line_2)
                if listing_data["purchased"]:
                    line_2_length -= len(Color.ITALIC + Color.GRAY + Color.END)
            elif i == 3:
                if line_2_length > line_1_length:
                    line_1 += " " * (line_2_length - line_1_length)
                else:
                    line_2 += " " * (line_1_length - line_2_length)
                line_1 += "   " + listing_text
        if m_listing:
            listing_text = (f"4. {m_listing['name']} Pack(M) [₲{m_listing['price']}]" if m_listing["purchased"] is False else Color.ITALIC + Color.GRAY + f"4. {m_listing['name']} Pack [Purchased]" + Color.END)
            line_2 += "   " + listing_text
        print(line_1 + "\n")
        print(line_2)
        print(f"\n{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        for i, (listing, listing_data) in enumerate(listings.items(), start=1):
            try:
                if int(choice) > 0 and int(choice) < 4 and int(choice) == i:
                    if listing_data["purchased"] is False and save_data["statistics"]["pebbles"] >= listing_data["price"]:
                        listing_data["purchased"] = True
                        game_data.add_pebbles(-listing_data["price"])
                        game_data.unlock_pack(listing)
            except:
                pass
        try:
            if int(choice) == 4 and m_listing:
                if m_listing["purchased"] is False and save_data["statistics"]["pebbles"] >= m_listing["price"]:
                    m_listing["purchased"] = True
                    game_data.add_pebbles(-m_listing["price"])
                    game_data.unlock_pack_m(m_listing["name"])
        except:
            pass
        if choice.lower() == "exit":
            break

    #audio.stop_audio("GourdShop", 500)

def encyclopedia():
    while True:
        bh.clear_screen()
        print(Color.HEADER + Color.BOLD + "ENCYCLOPEDIA\n" + Color.END)
        print("1. Item Packs\n2. Modifier Packs [WIP]")
        print(f"{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        if choice == "1":
            inner_encyclopedia(True)
        elif choice == "2":
            inner_encyclopedia(False)
        elif choice.lower() == "exit":
            break

def inner_encyclopedia(item : bool):
    while True:
        bh.clear_screen()
        pack_unlocked = {}
        for i, (pack_name, pack_data) in enumerate((item_data.items() if item else modifier_data.items()), start=1):
            if (save_data["packs"][pack_name]["unlocked"] if item else save_data["packs_m"][pack_name]["unlocked"]):
                print(f"{i}. {pack_name} Pack")
                pack_unlocked[i] = (True, pack_data)
            else:
                print(f"{i}. ???")
                pack_unlocked[i] = (False, pack_data)
        print(f"{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        if choice.lower() == "exit":
            break
        else:
            try:
                if pack_unlocked[int(choice)][0]:
                    while True:
                        bh.clear_screen()
                        for thing_name, thing in pack_unlocked[int(choice)][1].items():
                            if item:
                                print(Color.BOLD + Color.HEADER + f"{thing_name}" + Color.END + f"\nDamage: {thing['Damage'] if save_data['items'][thing_name]['used'] else '?'}\nLore: {thing['Lore']}\n")
                            else:
                                print(Color.BOLD + Color.HEADER + f"{thing_name}" + Color.END + f"\nValue: {thing['Value'] if save_data['modifiers'][thing_name]['used'] else '?'}\nTag: {thing['Tag']}\nLore: {thing['Lore']}\n")
                            time.sleep(0.01)
                        choice = input()
            except:
                pass

def altar():
    while True:
        bh.clear_screen()
        print(Color.HEADER + Color.BOLD + "THE ALTAR\n" + Color.END)
        for i, (name, data) in enumerate(relic_data.items(), start=1):
            if name in save_data["equipped_r"]:
                print(f"{Color.BOLD}{Color.RAINBOW(f'{i}. Relic of {name}')}")
                print(f"   {Color.ITALIC}{data['Lore']}{Color.END}\n")
            elif save_data["relics"][name]["unlocked"] is True:
                print(f"{i}. Relic of {name}")
                print(f"   {Color.GRAY}{Color.ITALIC}{data['Lore']}{Color.END}\n")
            else:
                print(f"{Color.GRAY}{Color.ITALIC}{i}. Relic of {name} [LOCKED]{Color.END}")
                print(f"   {Color.GRAY}{Color.ITALIC}{data['Unlock']}{Color.END}\n")
        print(f"Pebble Multiplier: {Color.MULT}X{len(save_data['equipped_r']) + 1}{Color.END}")
        print(f"[{len(save_data['equipped_r'])}/1] Equipped")
        print(f"{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        for i, (name, data) in enumerate(relic_data.items(), start=1):
            try:
                if int(choice) == i:
                    if name in save_data["equipped_r"]:
                        game_data.equip_relic(name)
                    elif len(save_data["equipped_r"]) > 0:
                        pass
                    elif save_data["relics"][name]["unlocked"]:
                        game_data.equip_relic(name)
            except:
                pass
        if choice.lower() == "exit":
            break

def statistics():
    while True:
        bh.clear_screen()
        print(f"{Color.BOLD}{Color.HEADER}Stats{Color.END}")
        print(f"\nGourd Pebbles:\n{save_data['statistics']['pebbles']}")
        print(f"\nGourd Seeds:\n{save_data['statistics']['seeds']}")
        print(f"\nTotal Rolls:\n{save_data['statistics']['total rolls']}")
        print(f"\n{Color.BOLD}{Color.HEADER}Bosses{Color.END}")
        for boss, temp_data in save_data["bosses"].items():
            print(f"\n{boss if temp_data['kills'] > 0 else f'{Color.GRAY}{Color.ITALIC}???{Color.END}'}")
            print(f"""{f"{Color.GRAY}{Color.ITALIC}{boss_data[boss]['Lore']}{Color.END}" if temp_data["kills"] > 0 else f"{Color.GRAY}{Color.ITALIC}???{Color.END}"}""")
            print(f"{Color.GRAY}{Color.ITALIC}Defeated: {temp_data['kills']}{Color.END}")
        print(f"{Color.GRAY}{Color.ITALIC}Type 'exit' to leave{Color.END}")
        choice = input(">")
        if choice.lower() == "exit":
            break

def run():
    bh.clear_screen()
    while True:
        audio.stop_audio("GourdEnd", 500)
        audio.play_audio("Town", True, 500)

        total_boss_defeats = 0
        for boss in save_data["bosses"].values():
            total_boss_defeats += boss["kills"]

        shop_packs = {}
        available_packs = []
        available_packs_m = []
        for pack in save_data["packs"]:
            if save_data["packs"][pack]["unlocked"] is False:
                available_packs.append(pack)
        for pack in save_data["packs_m"]:
            if save_data["packs_m"][pack]["unlocked"] is False:
                available_packs_m.append(pack)
        for i in range(3):
            while True:
                if len(available_packs) > 0:
                    pack_select = random.choice(available_packs)
                    if pack_select not in shop_packs:
                        shop_packs[pack_select] = {
                            "purchased": False,
                            "price": random.randint(100, 150)
                        }
                        break
                if i >= len(available_packs):
                    string = random.choices('!"#¤%&/()=?1234567890@£$€{[]}+', k=random.randint(3, 10))
                    shop_packs["".join(string)] = {
                        "purchased": True,
                        "price": 0
                    }
                    break
        string = random.choices('!"#¤%&/()=?1234567890@£$€{[]}+', k=random.randint(3, 10))
        tied_string = "".join(string)
        modifier_pack = ({"name": random.choice(available_packs_m), "purchased": False, "price": random.randint(150, 250)} if len(available_packs_m) > 0 else
                        {"name": tied_string, "purchased": True, "price": 0})

        while True:
            game_data.save()
            if len(save_data["equipped"]) >= 1 and len(save_data["equipped_m"]) >= 1:
                rollable = True
            else:
                rollable = False
            if len(save_data["equipped_r"]) > 0:
                if len(save_data["equipped"]) >= 3 and len(save_data["equipped_m"]) >= 1:
                    rollable = True
                else:
                    rollable = False
            bh.clear_screen()
            stats_bar = f"|| {Color.PEBBLE}₲{save_data['statistics']['pebbles']}{Color.END} | {Color.SEED}{save_data['statistics']['seeds']} Gourd Seeds{Color.END} ||"
            print("—" * (len(stats_bar) - 29))
            print(stats_bar)
            print("—" * (len(stats_bar) - 29))
            print("\n" + Color.HEADER + Color.BOLD + "GOURD TOWN" + Color.END + "\n")
            print("1. Roll")
            print("2. Deck Builder")
            print("3. Shop")
            print("4. Encyclopedia")
            print(Color.GRAY + Color.ITALIC + "5. Endings [WIP]" + Color.END)
            print(Color.GRAY + Color.ITALIC + "6. Farm [WIP]" + Color.END)
            if total_boss_defeats >= 3:
                print("7. The Altar")
            else:
                print(Color.GRAY + Color.ITALIC + "7. The Altar" + Color.END)
            print("8. Statistics")
            if rollable is False:
                if len(save_data["equipped_r"]) > 0:
                    print(f"\n{Color.GRAY}{Color.ITALIC}You need at least 3 Item Packs and 1 Modifier Pack equipped to roll when using a Relic{Color.END}\n")
                else:
                    print(f"\n{Color.GRAY}{Color.ITALIC}You need at least 1 Item Pack and 1 Modifier Pack equipped to roll{Color.END}\n")
            choice = input(">")

            if choice == "1":
                if rollable:
                    break
            elif choice == "2":
                deck_builder()
            elif choice == "3":
                shop(shop_packs, modifier_pack)
            elif choice == "4":
                encyclopedia()
            elif choice == "5":...
            elif choice == "6":...
            elif choice == "7" and total_boss_defeats >= 3:
                altar()
            elif choice == "8":
                statistics()

        audio.stop_audio("Town", 500)

        current_pebbles = 0
        current_seeds = 0
        rolls = 0
        weapon_amount = 4
        modifier_chance = 5

        non_modifier_streak = 0

        mess_king_repeat = 0

        if "The Empty" in save_data["equipped_r"]:
            weapon_amount -= 1

        if "Broken Chains" in save_data["equipped_r"]:
            weapon_amount += 2

        if "Change" in save_data["equipped_r"]:
            modifier_chance = 2

        while True:
            if rolls == 30:
                game_data.unlock_relic("The Empty")

            if non_modifier_streak == 5:
                game_data.unlock_relic("Change")

            bh.clear_screen()
            if rolls > 0 and rolls % 5 == 0:
                bh.timed_print("Do you which to leave with all your scavenged loot? (Y / N)")
                choice = input(">")
                if choice.lower() == "y":

                    audio.play_audio("GourdYes")
                    game_data.add_pebbles(current_pebbles)
                    game_data.add_seeds(current_seeds)
                    bh.clear_screen()
                    bh.slow_text("You return safely back to Town.")
                    time.sleep(1)
                    bh.timed_print(f"+ {Color.PEBBLE}₲{current_pebbles}{Color.END}", 500)
                    bh.timed_print(f"+ {Color.SEED}{current_seeds} Gourd Seeds{Color.END}\n", 500)
                    print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
                    input()
                    break
                bh.clear_screen()
                audio.play_audio("GourdNo")

            if (rolls + 1) % 10 != 0:
                current_gourd = random.choice(gourd_enemies)
            else:
                current_gourd = random.choice(gourd_bosses)
                if current_gourd == "Mess King":
                    mess_king_repeat = 2

            if mess_king_repeat >= 1:
                mess_king_repeat -= 1
                current_gourd = "Mess King"

            if current_gourd != "Mess King":
                full_picks = []
                for pack in save_data["equipped"]:
                    for weapon_name, weapon_obj in item_data[pack].items():
                        full_picks.append((weapon_name, weapon_obj))

                full_picks_m = []
                for pack in save_data["equipped_m"]:
                    for modifier_name, modifier_obj in modifier_data[pack].items():
                        full_picks_m.append((modifier_name, modifier_obj))
            else:
                full_picks = []
                for pack in item_data.keys():
                    for weapon_name, weapon_obj in item_data[pack].items():
                        full_picks.append((weapon_name, weapon_obj))

                full_picks_m = []
                for pack in modifier_data.keys():
                    for modifier_name, modifier_obj in modifier_data[pack].items():
                        full_picks_m.append((modifier_name, modifier_obj))

            if len(save_data["equipped"]) + len(save_data["equipped_m"]) == len(item_data.keys()) + len(modifier_data.keys()):
                full_picks.append((f"{Color.RAINBOW('???')}", { "Damage": 50, "Lore": "..." }))

            # Weapon/modifier picking logic for gourd

            repeat = 1

            total_damage = 0
            g_total_damage = 0
            g_weapon_name = ""

            g_weapon_amount = 1

            minimum_damage = -999

            if current_gourd == "Devouring Gourd":
                minimum_damage = 8
                g_weapon_amount = 4
                repeat = 4

            if "The Sisters" in save_data["equipped_r"]:
                g_weapon_amount += 1

            if "Broken Chains" in save_data["equipped_r"]:
                minimum_damage = 13

            for i in range(g_weapon_amount):
                while True:
                    g_weapon_pick_name, g_weapon_pick = random.choice(full_picks)
                    if g_weapon_pick["Damage"] >= minimum_damage:
                        break

                if random.uniform(0, modifier_chance) <= 1:
                    g_modifier_name, g_modifier = random.choice(full_picks_m)
                else:
                    g_modifier_name, g_modifier = ("", empty)

                if "The Sisters" in save_data["equipped_r"]:
                    g_modifier_name, g_modifier = ("", empty)

                g_damage = bh.estimate_damage(g_modifier, g_weapon_pick)
                if g_modifier["Tag"] == "Spec":
                    g_damage = bh.special_weapon(g_modifier_name, g_weapon_pick)

                g_total_damage += g_damage

                if current_gourd == "Black Hole":
                    g_modifier_name, g_modifier = ("", empty)
                    g_weapon_pick_name = Color.RAINBOW("??? (50)")
                    g_total_damage = 50
                    repeat = 5

                g_weapon_name_full = (f"""{f"{Color.GRAY}{Color.ITALIC}???{Color.END}" if "The Blind" in save_data["equipped_r"] else f"{Color.BOLD}{Color.HEADER}{g_modifier_name}"} """ if g_modifier_name else f"{Color.BOLD}{Color.HEADER}") + f"{g_weapon_pick_name}{Color.END}"
                if g_modifier_name == "":
                    g_weapon_prefix = " an " if g_weapon_pick_name[0].lower() in vowels else " a "
                else:
                    g_weapon_prefix = " an " if g_modifier_name[0].lower() in vowels else " a "

                if i != 0:
                    g_weapon_name += " and"

                g_weapon_name += g_weapon_prefix + g_weapon_name_full
                    
            bh.clear_screen()
            bh.timed_print(f"{Color.BOLD}ROLL {rolls + 1}{Color.END}\n")
            audio.play_audio("GourdBallRoll")
            bh.timed_print("The Ball is rolling", 3000)
            audio.play_audio("GourdBallRoll")
            bh.timed_print("The Ball continues to roll", 3000)
            audio.play_audio("GourdHit")
            bh.timed_print(f"The Ball has collided with the {current_gourd}", 2000)
            audio.play_audio("GourdFinalWeapon")
            bh.timed_print(f"The {current_gourd} attacks you with{g_weapon_name}\n")

            for _ in range(repeat):
                # Weapon/modifier picking logic for player
                weapon_picks = []
                modifier_picks = [random.choice(full_picks_m) if random.uniform(0, modifier_chance) <= 1 else ("", empty) for i in range (weapon_amount)]
                for i in range(weapon_amount):
                    while True:
                        pick = random.choice(full_picks)
                        if pick not in weapon_picks:
                            weapon_picks.append(pick)
                            break

                weapon_damages = []
                weapon_names = []
                weapon_m_names = []
                
                for i, ((modifier_name, modifier), (weapon_name, weapon)) in enumerate(zip(modifier_picks, weapon_picks), start=1):
                    audio.play_audio("GourdWeaponSelect")
                    bh.timed_print(f"{i}. " + (f"""{f"{Color.GRAY}{Color.ITALIC}???{Color.END}" if "The Blind" in save_data["equipped_r"] else modifier_name} """ if modifier_name else "") + weapon_name, 500)
                    damage = bh.estimate_damage(modifier, weapon)
                    if modifier["Tag"] == "Spec":
                        damage = bh.special_weapon(modifier_name, weapon)
                    weapon_damages.append(damage)
                    weapon_names.append(weapon_name)
                    weapon_m_names.append(modifier_name)

                highest_damage = max(weapon_damages)
                lowest_damage = min(weapon_damages)

                sorted_values = weapon_damages.copy()
                sorted_values.sort()
                allowed_values = []
                for v in sorted_values:
                    if v > g_damage:
                        allowed_values.append(v)

                while True:
                    choice = input("\n>")
                    try:
                        if int(choice) > 0 and int(choice) < weapon_amount + 1:
                            damage = weapon_damages[int(choice) - 1]
                            weapon_name = weapon_names[int(choice) - 1]
                            if weapon_m_names[int(choice) - 1] != "":
                                modifier_name = weapon_m_names[int(choice) - 1] + " "
                            else:
                                modifier_name = ""

                            match int(choice):
                                case 1:
                                    audio.play_audio("One")
                                case 2:
                                    audio.play_audio("Two")
                                case 3:
                                    audio.play_audio("Three")
                                case 4:
                                    audio.play_audio("Four")
                                case 5:
                                    audio.play_audio("Five")
                                case 6:
                                    audio.play_audio("Six")
                                case 7:
                                    audio.play_audio("Seven")
                                case 8:
                                    audio.play_audio("Eight")
                                case 9:
                                    audio.play_audio("Nine")
                                case 10:
                                    audio.play_audio("Ten")
                            break
                    except:
                        pass

                total_damage += damage
                if damage >= 50 and current_gourd in gourd_bosses:
                    game_data.unlock_relic("The Blind")
            
                game_data.used_item(weapon_picks[int(choice) - 1][0])

                if modifier_name == "":
                    non_modifier_streak += 1
                else:
                    non_modifier_streak = 0

            damage = total_damage
            time.sleep(1)
            audio.play_audio("GourdSwing")
            bh.timed_print(f"You swing at the {current_gourd} with the " + Color.BOLD + f"""{f"{Color.GRAY}{Color.ITALIC}??? {Color.END}" if "The Blind" in save_data["equipped_r"] and modifier_name != "" else modifier_name}{weapon_name}""" + Color.END)
            if "Golden" in modifier_name:
                mult = random.uniform(1.1, 1.5)
            elif "Midas" in modifier_name:
                mult = random.uniform(1.5, 2.0)
            else:
                mult = 1
            new_pebbles = int(random.randint(10,20) * mult * (1 + len(save_data["equipped"]) / 10))
            new_seeds = 1 + math.floor((len(list(i for i in save_data["equipped"])) + len(list(i for i in save_data["equipped_m"]))) / 10)
            if "Lucky" in modifier_name and random.randint(0,1) == 0:
                new_seeds += 1

            if "Greed" in save_data["equipped_r"]:
                new_seeds = 0
                new_pebbles *= 2

            if len(allowed_values) > 1:
                if damage == allowed_values[0]:
                    new_pebbles *= 1.5

            new_pebbles *= 1 + (math.floor((rolls + 1) / 10) / 10)

            new_seeds += math.floor((rolls + 1) / 20)

            new_pebbles = int(new_pebbles * (len(save_data["equipped_r"]) + 1))

            if new_seeds >= 5:
                game_data.unlock_relic("Greed")

            if ("Holy" in modifier_name and "Unholy" in g_modifier_name) and current_gourd not in gourd_bosses:
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Holy Damage!{Color.END}", 2000)
                bh.timed_print("It was enough to make an escape", 1500)
                audio.play_audio("GourdBag")
                bh.timed_print(f"Whilst running away you manage to gather {Color.PEBBLE}₲{new_pebbles}{Color.END} and {Color.SEED}{new_seeds} Gourd Seed" + ("s" if new_seeds > 1 else "") + Color.END, 2000)
                current_pebbles += new_pebbles
                current_seeds += new_seeds

            elif ("Unholy" in modifier_name and "Holy" in g_modifier_name) and current_gourd not in gourd_bosses:
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Unholy Damage!{Color.END}", 2000)
                bh.timed_print(f"The {current_gourd} stands Holy", 1500)
                bh.timed_print(f"You get stabbed right in the heart by{g_weapon_name}", 2000)
                game_data.add_pebbles(int(current_pebbles / 2))
                print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
                audio.play_audio("GourdEnd", True)
                input()
                bh.defeated(current_pebbles)
                break

            elif "Hyperdense" in modifier_name and damage < 10 and current_gourd not in gourd_bosses:
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Dense Damage!{Color.END}", 2000)
                bh.timed_print("It was enough to make an escape", 1500)
                audio.play_audio("GourdBag")
                bh.timed_print(f"Whilst running away you manage to gather {Color.PEBBLE}₲{new_pebbles}{Color.END} and {Color.SEED}{new_seeds} Gourd Seed" + ("s" if new_seeds > 1 else "") + Color.END, 2000)
                current_pebbles += new_pebbles
                current_seeds += new_seeds

            elif "Hyperdense" in modifier_name and damage >= 10 and current_gourd not in gourd_bosses:
                bh.timed_print("You barely swung your weapon, it was too heavy", 2000)
                bh.timed_print(f"You get stabbed right in the heart by{g_weapon_name}", 2000)
                game_data.add_pebbles(int(current_pebbles / 2))
                print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
                audio.play_audio("GourdEnd", True)
                input()
                bh.defeated(current_pebbles)
                break

            elif "Holographic" in modifier_name and damage >= 10 and current_gourd not in gourd_bosses:
                bh.timed_print(f"Your terrifying weapon scared away the {current_gourd}", 2000)
                audio.play_audio("GourdBag")
                bh.timed_print(f"Whilst running away you manage to gather {Color.PEBBLE}₲{new_pebbles}{Color.END} and {Color.SEED}{new_seeds} Gourd Seed" + ("s" if new_seeds > 1 else "") + Color.END, 2000)
                current_pebbles += new_pebbles
                current_seeds += new_seeds

            elif "Holographic" in modifier_name and damage < 10 and current_gourd not in gourd_bosses:
                bh.timed_print(f"Your weapon passes right through the {current_gourd}, as it doesn't have a hitbox", 2000)
                bh.timed_print(f"You get stabbed right in the heart by{g_weapon_name}", 2000)
                game_data.add_pebbles(int(current_pebbles / 2))
                print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
                audio.play_audio("GourdEnd", True)
                input()
                bh.defeated(current_pebbles)
                break

            elif highest_damage < g_total_damage and lowest_damage == damage and repeat == 1:
                new_pebbles = 0
                new_seeds = 0
                bh.timed_print(f"The {current_gourd} dodges", 2000)
                bh.timed_print("They decide to spare you", 1500)
                bh.timed_print("You run away without any rewards", 2000)

            elif damage > g_total_damage:
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Damage!{Color.END}", 2000)
                bh.timed_print("It was enough to make an escape", 1500)
                audio.play_audio("GourdBag")
                bh.timed_print(f"Whilst running away you manage to gather {Color.PEBBLE}₲{new_pebbles}{Color.END} and {Color.SEED}{new_seeds} Gourd Seed" + ("s" if new_seeds > 1 else "") + Color.END, 2000)
                if current_gourd in gourd_bosses and mess_king_repeat == 0:
                    save_data["bosses"][current_gourd]["kills"] += 1
                current_pebbles += new_pebbles
                current_seeds += new_seeds

            elif damage < g_total_damage:
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Damage!{Color.END}", 2000)
                bh.timed_print(f"The {current_gourd} stands unfaced", 1500)
                bh.timed_print(f"You get stabbed right in the heart by{g_weapon_name}", 2000)
                game_data.add_pebbles(int(current_pebbles / 2))
                print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
                audio.play_audio("GourdEnd", True)
                input()
                bh.defeated(current_pebbles)
                break

            else:
                new_pebbles = int(new_pebbles / 1.5)
                new_seeds = 0
                bh.timed_print(f"You dealt {Color.DAMAGE}{damage:.1f} Damage!{Color.END}", 2000)
                bh.timed_print(f"But so did the {current_gourd}", 1500)
                bh.timed_print("You have earned their respect for now", 2000)
                audio.play_audio("GourdBag")
                bh.timed_print(f"Whilst leaving you pick up {Color.PEBBLE}₲{new_pebbles}{Color.END} from the ground", 2000)
                current_pebbles += new_pebbles

            print(Color.ITALIC + Color.GRAY + "(Press 'enter' to continue)" + Color.END)
            input()

            rolls += 1
            game_data.add_rolls(1)
            game_data.save()
        game_data.save()

if __name__ == "__main__":
    run()
