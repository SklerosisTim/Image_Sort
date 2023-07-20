import pygame
import sys
import tkinter
import tkinter.filedialog

pygame.init()
W, H = 800, 600
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 60
path_folder = "<No File Selected>"


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return file_name


def start():
    global path_folder
    cycle = True
    while cycle:
        display.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                path_folder = prompt_file()

        pygame.display.set_caption(f"{path_folder}")
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
sys.exit()
