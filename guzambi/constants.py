import random

from pygame import image, transform, Rect
from enum import Enum

WIDTH = 700
BOARD_SIZE = 5
IMG_SRC = '../img/'

HEIGHT = (WIDTH * 3) // 4
MARGIN = WIDTH // 30
HEADER = HEIGHT // 4
FOOTER = HEADER // 3
TILE_WIDTH = (HEIGHT - HEADER - FOOTER) // BOARD_SIZE
BOARD_WIDTH = BOARD_SIZE * TILE_WIDTH
CARD_WIDTH = WIDTH // 6
CARD_HEIGHT = CARD_WIDTH * 1.5

class State(Enum):
    SETTING = 1
    PLAYING = 2
    GAMEOVER = 3

class CardType(Enum):
    DRAGON = 1
    BEAST = 2
    ATTACK = 3
    DEFEND = 4
    MAGIC = 5
    HEAL = 6
    SPEED = 7

class FortuneCard:
    def __init__(self, ctype, assets):
        self.type = ctype
        self.assets = assets

    def get_card(self):
        card_img = random.choice(self.assets)
        return card_img, card_img.get_rect()

class Monster(FortuneCard):
    def __init__(self, ctype, assets, dmg, step):
        super().__init__(ctype, assets)
        self.dmg = dmg
        self.step = step

class Item(FortuneCard):
    def __init__(self, ctype, assets, icon):
        super().__init__(ctype, assets)
        self.icon = transform.scale(icon, (TILE_WIDTH - 30, TILE_WIDTH - 30))

class Potion(FortuneCard):
    def __init__(self, ctype, assets, ability):
        super().__init__(ctype, assets)
        self.ability = ability

class Legend:
    def __init__(self, title, card_img, hero_img):
        self.name = title
        self.card = transform.scale(card_img, (CARD_WIDTH, CARD_HEIGHT))
        self.sprite = transform.scale(hero_img, (TILE_WIDTH // 2, TILE_WIDTH // 2))
        self.card_rect = self.card.get_rect()


WAR_CARD = image.load(IMG_SRC + 'card1.png')
ORC_CARD = image.load(IMG_SRC + 'card2.png')
KNT_CARD = image.load(IMG_SRC + 'card3.png')
WIZ_CARD = image.load(IMG_SRC + 'card4.png')

WAR_CHAR = image.load(IMG_SRC + 'warrior.png')
ORC_CHAR = image.load(IMG_SRC + 'orc.png')
KNIGHT_CHAR = image.load(IMG_SRC + 'knight.png')
WIZARD_CHAR = image.load(IMG_SRC + 'wizard.png')

WARRIOR = Legend('Mighty Warrior', WAR_CARD, WAR_CHAR)
ORC = Legend('Savage Goblin', ORC_CARD, ORC_CHAR)
KNIGHT = Legend('Skeleton Knight', KNT_CARD, KNIGHT_CHAR)
WIZARD = Legend('Sacred Wizard', WIZ_CARD, WIZARD_CHAR)
LEGENDS = [WARRIOR, ORC, KNIGHT, WIZARD]

# DICE BUTTON
class Dice:
    def __init__(self):
        self.icon = transform.scale(image.load(IMG_SRC + 'dice.jpg'), (TILE_WIDTH, TILE_WIDTH))
        self.x = WIDTH - MARGIN - TILE_WIDTH
        self.y = HEIGHT - FOOTER - TILE_WIDTH - 5
        self.rect = Rect(self.x, self.y, TILE_WIDTH, TILE_WIDTH)


DICE = Dice()

# CONTINUE BUTTON
CTN_IMG = transform.scale(image.load(IMG_SRC + 'continue_btn.png'), (150, 50))
num_base = image.load(IMG_SRC + 'profile.jpg')


# DRAGON CARDS
def make_card_img(img_name):
    img_path = IMG_SRC + img_name
    return transform.scale(image.load(img_path), (CARD_WIDTH, CARD_HEIGHT))


DRAG_IMGS = ['monsterx0.png', 'monsterx1.png', 'monsterx2.png', 'monsterx3.png', 'monsterx4.png', 'monsterx5.png']
BEAST_IMGS = ['normal0.png', 'normal1.png', 'normal2.png', 'normal3.png', 'normal4.png']

dragon_assets = []
for img in DRAG_IMGS:
    card = make_card_img(img)
    dragon_assets.append(card)

beast_assets = []
for img in BEAST_IMGS:
    card = make_card_img(img)
    beast_assets.append(card)

DRAGON = Monster(CardType.DRAGON, dragon_assets, 30, 3)
BEAST = Monster(CardType.BEAST, beast_assets, 10, 1)


ATK_IMGS = ['atk0.png', 'atk1.png', 'atk2.png', 'atk3.png', 'atk4.png']
DEF_IMGS = ['def0.png', 'def1.png', 'def2.png', 'def3.png', 'def4.png']
MAG_IMGS = ['spcl0.png', 'spcl1.png', 'spcl2.png', 'spcl3.png', 'spcl4.png']

HEL_IMGS = ['regen0.png', 'regen1.png', 'regen2.png']
SPD_IMGS = ['spd0.png', 'spd1.png', 'spd2.png']
item_assets = {
    'atk': ATK_IMGS,
    'def': DEF_IMGS,
    'mag': MAG_IMGS,
    'hel': HEL_IMGS,
    'spd': SPD_IMGS
}


attack_assets = []
defend_assets = []
magic_assets = []
heal_assets = []
speed_assets = []
for name, asset in item_assets.items():
    for img in asset:
        card = make_card_img(img)
        if name == 'atk':
            attack_assets.append(card)
        elif name == 'def':
            defend_assets.append(card)
        elif name == 'heal':
            heal_assets.append(card)
        elif name == 'spd':
            speed_assets.append(card)
        elif name == 'mag':
            magic_assets.append(card)


ATK_ICON = image.load(IMG_SRC + 'atk_icon2.jpg')
DEF_ICON = image.load(IMG_SRC + 'def_icon2.jpg')
MAG_ICON = image.load(IMG_SRC + 'skull_icon.jpg')

attack_item = Item(CardType.ATTACK, attack_assets, ATK_ICON)
defend_item = Item(CardType.DEFEND, defend_assets, DEF_ICON)
magic_item = Item(CardType.MAGIC, magic_assets, MAG_ICON)
ITEMS = [attack_item, defend_item, magic_item]

heal_potion = Potion(CardType.HEAL, heal_assets, 10)
speed_potion = Potion(CardType.SPEED, speed_assets, 3)
POTIONS = [heal_potion, speed_potion]
    
dragon_info = transform.scale(image.load(IMG_SRC + 'dg_info.png'), (100, 150))
beast_info = transform.scale(image.load(IMG_SRC + 'beast_info.png'), (100, 150))
atk_info = transform.scale(image.load(IMG_SRC + 'atk_info.png'), (100, 150))
def_info = transform.scale(image.load(IMG_SRC + 'def_info.png'), (100, 150))
reg_info = transform.scale(image.load(IMG_SRC + 'reg_info.png'), (100, 150))
shoe_info = transform.scale(image.load(IMG_SRC + 'shoe_info.png'), (100, 150))
darkmg_info = transform.scale(image.load(IMG_SRC + 'darkmg_info.png'), (100, 150))

item_back = transform.scale(image.load(IMG_SRC + 'stoneback3.png'), (CARD_WIDTH, CARD_HEIGHT))
monster_back = transform.scale(image.load(IMG_SRC + 'stoneback2.png'), (CARD_WIDTH, CARD_HEIGHT))
darkmg_back = transform.scale(image.load(IMG_SRC + 'stoneback1.png'), (CARD_WIDTH, CARD_HEIGHT))

BLANK_CARDS = [item_back, monster_back, darkmg_back]
COVER_IMG = transform.scale(image.load(IMG_SRC + 'start_screen.jpg'), (WIDTH, HEIGHT))
BGIMG = transform.scale(image.load(IMG_SRC + 'bg1.jpg'), (BOARD_WIDTH, BOARD_WIDTH))

WHITE = (224, 224, 224)
BLUE = (33, 150, 243)
TEAL = (29, 233, 182)
GREY = (96, 125, 139)
BLACK = (0, 0, 0)
ORANGE = (255, 152, 0)
INDIGO = (63, 81, 181)
RED = (244, 67, 54)
AMBER = (255, 193, 7)
GREEN = (76, 175, 80)
# touch_fx = pygame.mixer.Sound('../sound/dice.wav')
# card_fx = pygame.mixer.Sound('../sound/card.wav')
# dice_fx = pygame.mixer.Sound('../sound/dice2.wav')
