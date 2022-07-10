from guzambi.game import Game
import pygame

def main():
    game = Game('Guzambi')
    running = True
    clock = pygame.time.Clock()
    while running:
        game.update_display()
        clock.tick(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                game.handle_click(event)

    pygame.quit()


if __name__ == '__main__':
    main()