import random
from pygame import image, transform, Rect, Surface, Color
from enum import Enum

WIDTH = 700
BOARD_SIZE = 5
IMG_SRC = '../img/'

HEIGHT = (WIDTH * 3) // 4
MARGIN = WIDTH // 30
HEADER = HEIGHT // 4
FOOTER = 20
TILE_WIDTH = (HEIGHT - HEADER - FOOTER) // BOARD_SIZE
BOARD_WIDTH = BOARD_SIZE * TILE_WIDTH
CARD_WIDTH = WIDTH // 5
CARD_HEIGHT = CARD_WIDTH * 1.5

class State(Enum):
    SETTING = 1
    PLAYING = 2
    GAMEOVER = 3
    PAUSE = 4

class CardType(Enum):
    BACK = 0
    DRAGON = 1
    BEAST = 2
    ATTACK = 3
    DEFEND = 4
    MAGIC = 5
    HEAL = 6
    SPEED = 7

class Card:
    def __init__(self, ctype: CardType, assets: list[Surface], info: Surface):
        self.type = ctype
        self.assets = assets
        self.info = info

    @property
    def img(self):
        card_img = random.choice(self.assets)
        return card_img

    def __str__(self):
        return str(self.type)

class Monster(Card):
    def __init__(self, ctype, assets, info, dmg, step):
        super().__init__(ctype, assets, info)
        self.dmg = dmg
        self.step = step

class Item(Card):
    def __init__(self, ctype, assets, info, icon):
        super().__init__(ctype, assets, info)
        self.icon = transform.scale(icon, (TILE_WIDTH - 30, TILE_WIDTH - 30))

class Potion(Card):
    def __init__(self, ctype, assets, info, ability):
        super().__init__(ctype, assets, info)
        self.ability = ability

class Legend:
    def __init__(self, title, card_img, hero_img):
        self.name = title
        self.card = transform.scale(card_img, (CARD_WIDTH, CARD_HEIGHT))
        self.sprite = transform.scale(hero_img, (TILE_WIDTH // 2, TILE_WIDTH // 2))
        self.card_rect = self.card.get_rect()


def make_card_img(img_name):
    img_path = IMG_SRC + img_name
    return transform.scale(image.load(img_path), (CARD_WIDTH, CARD_HEIGHT))


# Loading Images
COVER_IMG = transform.scale(image.load(IMG_SRC + 'fantasy1.jpg'), (WIDTH, HEIGHT))
BGIMG = transform.scale(image.load(IMG_SRC + 'bg1.jpg'), (BOARD_WIDTH, BOARD_WIDTH))
NAMEPAD = image.load(IMG_SRC + 'name_pad.png')
NAMEPAD_ACTIVE = image.load(IMG_SRC + 'name_pad_hl.png')
ICONPAD = transform.scale(image.load(IMG_SRC + 'icon_pad.png'), (TILE_WIDTH+10, TILE_WIDTH+10))
MSGPAD = image.load(IMG_SRC + 'msg_plate.png')
WINNER_BADGE = transform.scale(image.load(IMG_SRC + 'winner_badge.png'), (WIDTH//2, HEIGHT//2 + HEADER))

WAR_CARD = image.load(IMG_SRC + 'card1.png')
ORC_CARD = image.load(IMG_SRC + 'card2.png')
KNT_CARD = image.load(IMG_SRC + 'card3.png')
WIZ_CARD = image.load(IMG_SRC + 'card4.png')

WAR_CHAR = image.load(IMG_SRC + 'warrior.png')
ORC_CHAR = image.load(IMG_SRC + 'orc.png')
KNIGHT_CHAR = image.load(IMG_SRC + 'knight.png')
WIZARD_CHAR = image.load(IMG_SRC + 'wizard.png')

# Card info images
INFO_WIDTH = WIDTH - MARGIN*2 - BOARD_WIDTH - 20
INFO_HEIGHT = INFO_WIDTH // 2
dragon_info = transform.scale(image.load(IMG_SRC + 'dg_info.png'), (INFO_WIDTH, INFO_HEIGHT))
beast_info = transform.scale(image.load(IMG_SRC + 'beast_info.png'), (INFO_WIDTH, INFO_HEIGHT))
atk_info = transform.scale(image.load(IMG_SRC + 'atk_info.png'), (INFO_WIDTH, INFO_HEIGHT))
def_info = transform.scale(image.load(IMG_SRC + 'def_info.png'), (INFO_WIDTH, INFO_HEIGHT))
hel_info = transform.scale(image.load(IMG_SRC + 'reg_info.png'), (INFO_WIDTH, INFO_HEIGHT))
spd_info = transform.scale(image.load(IMG_SRC + 'shoe_info.png'), (INFO_WIDTH, INFO_HEIGHT))
mag_info = transform.scale(image.load(IMG_SRC + 'darkmg_info.png'), (INFO_WIDTH, INFO_HEIGHT))

# Monster Cards
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

# Item & Potion Cards
ATK_IMGS = ['atk0.png', 'atk1.png', 'atk2.png', 'atk3.png', 'atk4.png']
DEF_IMGS = ['def0.png', 'def1.png', 'def2.png', 'def3.png', 'def4.png']
MAG_IMGS = ['spcl0.png', 'spcl1.png', 'spcl2.png', 'spcl3.png', 'spcl4.png']

HEL_IMGS = ['regen0.png', 'regen1.png', 'regen2.png']
SPD_IMGS = ['spd0.png', 'spd1.png', 'spd2.png']
item_assets = {'atk': ATK_IMGS, 'def': DEF_IMGS, 'mag': MAG_IMGS, 'hel': HEL_IMGS, 'spd': SPD_IMGS}

attack_assets = []
defend_assets = []
magic_assets = []
heal_assets = []
speed_assets = []
for name in item_assets:
    for img in item_assets[name]:
        card = make_card_img(img)
        if name == 'atk':
            attack_assets.append(card)
        elif name == 'def':
            defend_assets.append(card)
        elif name == 'hel':
            heal_assets.append(card)
        elif name == 'spd':
            speed_assets.append(card)
        elif name == 'mag':
            magic_assets.append(card)

ATK_ICON = image.load(IMG_SRC + 'atk_icon2.jpg')
DEF_ICON = image.load(IMG_SRC + 'def_icon2.jpg')
MAG_ICON = image.load(IMG_SRC + 'skull_icon.jpg')

BACK1 = transform.scale(image.load(IMG_SRC + 'stoneback3.png'), (CARD_WIDTH, CARD_HEIGHT))
BACK2 = transform.scale(image.load(IMG_SRC + 'stoneback2.png'), (CARD_WIDTH, CARD_HEIGHT))
BACK3 = transform.scale(image.load(IMG_SRC + 'stoneback1.png'), (CARD_WIDTH, CARD_HEIGHT))
back_assets = [BACK1, BACK2, BACK3]

# Card Collections
WARRIOR = Legend('Mighty Warrior', WAR_CARD, WAR_CHAR)
ORC = Legend('Savage Goblin', ORC_CARD, ORC_CHAR)
KNIGHT = Legend('Skeleton Knight', KNT_CARD, KNIGHT_CHAR)
WIZARD = Legend('Sacred Wizard', WIZ_CARD, WIZARD_CHAR)
LEGENDS = [WARRIOR, ORC, KNIGHT, WIZARD]

Dragons = Monster(CardType.DRAGON, dragon_assets, dragon_info, 30, 3)
BEASTS = Monster(CardType.BEAST, beast_assets, beast_info, 10, 1)

ATTACK_ITEM = Item(CardType.ATTACK, attack_assets, atk_info, ATK_ICON)
DEFEND_ITEM = Item(CardType.DEFEND, defend_assets, def_info, DEF_ICON)
MAGIC_ITEM = Item(CardType.MAGIC, magic_assets, mag_info, MAG_ICON)
ITEMS = [ATTACK_ITEM, DEFEND_ITEM, MAGIC_ITEM]

HEAL_POTION = Potion(CardType.HEAL, heal_assets, hel_info, 10)
SPEED_POTION = Potion(CardType.SPEED, speed_assets, spd_info, 2)
POTIONS = [HEAL_POTION, SPEED_POTION]

BACKS = Card(CardType.BACK, back_assets, BACK1)

DICE1 = image.load(IMG_SRC + 'dice1.png')
DICE2 = image.load(IMG_SRC + 'dice2.png')
DICE3 = image.load(IMG_SRC + 'dice3.png')
DICE4 = image.load(IMG_SRC + 'dice4.png')
DICEICON = image.load(IMG_SRC + 'dice_icon.png')

# DICE BUTTON
class Dice:
    def __init__(self):
        self.icon = transform.scale(DICEICON, (TILE_WIDTH, TILE_WIDTH))
        self.numbers = [DICE1, DICE2, DICE3, DICE4]
        self.x = WIDTH - MARGIN - TILE_WIDTH
        self.y = HEIGHT - FOOTER - TILE_WIDTH - 5
        self.rect = Rect(self.x, self.y, TILE_WIDTH, TILE_WIDTH)

    def get_num_img(self, num):
        dice_img = self.numbers[num-1]
        return transform.scale(dice_img, (TILE_WIDTH, TILE_WIDTH))


DICE = Dice()

# CONTINUE BUTTON
CTN_IMG = transform.scale(image.load(IMG_SRC + 'continue_btn.png'), (150, 50))
num_base = image.load(IMG_SRC + 'profile.jpg')

LIGHT = Color(236, 240, 241)
GLASS = Color(236, 240, 241, 150)
BLUE = Color(41, 128, 185)
GREY = Color(52, 73, 94)
DARK = Color(44, 62, 80)
RED = Color(229, 20, 0)
GREEN = Color(46, 204, 113)
YELLOW = Color(241, 196, 15)
PURPLE = Color(142, 68, 173)
ORANGE = Color(230, 126, 34)
# touch_fx = pygame.mixer.Sound('../sound/dice.wav')
# card_fx = pygame.mixer.Sound('../sound/card.wav')
# dice_fx = pygame.mixer.Sound('../sound/dice2.wav')
