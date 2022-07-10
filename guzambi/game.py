from .constants import State
from .gui import GUI
from .board import Board

class Game:
    def __init__(self, title: str):
        self.state = State.SETTING
        self.board = Board()
        self.gui = GUI(title)

    def change_state(self):
        if self.state == State.SETTING:
            self.state = State.PLAYING
        elif self.state == State.PLAYING:
            self.state = State.GAMEOVER
        elif self.state == State.GAMEOVER:
            self.state = State.SETTING

    def update_display(self):
        if self.state == State.SETTING:
            self.gui.display_menu()
        elif self.state == State.PLAYING:
            self.gui.display_game(self.board)

    def handle_setting(self, pos):
        selected_hero = self.gui.get_selected_hero(pos)
        if selected_hero is None:
            return
        if self.board.set_hero(selected_hero):
            self.change_state()

    def handle_click(self, e):
        if self.state == State.SETTING:
            self.handle_setting(e.pos)
        elif self.state == State.PLAYING:
            if self.gui.dice_clicked(e.pos):
                num = self.board.roll_dice(1, 3)
                self.board.move_player(num)
                card = self.board.get_fortune_card()
                print(card.type)