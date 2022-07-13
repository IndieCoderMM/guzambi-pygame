import pygame
import guzambi

def main():
    game = guzambi.Game('Guzambi')
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


# TODO: Features to Add
#   1. Add attributes to each character
#   2. Display card info
#   3. Add sound effects
