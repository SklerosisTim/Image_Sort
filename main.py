import pygame
import sys
import tkinter
import tkinter.filedialog
from os import listdir, path

pygame.init()
W, H = 800, 600
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 30
path_folder = "<No File Selected>"


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return file_name


def image():
    if path_folder != "<No File Selected>":
        try:
            img = listdir(path_folder)[0]
            path_img = path.join(path_folder, img)
            original_img = pygame.image.load(path_img).convert()
            iw, ih = original_img.get_size()
            scale = min(600 / iw, 600 / ih)
            new_size = (round(iw * scale), round(ih * scale))
            resize_img = pygame.transform.smoothscale(original_img, new_size)
            return resize_img
        except IndexError:
            pass


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
        if path_folder != "<No File Selected>":
            display.blit(image(), (300 - image().get_rect().centerx, 300 - image().get_rect().centery))
        pygame.display.set_caption(f"{path_folder}")
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
sys.exit()
