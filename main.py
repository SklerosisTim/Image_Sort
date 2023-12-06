import tkinter
import tkinter.filedialog
import pygame
import pygame_gui
from subprocess import run
from sys import exit
from os import listdir, path, remove, mkdir
from re import sub

pygame.init()
W, H = 1920, 1080
iw, ih = 1920, 1080
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 30
manager = pygame_gui.UIManager((W, H), 'main.json')
saving_folder = r'D:\[Photo]'
open_folder = ''
file_types = ('jpg', 'jpeg', 'png')
img_original = pygame.Surface((W, H))
img_opened = pygame.Surface((W, H))
img_name = ''
img_path = ''
last_saving_img_path = ''
all_girl_btn = []
stat_option = False
last_update_folder = ''
stat = []
full_screen = False
len_open_folder = 0


# кнопки
class Button(pygame_gui.elements.UIButton):
    def __init__(self, x, y, w, h, text, mngr, visible=1):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (w, h)), text=text, manager=mngr,
                                              visible=visible)
        self.group = []


# надписи
def print_text(message, x, y, f_color='black', bg_color=None, f_size=30, font='arial'):
    font_type = pygame.font.SysFont(font, f_size)
    shadow_surf = font_type.render(message, True, 'white')
    text_surf = font_type.render(message, True, f_color, bg_color)
    display.blit(shadow_surf, (x + 1, y + 1))
    display.blit(text_surf, (x, y))


# диалоговое окно выбора папки
def prompt_folder():
    top = tkinter.Tk()
    top.withdraw()
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def image_load():
    global open_folder, img_opened, img_path, img_name, img_original, iw, ih
    img_list = listdir(open_folder)
    if len(img_list) > 0:
        for img in img_list:
            if img.split('.')[-1] in file_types:
                path_img = path.join(open_folder, img)
                original = pygame.image.load(path_img).convert()
                iw, ih = original.get_size()
                scale = min(W / iw, H / ih)
                new_size = (round(iw * scale), round(ih * scale))
                resize_img = pygame.transform.smoothscale(original, new_size)
                img_original = original
                img_opened = resize_img
                img_name = img
                img_path = path_img
                return
    open_folder = ''
    img_opened = pygame.Surface((W, H))
    img_name = ''
    img_path = ''


def save_load(name_target_folder):
    global last_update_folder, last_saving_img_path
    last_update_folder = name_target_folder
    target_folder = path.normpath(path.join(saving_folder, name_target_folder))
    if not path.isdir(target_folder):
        mkdir(target_folder)
    if img_name:
        last_saving_img_path = path.normpath(path.join(target_folder, img_name))
        pygame.image.save(img_original, last_saving_img_path)
        print(f'{img_name} сохранено в {target_folder}')
        remove(img_path)
        image_load()


def switch_btn_visible(list_btn):
    for btn in all_girl_btn:
        btn.visible = 0
    if list_btn:
        for btn in list_btn:
            btn.visible = 1


def buttons_draw():
    global all_girl_btn
    with open('buttons.txt', 'r', encoding='utf8') as girl_groups:
        x, y, w, h = 1670, 10, 240, 45
        for num, line in enumerate(girl_groups):
            if num > 20:
                break
            group = line.split(' ')[0]
            group_btn = Button(x, y, w, h, group, manager)
            step = 0
            up_frame = 0
            bottom_frame = 22 - len(line.split(' '))
            if num > bottom_frame:
                up_frame -= (num - bottom_frame) * 50
            for girl in line.split(' ')[1:]:
                member = girl.rstrip()
                girl_btn = Button(x - 190, y + up_frame + step, w - 60, h, member, manager, visible=0)
                group_btn.group.append(girl_btn)
                all_girl_btn.append(girl_btn)
                step += 50
            y += 50


def statistic():
    stat.clear()
    for name in listdir(saving_folder):
        if name not in ('[Удалить]', '[Прочее]'):
            path_name = path.join(saving_folder, name)
            if path.isdir(path_name):
                stat.append([len(listdir(path_name)), name])
    stat.sort(reverse=True)


def draw_stat():
    place, step = 1, 0
    for value, name in stat:
        upd_color = 'yellow' if name == last_update_folder else None
        print_text(f'{place}. {name}: {value}', 10, 60 + step, bg_color=upd_color)
        place += 1
        step += 32
        if place > 25:
            break


def full_screen_switch():
    global display, full_screen
    full_screen = not full_screen
    if full_screen:
        display = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((W, H))


def prog_bar(x, y, w, h, progress, max_progress=100, color1='gray', bg_color='black', surf=display):
    pygame.draw.rect(surf, bg_color, (x, y, w, h))
    progress = max_progress if progress > max_progress else progress
    pygame.draw.rect(surf, color1, (x, y, w, progress / max_progress * h))


def start():
    global open_folder, saving_folder, stat_option, len_open_folder
    del_bt = Button(10, H - 130, 160, 45, '[Удалить]', manager)
    other_bt = Button(180, H - 130, 160, 45, '[Прочее]', manager)
    load_bt = Button(550, H - 150, 800, 60, 'Загрузить изображение', manager)
    input_bt = Button(10, H - 80, 100, 35, '---', manager)
    output_bt = Button(10, H - 40, 100, 35, '---', manager)
    stat_bt = Button(10, 10, 200, 45, 'Статистика', manager)
    f_bt = Button(220, 10, 50, 45, 'F', manager)
    z_bt = Button(280, 10, 50, 45, 'Z', manager)
    buttons_draw()
    while True:
        time_delta = clock.tick(fps)
        display.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    full_screen_switch()
                if event.key == pygame.K_z:
                    if last_saving_img_path:
                        pygame.time.wait(200)
                        run('explorer /select, ' + last_saving_img_path)

            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element not in all_girl_btn:
                    switch_btn_visible(event.ui_element.group)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if open_folder:
                    if event.ui_element not in (load_bt, input_bt, output_bt, stat_bt, f_bt, z_bt):
                        save_load(sub('\n', '', event.ui_element.text))
                        statistic()
                    if event.ui_element == load_bt:
                        image_load()
                        statistic()
                    if event.ui_element == stat_bt:
                        stat_option = not stat_option
                if event.ui_element == input_bt:
                    open_folder = prompt_folder()
                    len_open_folder = len(listdir(open_folder)) if open_folder else 0
                if event.ui_element == output_bt:
                    saving_folder = prompt_folder()
                if event.ui_element == f_bt:
                    full_screen_switch()
                if event.ui_element == z_bt:
                    if last_saving_img_path:
                        pygame.time.wait(200)
                        run('explorer /select, ' + last_saving_img_path)

            manager.process_events(event)

        display.blit(img_opened, (W // 2 - img_opened.get_rect().centerx, H // 2 - img_opened.get_rect().centery))
        if open_folder and len(listdir(open_folder)):
            prog_bar(W - 5, 0, 5, H, len_open_folder - len(listdir(open_folder)), len_open_folder)
        num = len(listdir(open_folder)) if open_folder else 0
        print_text(f'Из: {open_folder} ({num})', 120, H - 80, 'brown')
        print_text(f'В: {saving_folder}', 120, H - 40, 'brown')
        load_bt.show() if open_folder and not img_name else load_bt.hide()
        if img_name:
            print_text(f'{img_name}  ( {iw} / {ih} )', 340, 10, 'brown')
            del_bt.show()
            other_bt.show()
        else:
            del_bt.hide()
            other_bt.hide()

        draw_stat() if stat_option else None
        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
exit()
