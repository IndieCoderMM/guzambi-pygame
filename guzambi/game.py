import pygame.time

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
        elif self.state == State.PAUSE:
            self.state = State.PLAYING

    def pause(self):
        self.state = State.PAUSE

    def update_display(self):
        if self.state == State.SETTING:
            self.gui.display_menu(self.board)
        elif self.state == State.PLAYING:
            self.gui.display_game(self.board)
        elif self.state == State.GAMEOVER:
            self.gui.display_gameover(self.board)

    def handle_setting(self, pos):
        selected_hero = self.gui.get_selected_hero(pos)
        if selected_hero is None:
            return
        if self.board.set_hero(selected_hero):
            self.gui.display_menu(self.board)
            self.change_state()

    def handle_click(self, e):
        if self.state == State.SETTING:
            self.handle_setting(e.pos)
        elif self.state == State.PLAYING:
            if self.gui.dice_clicked(e.pos):
                self.gui.draw_dice_animation(self.board)
                num = self.board.roll_dice()
                self.board.move_player(num)
                self.board.get_fortune_card()
                self.update_display()
                self.gui.display_info('Click anywhere to continue')
                self.gui.show_dice_num(num)
                self.pause()
        elif self.state == State.PAUSE:
            self.board.take_action()

            if self.board.winner is not None:
                self.state = State.GAMEOVER
            else:
                self.change_state()
        elif self.state == State.GAMEOVER:
            self.board = Board()
            self.change_state()
