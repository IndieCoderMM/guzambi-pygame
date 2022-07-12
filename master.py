from guzambi.game import Game
import pygame

def main():
    game = Game('Guzambi')
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                game.handle_click(event)

        game.update_display()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
