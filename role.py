'''
Program realised by :
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


class Inventory:
    none_weapon = {'name': 'Nothing', 'atk': 0}
    none_armor = {'name': 'None', 'def': 0}
    def __init__(self):
        self.equipped_weapon = self.none_weapon.copy()
        self.equipped_armor = self.none_armor.copy()
        self.__inventory={}
   
    def add_to_inventory(self,items):
        """thing : {object_name1:{attribute1:value,attribute2:value,...},object_name2:{...},...}"""
        for obj in items.keys():
            # add the object in the inventory if it is not already inside
            if obj not in self.__inventory:
                # add a "quantity" parameter to the object if it don't have already one
                if "quantity" not in items[obj]:
                    items[obj]["quantity"]=1
                self.__inventory.update({obj:items[obj]})
    
    def add_to_items(self,items):
        """allow to increase (or decrease with negative values) some parameters of items in inventory (quantity, ...)"""
        for item in items.keys():
            if item not in self.__inventory:
                self.add_to_inventory({item:items[item]})
            for i in self.__inventory[item]:
                if i in items[item]:
                    self.__inventory[item][i]+=items[item][i]
    
    def set_to_items(self,items):
        """allow to set some parameters of items in inventory (quantity, ...)"""
        for item in items.keys():
            if item not in self.__inventory:
                self.add_to_inventory({item:items[item]})
            for i in self.__inventory[item]:
                if i in items[item]:
                    self.__inventory[item][i]=items[item][i]
   
    def is_in_inventory(self,thing):
        """return a bool : True if thing is the name of an item in the inventory, False else"""
        return thing in self.__inventory
   
    def remove_to_inventory(self,thing):
        """
        thing is the name of an item in the inventory
        remove 1 to thing "quantity" parameter
        """
        if self.is_in_inventory(thing):
            inventory=self.__inventory[thing]
            self.__inventory[thing]["quantity"]-=1
            if inventory["quantity"]==0:
                self.__inventory.pop(thing)


    def get_inventory(self):
        """Return the inventory"""
        return self.__inventory


class Character(pygame.sprite.Sprite,Inventory):
    '''The main class where start all the characters : Magicians, Warriors,... And even the main character !'''

    def __init__(self, position, size, img, collisions, name, life, defense, attack, xp, xp_level, sens=False):
        super().__init__()
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
        self.life = min(self.life + life, self.maxLife)

    def remove_life(self, life):
        self.life = max(self.life - life, 0)

    def up_xp(self, xp):
        self.xp += round(xp)
        self.total_xp += round(xp)
        while self.xp >= self.next_level:
            self.xp_level += 1
            self.xp -= round(self.next_level)
            self.next_level = round(self.next_level * 1.1)
            self.maxLife += 2
            self.life += 2
            self.attack += round(5 + (0.005 * self.attack))
            self.defense += round(4 + (0.005 * self.defense))
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
        #print(damage)
        opponent.remove_life(damage)

        if isinstance(self, Magician):
            # remove mana
            self.remove_mana(2)

        if opponent.is_dead():
            # gain xp and strength if the opponent is dead
            self.up_xp(opponent.total_xp * 0.9 * self.xp_bonus)
            if isinstance(self, Magician):
                self.add_mana(self.maxMana // 2)
        return damage, critic

    # attacker_attack, defender_defense, attacker_level, defender_level, attack_multiplier, damage_bonus):
    def calculate_damage(self, other, attack_multiplier, damage_bonus):
        #print(self.attack, other.defense)
        level_ratio = (self.xp_level + 100) / (self.xp_level + other.xp_level + 200)
        damage = ((((2 * (self.xp_level + 50)) / 100) * (self.attack / (other.defense + 100)) * attack_multiplier) + 2) * damage_bonus
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

    def increase_strength(self):
        self.force += 1


class Magician(Character):
    '''This character have mana. It's a resource who inflict more damage to his enemy : two time more than the strength of the warrior !
    However, each time you hurt your opponent, you will lose a part of your mana. If your mana drops to 0, you just inflict normal damage.
    After each figth you will regain, the half of your maximum of mana.'''

    def __init__(self, position, size, img, collisions, name, mana, life, defense, attack, xp, xp_level, sens=False):
        super().__init__(position, size, img, collisions, name, life, defense, attack, xp, xp_level, sens)
        self.maxMana = mana
        self.mana = mana
        self.critic = 3

    def increase_mana(self):
        self.maxMana += 2

    def remove_mana(self, mana):
        self.mana = max(0, self.mana - mana)
        return self.mana > 0

    def add_mana(self, mana):
        self.mana = min(self.maxMana, self.mana + mana)


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


class Fight:
    '''
    A class o fight !
    It managed the fight himself, but also the display of all the fight infos
    '''

    def __init__(self, figther1: Character, figther2: Character):
        self.f1 = figther1
        self.f2 = figther2
        self.duel()

    def write_figthers(self):
        '''
        Write the names of the fighters like that :
        Fighter1    VS   Fighter2
        '''
        pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, TILE_SIZE))
        self.write_text(self.f1.name, 0, TILE_SIZE * width)
        self.write_text('VS', 0, TILE_SIZE * width, pos='center')
        self.write_text(self.f2.name, 0, TILE_SIZE * width, pos='right')

    def write_infos(self, results=None):
        '''
        Write all the fight infos like PV, XP, Shield, Mana, Damages...
        '''
        pygame.draw.rect(window, '#000000', pygame.Rect(
            0, TILE_SIZE * width + self.text_size, TILE_SIZE * length, self.text_size * 8))
        write_text(f'{str(self.f1.life)}/{str(self.f1.maxLife)} PV', 0, TILE_SIZE * width+self.text_size, font, '#EE3333')
        write_text(f'{str(self.f2.life)}/{str(self.f2.maxLife)} PV', 0, TILE_SIZE * width + self.text_size, font, '#EE3333', pos='right')
        write_text(f'{str(self.f1.xp)}/{str(self.f1.next_level)} XP', 0, TILE_SIZE * width + text_size * 2, font, '#33EE33')
        write_text(f'{str(self.f1.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 3, font, '#33EE33')
        write_text(f'{str(self.f2.xp)}/{str(self.f2.next_level)} XP', 0, TILE_SIZE * width + text_size * 2, font, '#33EE33', pos='right')
        write_text(f'{str(self.f2.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 3, font, '#33EE33', pos='right')
        write_text(f'{str(self.f1.defense)} Shield', 0, TILE_SIZE * width + self.text_size * 4, font, '#3333EE')
        write_text(f'{str(self.f2.defense)} Shield', 0, TILE_SIZE * width + self.text_size * 4, font, '#3333EE', pos='right')

        for i, f in enumerate([self.f1, self.f2]):
            if isinstance(f, Warrior):
                write_text(f'{str(f.force)} Strength', 0, TILE_SIZE * width + self.text_size * 5, font, '#EEA500', pos=('left' if not i else 'right'))
            elif isinstance(f, Magician):
                write_text(f'{str(f.mana)} Mana', 0, TILE_SIZE * width + self.text_size * 5, font, '#EEEE33', pos=('left' if not i else 'right'))

        if results != None:
            write_text('-' + str(results[0]) + ' PV', 0, TILE_SIZE * width + self.text_size * 6, font, '#FF3333', pos='center')
            if results[1]:
                write_text('CRITIC !', 0, TILE_SIZE * width + self.text_size * 7, font, pos='center')

    def duel(self):
        '''
        A loop to manage the duel :
        Attack of the player and riposte of the ennemy !
        And she call write functions when she need.
        '''
        self.write_figthers()
        self.write_infos()
        self.write_text('ATTAQUER [Entrée]', 0, TILE_SIZE * width + self.text_size * 9)
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
                                attack = 1
                                t = monotonic() + 0.3

                else:
                    self.write_infos(self.f2.fight(self.f1, critic))
                    critic = False
                    attack = 0
                    t = monotonic() + 0.3
                    pygame.event.clear()

                pygame.display.flip()


class Actions(Fight):
    '''
    A class to interact with PNGs : fight, trade...
    '''

    def __init__(self, character1, character2):
        self.c1 = character1
        self.c2 = character2
        self.text_size = TILE_SIZE // 2
        self.font = pygame.font.Font('freesansbold.ttf', self.text_size)
        self.choose_action()

    def write_text(self, text, x, y, color = '#FFFFFF', pos = 'left'):
        '''
        Write text with the possibility to choose where : left, center or right.
        Very useful !
        '''
        if pos == 'center':
            x += (length * TILE_SIZE - self.font.size(text)[0]) // 2
        elif pos == 'right':
            x += length * TILE_SIZE - self.font.size(text)[0]
        window.blit(self.font.render(text, True, color), (x, y))

    def choose_action(self):
        '''
        Choose the thing to do with the PNG (ask the player).
        '''
        if self.c2 in evils:
            cursor = self.get_action(('Attaquer', 'Retour'))
            if cursor == 0:
                Fight.__init__(self, self.c1, self.c2)
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
            self.write_text(('> ' if i == cursor else '') + option, 0, TILE_SIZE * width + self.text_size * 1.5 * i, '#FFFFFF')

    def get_action(self, actions):
        '''
        Ask the user for the action to do with the PNG.
        '''
        cursor = 0
        self.write_options(actions, cursor)
        t = 0
        while True:
            for event in pygame.event.get():
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

def write_text(text, x, y,font, color='#FFFFFF', pos='left'):
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
    character_type=('Warrior 'if isinstance(main_character,Warrior) else 'Magician 'if isinstance(main_character,Magician) else '')
    pygame.draw.rect(window, '#000000', pygame.Rect(0, TILE_SIZE * width, TILE_SIZE * length, text_size * 8))
    write_text(character_type+main_character.name, 0, TILE_SIZE * width, font2, pos='center')
    write_text(f'{str(main_character.life)}/{str(main_character.maxLife)} PV', 0, TILE_SIZE * width+text_size, font2, '#EE3333', pos='center')
    write_text(f'{str(main_character.xp)}/{str(main_character.next_level)} XP', 0, TILE_SIZE * width + text_size * 2.5, font2, '#33EE33', pos='center')
    write_text(f'{str(main_character.xp_level)} LEVELS', 0, TILE_SIZE * width + text_size * 4, font2, '#33EE33', pos='center')
    write_text(f'{str(main_character.defense)} Shield', 0, TILE_SIZE * width + text_size * 5.5, font2, '#3333EE', pos='center')

    if isinstance(main_character, Warrior):
        write_text(f'{str(main_character.force)} Strength', 0, TILE_SIZE * width + text_size * 7, font2, '#EEA500', pos='center')
    elif isinstance(main_character, Magician):
        write_text(f'{str(main_character.mana)}/{str(main_character.maxMana)} Mana', 0, TILE_SIZE * width + text_size * 7, font2, '#EEEE33', pos='center')



# the window size depend of the length and the width of the level
# we add a row of 32 pixels
# we add a row of 32 pixels at the bottom of the window to display additional information -> (height +5)
pygame.init()
window = pygame.display.set_mode((length * TILE_SIZE, (width + 5) * TILE_SIZE))
pygame.display.set_caption('Dungeon')
font = pygame.font.Font('freesansbold.ttf', 20)
text_size=TILE_SIZE//2
font2 = pygame.font.Font('freesansbold.ttf', text_size)


def load_tiles(tiles):
    '''
    function allowing to load the tiles' images in a list tiles[]
    '''
    for n in range(0, NB_TILES):
        tile = pygame.image.load('data/' + str(n) + '.png')
        new_tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
        tiles.append(new_tile)  # pay attention to the path


def display_level(level):
    '''
    display the level from a two dimensions list level[][]
    '''
    for y in range(width):
        for x in range(length):
            window.blit(tiles[level[y][x]], (x * TILE_SIZE, y * TILE_SIZE))
            if (decor[y][x] > 0):
                window.blit(tiles[decor[y][x]], (x * TILE_SIZE, y * TILE_SIZE))


window.fill((0, 0, 0))   # clear the window
load_tiles(tiles)  # load images

perso = Magician([1, 3], TILE_SIZE, 'data/perso.png', collisions, 'Théodore', 10, 200, 10, 10, 5, 1)
# perso = Warrior([1,1],TILE_SIZE,'data/perso.png',collisions,'Théodore',1,200,0,0,15)
perso.equipped_weapon={"name":"epee","atk":200}
perso.equipped_armor={"name":"armure en diamant","def":200}
perso2 = Magician([3, 5], TILE_SIZE, 'data/perso.png', collisions, 'Magician', 100, 200, 60, 70, 288, 25, sens=True)
perso5 = Magician([2, 5], TILE_SIZE, 'data/perso.png', collisions, 'Johan', 200, 500, 80, 90, 641, 200)
perso3 = Character([3, 7], TILE_SIZE, 'data/perso.png', collisions, 'Inconnu.txt', 13, 22, 15, 2, 2)
perso4 = Warrior([1, 5], TILE_SIZE, 'data/perso.png', collisions, 'Guerrier', 10, 20, 15, 5, 2, 3)
perso6 = Warrior([1, 6], TILE_SIZE, 'data/perso.png', collisions, 'Warrior', 15, 30, 20, 10, 45, 17)


backboard = Backboard([3, 6], TILE_SIZE, "data/99.png", ["Salut, je suis un", "panneau publicitaire !", "La publicité du jour :",
                      "Aujourd'hui seulement!", "-70% sur tout les produits", "Johan & co.", "", "Une offre à ne pas rater !!"])


adventurers = pygame.sprite.Group()
adventurers.add(perso)
adventurers.add(perso3)

evils = pygame.sprite.Group()
evils.add(perso2)
evils.add(perso4)
evils.add(perso5)
evils.add(perso6)


billboard = pygame.sprite.Group()
billboard.add(backboard)

collide_group = (adventurers, evils, billboard)

for group in (adventurers, evils):
    for character in group:
        character.move(0, 0)

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
                n = perso.near_people((evils, billboard))
                if n:
                    Actions(perso, n[0])
                if perso.is_dead():
                    print('Vous êtes mort !')
                    loop = False

    window.fill((0, 0, 0))
    display_level(level)  # display the level
    adventurers.update()
    adventurers.draw(window)
    evils.update()
    evils.draw(window)
    billboard.update()
    billboard.draw(window)
    write_main_character_infos(perso,text_size)
    pygame.display.flip()
    clock.tick(GLOBAL_FPS)
pygame.quit()
