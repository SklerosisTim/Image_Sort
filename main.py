import pygame
import sys
import pygame_gui as pg

pygame.init()
W, H = 800, 600
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 60


def start():
    manager = pg.UIManager((W, H), 'json/main.json')
    display.fill('white')
    cycle = True
    while cycle:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
sys.exit()
