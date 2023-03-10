'''
Program realized by :
Chailloleau Leclerc Théodore,
Valentin Johan
in class of TG4.
'''
import pygame
from random import random, randint, uniform
from time import monotonic




# to transform an image in a python script (to adapt) :
# https://tiplanet.org/forum/img2calc.php




# to download a file on the calculator :
# https://yaya-cout.github.io/Numworks-connector/#/


# variables of the level
# number of tiles to change (here from 00.png to 26.png) 27 in total !!
GLOBAL_FPS = 60
NB_TILES = 666
TILE_SIZE = 50   # definition of the drawing (square)
length = 10       # height of the level
width = 10       # length of the level
tiles = []       # list of tiles images
clock = pygame.time.Clock()


# definition of the level

# the tiles number
level = [[23,  24,  24,  24,  24,  203, 108, 108, 108, 206],
         [46,  47,  47,  47,  47,  222, 30,  31,  32,  222],
         [46,  47,  47,  47,  47,  270, 76,  77,  78,  270],
         [189, 189, 124, 189, 189, 189, 189, 189, 194, 48],
         [46,  47,  187, 47,  47,  47,  47,  47,  47,  48],
         [46,  118, 217, 120, 47,  47,  47,  47,  47,  48],
         [46,  141, 142, 143, 47,  47,  47,  47,  47,  48],
         [46,  164, 165, 166, 47,  47,  47,  47,  47,  48],
         [506, 507, 507, 507, 507, 507, 507, 507, 507, 508],
         [529, 486, 486, 486, 486, 486, 486, 486, 486, 531]]




# the additional infos (trees,...)
decor = [[0,   0,   253, 0,   295, 0,   112, 0,   0,   0],
         [0,   0,   0,   0,   295, 0,   0,   0,   0,   0],
         [0,   0,   0,   0,   295, 0,   0,   0,   0,   0],
         [0,   0,   0,   0,   318, 273, 319, 273, 319, 273],
         [184, 0,   0,   138, 0,   278, 279, 0,   0,   0],
         [0,   0,   0,   0,   0,   276, 277, 0,   0,   0],
         [0,   0,   0,   0,   0,   299, 300, 0,   0,   0],
         [186, 0,   0,   0,   0,   0,   0,   0,   0,   0],
         [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
         [0,   0,   0,   0,   0,   0,   0,   0,   0,   0]]

# collisions with the decor
collisions = [[0,  0,  1,  0,  0,  1,  1,  1,  1,  1],
              [0,  0,  0,  0,  0,  1,  0,  0,  0,  1],
              [0,  0,  0,  0,  0,  1,  0,  0,  0,  1],
              [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [1,  0,  0,  1,  0,  1,  1,  0,  0,  0],
              [0,  0,  0,  0,  0,  1,  1,  0,  0,  0],
              [0,  0,  0,  0,  0,  1,  1,  0,  0,  0],
              [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [0,  1,  1,  1,  1,  1,  1,  1,  1,  0]]


class Weapon:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

class Inventory:
    def __init__(self):
        self.items = {}
        self.weapon = Weapon("Fist", 0)
        self.armor = Armor("Clothes", 0)
        self.money = 100
   
    def add_item(self, name, quantity=1, **attributes):
        if name in self.items:
            self.items[name]['quantity'] += quantity
        else:
            self.items[name] = {'quantity': quantity, **attributes}
   
    def remove_item(self, name, quantity=1):
        if name in self.items:
            self.items[name]['quantity'] -= quantity
            if self.items[name]['quantity'] <= 0:
                del self.items[name]
        else:
            print(f"The item {name} doesn't exist in the inventory.")
   
    def equip_weapon(self, name, attack):
        self.weapon = Weapon(name, attack)
   
    def equip_armor(self, name, defense):
        self.armor = Armor(name, defense)
   
    def has_item(self, name):
        return name in self.items
   
    def get_weapon(self):
        return self.weapon
   
    def get_armor(self):
        return self.armor
   
    def add_money(self, amount):
        self.money += amount
   
    def remove_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        else:
            print("Not enough money to complete the transaction.")
            return False
   
    def get_money(self):
        return self.money






class Character(pygame.sprite.Sprite,Inventory):
    '''The main class where start all the characters : Magicians, Warriors,... And even the main character !'''


    def __init__(self, position, size, img, collisions, name, life, defense, attack, xp, xp_level, sens=False):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (size, size))
        self.image = self.img.copy()
        self.rect = self.image.get_rect()
        self.size = size
        self.sens = sens

        self.collisions = collisions
        self.x, self.y = position
        self.rect.x = self.x * size
        self.rect.y = self.y * size

        self.name = name
        self.life = life
        self.defense = defense
        self.attack = attack
       
        self.maxLife = life
        self.damage_bonus = 1
       
        self.xp_level = xp_level
        self.xp = xp
        self.xp_bonus = 1
        self.next_level = int(10 * 1.1 ** self.xp_level)
        self.total_xp = int(self.xp + sum([10 * 1.1 ** i for i in range(self.xp_level)]))
        self.increase={"xp":0,"life":0,"defense":0,"attack":0,"xp_level":0,"next_level":0,"maxLife":0}
        Inventory.__init__(self)


    # detects if there is an obstacle where you want to walk or a character. If no, the method will move the character by x and y.
    def collisions_tests(self, x, y):
        if 0 <= self.x + x < len(self.collisions[0]) and 0 <= self.y + y < len(collisions):
            if self.collisions[self.y + y][self.x + x] == 0:
                if not self.test_collide_people(x, y, self.near_people(collide_group)):
                    self.x += x
                    self.y += y

    # test if there is any character in peoples on the path of the class' character

    def test_collide_people(self, x, y, peoples):
        return any((self.x + x == people.x and self.y + y == people.y for people in peoples))

    # return all the characters who are around the character (left,up,down and right)
    def near_people(self, groups):
        near = []
        for group in groups:
            for people in group:
                x, y = people.x, people.y
                if (abs(self.x - x) == 1 and abs(self.y - y) == 0) or (abs(self.y - y) == 1 and abs(self.x - x) == 0):
                    near.append(people)
        return near

    def add_life(self, life):
        self.increase["life"] += min(self.life + life, self.maxLife)-self.life


    def remove_life(self, life):
        self.increase["life"] += max(self.life - life, 0)-self.life


    def up_xp(self, xp):
        self.increase["xp"] += round(xp)
        self.total_xp += round(xp)
   
    def up_level(self):
        self.increase["xp_level"] += 1
        self.xp -= round(self.next_level)
        self.increase["next_level"] = round(self.next_level * 1.1)-self.next_level
        self.increase["maxLife"] += 2
        self.increase["life"] += 2
        self.increase["attack"] += round(5 + (0.005 * self.attack))
        self.increase["defense"] += round(4 + (0.005 * self.defense))
        if isinstance(self, Magician):
            self.increase_mana()
        elif isinstance(self, Warrior):
            self.increase_strength()

    def is_dead(self):
        return self.life == 0

    def move(self, x, y):
        if x == -1:
            self.sens = True
        elif x == 1:
            self.sens = False

        self.collisions_tests(x, y)
        self.rect.x = self.x * self.size
        self.rect.y = self.y * self.size
        self.image = pygame.transform.flip(self.img.copy(), True, False) if self.sens else self.img.copy()

    def fight(self, opponent, critic=False, attack_multiplier=100):
        damage_bonus = 1
        if isinstance(self, Magician):
            if self.mana > 1:
                damage_bonus += 0.5

        elif isinstance(self, Warrior):
            damage_bonus += self.force * 0.05

        if critic:
            damage_bonus *= 1.5
        damage = self.calculate_damage(opponent, attack_multiplier, damage_bonus)
        opponent.remove_life(damage)

        if isinstance(self, Magician):
            # remove mana
            self.remove_mana(2)
        return damage, critic

    def gain_to_death(self,opponent):
        if opponent.is_dead():
            # gain xp and strength if the opponent is dead
            self.up_xp(opponent.total_xp * 0.9 * self.xp_bonus)
            self.add_money(65 + round(5 * opponent.xp_level))
            if isinstance(self, Magician):
                self.add_mana(self.maxMana // 2)


    # attacker_attack, defender_defense, attacker_level, defender_level, attack_multiplier, damage_bonus):
    def calculate_damage(self, other, attack_multiplier, damage_bonus):
        attack = self.attack+self.get_weapon().attack
        defense = other.defense+other.get_armor().defense
        level_ratio = (self.xp_level + 100) / (self.xp_level + other.xp_level + 200)
        damage = ((((2 * (self.xp_level + 50)) / 100) * (attack / (defense + 100)) * attack_multiplier) + 2) * damage_bonus
        damage *= level_ratio

        # Generates a random number between 0.8 and 1.2
        variation = uniform(0.8, 1.2)
        damage *= variation

        if damage < 1:
            damage = 1  # guarantees the attacker to do at least 1 damage regardless of the level difference
        return round(damage)

class Warrior(Character):
    '''It's a character who have a particularity : strength. If you won a fight, it increases. It add power to your attacks.'''


    def __init__(self, position, size, img, collisions, name, strength, life, defense, attack, xp, xp_level, sens=False):
        super().__init__(position, size, img, collisions, name, life, defense, attack, xp, xp_level, sens)
        self.force = strength
        self.critic = 2.5
        self.increase["strength"]=0


    def increase_strength(self):
        self.increase["strength"] += 1




class Magician(Character):
    '''This character have mana. It's a resource who inflict more damage to his enemy : two time more than the strength of the warrior !
    However, each time you hurt your opponent, you will lose a part of your mana. If your mana drops to 0, you just inflict normal damage.
    After each figth you will regain, the half of your maximum of mana.'''


    def __init__(self, position, size, img, collisions, name, mana, life, defense, attack, xp, xp_level, sens=False):
        super().__init__(position, size, img, collisions, name, life, defense, attack, xp, xp_level, sens)
        self.maxMana = mana
        self.mana = mana
        self.critic = 3
        self.increase["mana"]=0


    def increase_mana(self):
        self.maxMana += 2


    def remove_mana(self, mana):
        self.increase["mana"] += max(0, self.mana - mana)-self.mana
        return self.mana-self.increase["mana"] > 0


    def add_mana(self, mana):
        self.increase["mana"] += min(self.maxMana, self.mana + mana)




class Backboard(pygame.sprite.Sprite):
    def __init__(self, position, size, img, text) -> None:
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load(img), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.size = size
        self.x, self.y = position
        self.rect.x = self.x * size
        self.rect.y = self.y * size
        self.text = text

    def interact(self):
        display_level(level)
        adventurers.draw(window)
        evils.draw(window)
        billboard.draw(window)
        for i in range(len(self.text)):
            size = font.size(self.text[i])
            x = (TILE_SIZE * length / 2) - size[0] / 2
            write_text(self.text[i], x, TILE_SIZE * width + TILE_SIZE // 2 * i + 1, font)


        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                        return


            clock.tick(60)
            pygame.display.flip()

class Merchant(pygame.sprite.Sprite):
   
    def __init__(self, position, size, img, *goods, text=[]) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.size = size
        self.x, self.y = position
        self.rect.x = self.x * size
        self.rect.y = self.y * size
        self.text = text
        self.goods = list(goods)
        self.text_size = TILE_SIZE // 2
   
    def display_text(self):
        for i in range(len(self.text)):
            size = font.size(self.text[i])
            x = (TILE_SIZE * length / 2) - size[0] / 2
            write_text(self.text[i], x, TILE_SIZE * width + TILE_SIZE // 2 * i + 1,font)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                        return

            clock.tick(GLOBAL_FPS)
            pygame.display.flip()

    def write_act(self, act, cursor, retour=True, info=True, text=[]):
        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
        for i in range(len(text)):
            write_text(text[i], 0, TILE_SIZE * width + self.text_size * 1.5 * i, font2, pos="center")
        for i, option in enumerate(act):
            if info:good = option[0]
            else: good = option
            write_text(('> ' if i == cursor else '') + good, 0, TILE_SIZE * width + self.text_size * 1.5 * (i + len(text)), font2)
            if info:
                write_text(("Attaque: " if option[1]["type"] == Weapon else "Défense: ") + str(option[1]["effect"]), 0, TILE_SIZE * width + self.text_size * 1.5 * (i + len(text)), font2, pos='right')
        if retour:
            write_text(('> ' if (len(act) - (1 if not retour else 0)) == cursor else '') + "Retour", 0, TILE_SIZE * width + self.text_size * 1.5 * (len(act) + len(text)), font2)

    def get_cursor(self, *act, text=[], retour=True, info=True):
        cursor = 0
        self.write_act(act, cursor, retour, info, text)
        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
                        return len(act) - (1 if not retour else 0)

                    if event.key == pygame.K_RETURN:
                        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
                        return cursor

                    elif event.key == pygame.K_UP:
                        if cursor > 0:
                            cursor -= 1
                            self.write_act(act, cursor, retour, info, text)

                    elif event.key == pygame.K_DOWN:
                        if cursor < len(act) - (1 if not retour else 0):
                            cursor += 1
                            self.write_act(act, cursor, retour, info, text)
            pygame.display.flip()
            clock.tick(GLOBAL_FPS)

    def validation_achat(self, c1, obj):
        text = ["vous avez " + str(c1.money) + " monaie", "voulez vous acheter " + str(obj[0]), "pour " + str(obj[1]["cost"]) + " ?"]
        cursor = self.get_cursor("Oui", "Non", text=text, retour=False, info=False)
        if cursor == 0:
            valide = c1.remove_money(obj[1]["cost"])
            if valide:
                c1.add_item(obj[0], effect=obj[1]["effect"], type=obj[1]["type"])
                if obj[1]["type"] == Weapon:
                    c1.equip_weapon(obj[0], obj[1]["effect"])
                elif obj[1]["type"] == Armor:
                    c1.equip_armor(obj[0], obj[1]["effect"])
                del self.goods[self.goods.index(obj)]
            else:
                pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
                write_text("Pas assez d'argent !", 0, TILE_SIZE * width + self.text_size * 1.5 * 3, font2, pos='center')
                pygame.display.flip()
                pygame.time.wait(1500)
                return
        if cursor == 1:
            return

    def show_goods(self, c1):
        cursor = self.get_cursor(*self.goods)
        if cursor == len(self.goods):
            return
        else:
            obj = self.goods[cursor]
            self.validation_achat(c1, obj)
        pygame.event.clear()

    def interact(self, c1):
        if self.text:
            self.display_text()
        self.show_goods(c1)
       


class Fight:
    '''
    A class o fight !
    It managed the fight himself, but also the display of all the fight infos
    '''

    def __init__(self, figther1: Character, figther2: Character):
        self.f1 = figther1
        self.f2 = figther2
        self.text_size = TILE_SIZE // 2
        self.font = pygame.font.Font('freesansbold.ttf', self.text_size)
        self.duel()

    def write_figthers(self):
        '''
        Write the names of the fighters like that :
        Fighter1    VS   Fighter2
        '''
        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE))
        write_text(self.f1.name, 0, TILE_SIZE * width,self.font,)
        write_text('VS', 0, TILE_SIZE * width,self.font, pos='center')
        write_text(self.f2.name, 0, TILE_SIZE * width,self.font, pos='right')


    def increase_attribute(self,name,var,increase,stop):
        if increase[name]>0:
            var+=1
            increase[name]-=1
            return stop+[False],var
        elif increase[name]<0:
            var-=1
            increase[name]+=1
            return stop+[False],var
        return stop+[True],var


    def write_infos(self, results=None):
        '''
        Write all the fight infos like PV, XP, Shield, Mana, Damages...
        '''
        i=10
        while True:
            stop=[]
            stop,self.f1.life=self.increase_attribute("life",self.f1.life,self.f1.increase,stop)
            stop,self.f1.defense=self.increase_attribute("defense",self.f1.defense,self.f1.increase,stop)
            stop,self.f1.attack=self.increase_attribute("attack",self.f1.attack,self.f1.increase,stop)
            stop,self.f1.xp=self.increase_attribute("xp",self.f1.xp,self.f1.increase,stop)
            if self.f1.xp>= self.f1.next_level:
                self.f1.up_level()
            stop,self.f1.xp_level=self.increase_attribute("xp_level",self.f1.xp_level,self.f1.increase,stop)
            stop,self.f1.next_level=self.increase_attribute("next_level",self.f1.next_level,self.f1.increase,stop)
            stop,self.f1.maxLife=self.increase_attribute("maxLife",self.f1.maxLife,self.f1.increase,stop)
           
            stop,self.f2.life=self.increase_attribute("life",self.f2.life,self.f2.increase,stop)
            stop,self.f2.defense=self.increase_attribute("defense",self.f2.defense,self.f2.increase,stop)
            stop,self.f2.attack=self.increase_attribute("attack",self.f2.attack,self.f2.increase,stop)
            stop,self.f2.xp=self.increase_attribute("xp",self.f2.xp,self.f2.increase,stop)
            if self.f2.xp >= self.f2.next_level:
                self.f2.up_level()
            stop,self.f2.xp_level=self.increase_attribute("xp_level",self.f2.xp_level,self.f2.increase,stop)
            stop,self.f2.next_level=self.increase_attribute("next_level",self.f2.next_level,self.f2.increase,stop)
            stop,self.f2.maxLife=self.increase_attribute("maxLife",self.f2.maxLife,self.f2.increase,stop)


            pygame.draw.rect(window, '#000000', pygame.Rect(
                0, TILE_SIZE * width + self.text_size, TILE_SIZE * length, self.text_size * 8))
            write_text(f'{str(self.f1.life)}/{str(self.f1.maxLife)} PV', 0, TILE_SIZE * width+self.text_size, font, '#EE3333')
            write_text(f'{str(self.f2.life)}/{str(self.f2.maxLife)} PV', 0, TILE_SIZE * width + self.text_size, font, '#EE3333', pos='right')
            write_text(f'{str(self.f1.xp)}/{str(self.f1.next_level)} XP', 0, TILE_SIZE * width + text_size * 2, font, '#33EE33')
            write_text(f'{str(self.f2.xp)}/{str(self.f2.next_level)} XP', 0, TILE_SIZE * width + text_size * 2, font, '#33EE33', pos='right')
            write_text(f'{str(self.f1.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 3, font, '#33EE33')
            write_text(f'{str(self.f2.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 3, font, '#33EE33', pos='right')
            write_text(f'{str(self.f1.defense)} Shield', 0, TILE_SIZE * width + self.text_size * 4, font, '#3333EE')
            write_text(f'{str(self.f2.defense)} Shield', 0, TILE_SIZE * width + self.text_size * 4, font, '#3333EE', pos='right')


            for i, f in enumerate([self.f1, self.f2]):
                if isinstance(f, Warrior):
                    stop,f.force=self.increase_attribute("strength",f.force,f.increase,stop)
                    write_text(f'{str(f.force)} Strength', 0, TILE_SIZE * width + self.text_size * 5, font, '#EEA500', pos=('left' if not i else 'right'))
                elif isinstance(f, Magician):
                    stop,f.mana=self.increase_attribute("mana",f.mana,f.increase,stop)
                    write_text(f'{str(f.mana)} Mana', 0, TILE_SIZE * width + self.text_size * 5, font, '#00DDDD', pos=('left' if not i else 'right'))


            if results != None:
                write_text(
                    '-' + str(results[0]) + ' PV', 0, TILE_SIZE * width + self.text_size * 6, font, '#FF3333', pos='center')
                if results[1]:
                    write_text('CRITIC !', 0, TILE_SIZE * width +
                            self.text_size * 7, font, pos='center')
           
            pygame.display.update()
            pygame.time.wait(i)
            i-=0.1


            if all(stop):
                return


    def duel(self):
        '''
        A loop to manage the duel :
        Attack of the player and riposte of the ennemy !
        And she call write functions when she need.
        '''
        self.write_figthers()
        self.write_infos()
        write_text('ATTAQUER [Entrée]', 0, TILE_SIZE * width + self.text_size * 9,self.font)
        attack = 0
        critic = False
        t = 0


        while True:
            if t < monotonic():
                # Check if the opponent is dead
                if self.f2.is_dead():
                    evils.remove(self.f2)
                    return


                # Check if the player is dead
                elif self.f1.is_dead():
                    return


                if not attack:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                if randint(0, 1):
                                    return


                                else:
                                    attack = 1
                                    critic = True


                            elif event.key == pygame.K_RETURN:
                                self.write_infos(self.f1.fight(self.f2))
                                self.write_infos(self.f1.gain_to_death(self.f2))
                                attack = 1
                                t = monotonic() + 0.3


                else:
                    self.write_infos(self.f2.fight(self.f1, critic))
                    self.write_infos(self.f2.gain_to_death(self.f1))
                    critic = False
                    attack = 0
                    t = monotonic() + 0.3
                    pygame.event.clear()


                pygame.display.flip()




class Actions:
    '''
    A class to interact with PNGs : fight, trade...
    '''


    def __init__(self, character1=None, character2=None):
        self.c1 = character1
        self.c2 = character2
        self.text_size = TILE_SIZE // 2
        self.font = pygame.font.Font('freesansbold.ttf', self.text_size)
        self.choose_action()




    def choose_action(self):
        '''
        Choose the thing to do with the PNG (ask the player).
        '''
        if self.c2 in evils:
            cursor = self.get_action(('Attaquer', 'Retour'))
            if cursor == 0:
                Fight(self.c1, self.c2)
            if cursor == -1:
                pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width + self.text_size, TILE_SIZE * length, TILE_SIZE * 5))
                return
           
        elif self.c2 in merchant:
            cursor = self.get_action(('Acheter', 'Retour'))
            if cursor == 0:
                self.c2.interact(self.c1)
            if cursor == -1:
                pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width + self.text_size, TILE_SIZE * length, TILE_SIZE * 5))
                return

        elif self.c2 in billboard:
            cursor = self.get_action(('Interagir', 'Retour'))
            if cursor == 0:
                self.c2.interact()
            if cursor == -1:
                pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width + self.text_size, TILE_SIZE * length, TILE_SIZE * 5))
                return

    def write_options(self, options, cursor):
        '''
        Write the options of things to do with the PNG.
        '''
        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
        for i, option in enumerate(options):
            write_text(('> ' if i == cursor else '') + option, 0, TILE_SIZE * width + self.text_size * 1.5 * i,self.font, '#FFFFFF')


    def get_action(self, actions):
        '''
        Ask the user for the action to do with the PNG.
        '''
        cursor = 0
        self.write_options(actions, cursor)
        t = 0
        while True:
            for event in pygame.event.get():
                if event.key == pygame.K_ESCAPE:
                        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
                        return -1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE * 5))
                        return cursor

                    elif event.key == pygame.K_UP:
                        if t < monotonic() and cursor > 0:
                            cursor -= 1
                            self.write_options(actions, cursor)
                            t = monotonic() + 0.1

                    elif event.key == pygame.K_DOWN:
                        if t < monotonic() and cursor < len(actions) - 1:
                            cursor += 1
                            self.write_options(actions, cursor)
                            t = monotonic() + 0.1
            pygame.display.flip()

def write_text(text, x, y, font, color='#FFFFFF', pos='left'):
    '''
    Write text with the possibility to choose where : left, center or right.
    Very useful !
    '''
    if pos == 'center':
        x += (length * TILE_SIZE - font.size(text)[0]) // 2
    elif pos == 'right':
        x += length * TILE_SIZE - font.size(text)[0]
    window.blit(font.render(text, True, color), (x, y))

def write_main_character_infos(main_character, text_size):
    character_type = ('Warrior 'if isinstance(main_character, Warrior) else 'Magician 'if isinstance(main_character, Magician) else '')
    pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, text_size * 8))
    write_text(character_type+main_character.name, 0, TILE_SIZE * width, font2, pos='center')
    write_text(f'{str(main_character.life)}/{str(main_character.maxLife)} PV', 0, TILE_SIZE * width+text_size, font2, '#EE3333', pos='center')
    write_text(f'{str(main_character.xp)}/{str(main_character.next_level)} XP', 0, TILE_SIZE * width + text_size * 2.5, font2, '#33EE33', pos='center')
    write_text(f'{str(main_character.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 4, font2, '#33EE33', pos='center')
    write_text(f'{str(main_character.defense)} Shield', 0, TILE_SIZE * width + text_size * 5.5, font2, '#3333EE', pos='center')

    if isinstance(main_character, Warrior):
        write_text(f"{str(main_character.force)} Strength", 0, TILE_SIZE * width + text_size * 7, font2, "#EEA500", pos='center')
    elif isinstance(main_character, Magician):
        write_text(f'{str(main_character.mana)}/{str(main_character.maxMana)} Mana', 0, TILE_SIZE * width + text_size * 7, font2, '#00DDDD', pos='center')
   
    write_text(f'{str(main_character.money)} Money', 0, TILE_SIZE * width + text_size * 8.5, font2, '#EDDE44', pos='center')


# the window size depend of the length and the width of the level
# we add a row of 32 pixels
# we add a row of 32 pixels at the bottom of the window to display additional information -> (height +5)
pygame.init()
window = pygame.display.set_mode((length * TILE_SIZE, (width + 5) * TILE_SIZE))
pygame.display.set_caption("Dungeon")
font = pygame.font.Font('freesansbold.ttf', 20)
text_size = TILE_SIZE // 2
font2 = pygame.font.Font('freesansbold.ttf', text_size)


def load_tiles(tiles):
    """
    function allowing to load the tiles' images in a list tiles[]
    """
    for n in range(0, NB_TILES):
        tile = pygame.image.load('data/' + str(n) + '.png')
        new_tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
        tiles.append(new_tile)  # pay attention to the path


def display_level(level):
    """
    display the level from a two dimensions list level[][]
    """
    for y in range(width):
        for x in range(length):
            window.blit(tiles[level[y][x]], (x * TILE_SIZE, y * TILE_SIZE))
            if (decor[y][x] > 0):
                window.blit(tiles[decor[y][x]], (x * TILE_SIZE, y * TILE_SIZE))


window.fill((0, 0, 0))   # clear the window
load_tiles(tiles)  # load images

perso = Magician([1, 3], TILE_SIZE, 'data/perso.png', collisions, 'Théodore', 10, 200, 10, 10, 5, 1)
# perso = Warrior([1,1],TILE_SIZE,'data/perso.png',collisions,'Théodore',1,200,0,0,15)
perso2 = Magician([3, 5], TILE_SIZE, 'data/perso.png', collisions, 'Magician', 100, 200, 60, 70, 288, 25, sens=True)
perso4 = Warrior([1, 5], TILE_SIZE, 'data/perso.png', collisions, 'Guerrier', 10, 20, 15, 5, 2, 3)
perso5 = Magician([2, 5], TILE_SIZE, 'data/perso.png', collisions, 'Johan', 200, 500, 80, 90, 641, 200)
perso6 = Warrior([1, 6], TILE_SIZE, 'data/perso.png', collisions, 'Warrior', 15, 30, 20, 10, 45, 17)

perso3 = Merchant([6, 1], TILE_SIZE, 'data/perso.png',
                    ("épée en carton", {"cost": 20, "effect": 10, "type": Weapon}), ("armure en cuire", {"cost": 50, "effect": 40, "type": Armor}),
                    ("épée en fer", {"cost": 200, "effect": 190, "type": Weapon}), ("armure en fer", {"cost": 250, "effect": 220, "type": Armor}),
                    text=["Bonjour et bienvenue chez Johan & co.", "Je me présente, je suis Inconnu.txt", "vendeur officiel de Johan & co.", "Je présume que vous êtes",
                    "intéressé par la réduction du jour.", "Et bien vous êtes au bon endroit !", "", "Aujourd'hui seulement,", "-0% sur tous les produits !!!", "Ah oui désolé j'ai mis un 7 en trop sur le panneau."])

backboard = Backboard([3, 6], TILE_SIZE, "data/99.png", ["Salut, je suis un", "panneau publicitaire !", "La publicité du jour :",
                      "Aujourd'hui seulement,", "-70% sur tout les produits", "Johan & co.", "", "Une offre à ne pas rater !!!"])


adventurers = pygame.sprite.Group()
adventurers.add(perso)

evils = pygame.sprite.Group()
evils.add(perso2)
evils.add(perso4)
evils.add(perso5)
evils.add(perso6)


billboard = pygame.sprite.Group()
billboard.add(backboard)

merchant = pygame.sprite.Group()
merchant.add(perso3)

collide_group = (adventurers, evils, billboard, merchant)


#perso.equip_weapon('arme',100000)
#perso.equip_armor('armure',100000)


loop = True
pygame.key.set_repeat(200, 100)
while loop == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False  # close the window (red cross)
        elif event.type == pygame.KEYDOWN:  # A key has been pressed... which one?
            if event.key == pygame.K_UP:    # Is it the UP Key
                perso.move(0, -1)
            elif event.key == pygame.K_DOWN:  # Is it the DOWN Key
                perso.move(0, 1)
            elif event.key == pygame.K_RIGHT:  # Is it the RIGHT Key
                perso.move(1, 0)
            elif event.key == pygame.K_LEFT:  # Is it the LEFT Key
                perso.move(-1, 0)
            elif event.unicode == 'q':  # Q key to quit
                loop = False
            elif event.key == pygame.K_RETURN:
                n = perso.near_people((evils, billboard, merchant))
                if n:
                    Actions(perso, n[0])
                if perso.is_dead():
                    print('Vous êtes mort !')
                    loop = False

    window.fill((0, 0, 0))
    display_level(level)  # display the level
    for groups in collide_group:
        groups.update()
        groups.draw(window)
    write_main_character_infos(perso,text_size)
    pygame.display.flip()
    clock.tick(GLOBAL_FPS)
pygame.quit()
