import pygame
import sys
import tkinter
import tkinter.filedialog
import pygame_gui as pg
from os import listdir, path, remove

pygame.init()
W, H = 1920, 1080
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 30
manager = pg.UIManager((W, H), 'json/main.json')
open_folder = "<No File Selected>"
file_types = ['jpg', 'jpeg', 'png']
img_opened = pygame.image.load('Mina-Sana-Kfapfakes.jpg').convert()
img_name = ''
img_path = ''


# кнопки
class Button(pg.elements.UIButton):
    def __init__(self, x, y, w, h, text, mngr, visible=1):
        pg.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (w, h)), text=text, manager=mngr,
                                      visible=visible)


# выпадающее меню
class DDMenu(pg.elements.UIDropDownMenu):
    def __init__(self, x, y, w, h, options_list, starting_option, mngr):
        pg.elements.UIDropDownMenu.__init__(self, relative_rect=pygame.Rect((x, y), (w, h)),
                                            options_list=options_list, starting_option=starting_option, manager=mngr)


# надписи
def print_text(message, x, y, f_color='black', bg_color=None, f_size=30, font='arial'):
    font_type = pygame.font.SysFont(font, f_size)
    text_surf = font_type.render(message, True, f_color, bg_color)
    display.blit(text_surf, (x, y))


# диалоговое окно выбора папки
def prompt_folder():
    top = tkinter.Tk()
    top.withdraw()
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def image_load():
    global img_opened, img_path, img_name
    if open_folder != "<No File Selected>":
        try:
            img = listdir(open_folder)[0]
            if img.split('.')[-1] in file_types:
                path_img = path.join(open_folder, img)
                original_img = pygame.image.load(path_img).convert()
                iw, ih = original_img.get_size()
                scale = min(W / iw, H / ih)
                new_size = (round(iw * scale), round(ih * scale))
                resize_img = pygame.transform.smoothscale(original_img, new_size)
                img_opened = resize_img
                img_name = img
                img_path = path_img
                print(f'Загружена картинка {img_path}')
            else:
                print(f'Формат {img.split(".")[-1]} не поддерживается')
        except IndexError:
            img_opened = pygame.image.load('Mina-Sana-Kfapfakes.jpg').convert()


Aespa = Button(W - 200, 10, 190, 40, 'Aespa', manager)
winter = Button(W - 350, 10, 140, 40, 'Винтер', manager, visible=0)
giselle = Button(W - 350, 60, 140, 40, 'Жизель', manager, visible=0)
karina = Button(W - 350, 110, 140, 40, 'Карина', manager, visible=0)
ningning = Button(W - 350, 160, 140, 40, 'НинНин', manager, visible=0)

Dreamcatcher = Button(W - 200, 60, 190, 40, 'Dreamcatcher', manager)
Everglow = Button(W - 200, 110, 190, 40, 'Everglow', manager)
Fromis_9 = Button(W - 200, 160, 190, 40, 'Fromis_9', manager)
Gidle = Button(W - 200, 210, 190, 40, 'Gidle', manager)
ITZY = Button(W - 200, 260, 190, 40, 'ITZY', manager)
IVE = Button(W - 200, 310, 190, 40, 'IVE', manager)
Kep1er = Button(W - 200, 360, 190, 40, 'Kep1er', manager)
LeSserafim = Button(W - 200, 410, 190, 40, 'LeSserafim', manager)
LOONA = Button(W - 200, 460, 190, 40, 'LOONA', manager)
Lovelyz = Button(W - 200, 510, 190, 40, 'Lovelyz', manager)
Mamamoo = Button(W - 200, 560, 190, 40, 'Mamamoo', manager)
Momoland = Button(W - 200, 610, 190, 40, 'Momoland', manager)
NMIXX = Button(W - 200, 660, 190, 40, 'NMIXX', manager)
Oh_My_Girl = Button(W - 200, 710, 190, 40, 'Oh My Girl', manager)
Red_Velvet = Button(W - 200, 760, 190, 40, 'Red Velvet', manager)
Rocket_Punch = Button(W - 200, 810, 190, 40, 'Rocket Punch', manager)
TWICE = Button(W - 200, 860, 190, 40, 'TWICE', manager)
VIVIZ = Button(W - 200, 910, 190, 40, 'VIVIZ', manager)
WJSN = Button(W - 200, 960, 190, 40, 'WJSN', manager)
Solo = Button(W - 200, 1010, 190, 40, 'SOLO', manager)


def start():
    global open_folder
    cycle = True
    while cycle:
        time_delta = clock.tick(fps)
        display.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    open_folder = prompt_folder()
                if event.key == pygame.K_SPACE:
                    image_load()

            if event.type == pg.UI_BUTTON_PRESSED:
                if event.ui_element == Aespa:
                    winter.visible = 1 if winter.visible == 0 else 0
                    giselle.visible = 1 if giselle.visible == 0 else 0
                    karina.visible = 1 if karina.visible == 0 else 0
                    ningning.visible = 1 if ningning.visible == 0 else 0
                if event.ui_element == winter:
                    pygame.image.save(img_opened, path.join(r'C:\kpop\Aespa\Винтер', img_name))
                    remove(img_path)
                    image_load()
                if event.ui_element == giselle:
                    pygame.image.save(img_opened, path.join(r'C:\kpop\Aespa\Жизель', img_name))
                    remove(img_path)
                    image_load()
                if event.ui_element == karina:
                    pygame.image.save(img_opened, path.join(r'C:\kpop\Aespa\Карина', img_name))
                    remove(img_path)
                    image_load()
                if event.ui_element == ningning:
                    pygame.image.save(img_opened, path.join(r'C:\kpop\Aespa\НинНин', img_name))
                    remove(img_path)
                    image_load()

            manager.process_events(event)

        display.blit(img_opened, (W // 2 - img_opened.get_rect().centerx, H // 2 - img_opened.get_rect().centery))
        print_text(f'{open_folder}', 10, H - 40, f_color='red')
        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
sys.exit()
