import tkinter
import tkinter.filedialog
import pygame_gui
from subprocess import run
from sys import exit
from os import listdir, path, remove, mkdir
from re import sub
from json import load, dump
from interface import *

iw, ih = 1920, 1080
clock = pygame.time.Clock()
fps = 30
manager = pygame_gui.UIManager((W, H), 'json/main.json')
img_original = pygame.Surface((W, H))
img_opened = pygame.Surface((W, H))
file_types = ('jpg', 'jpeg', 'png')
buttons = 'buttons.txt'
saving_folder = r'D:/[Photo]'
open_folder = ''
img_name = ''
img_path = ''
last_saving_img_path = ''
last_update_folder = ''
all_group_btn = []
all_girl_btn = []
stat = {}
stat_option = False
full_screen = False


def prompt_folder():  # диалоговое окно выбора папки
    top = tkinter.Tk()
    top.withdraw()
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def choice_buttons_layout():  # выбор макета кнопок
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def read_conf():
    global open_folder, saving_folder, buttons
    try:
        with open('json/config.json', 'r', encoding='utf8') as config_file:
            conf_dict = load(config_file)
            open_folder = conf_dict['open_folder']
            saving_folder = conf_dict['saving_folder']
            buttons = conf_dict['buttons']
    except FileNotFoundError:
        pass


def write_conf():
    conf_dict = {'open_folder': open_folder, 'saving_folder': saving_folder, 'buttons': buttons}
    with open('json/config.json', 'w', encoding='utf8') as config_file:
        dump(conf_dict, config_file, indent=2, ensure_ascii=False)


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
    global all_group_btn, all_girl_btn
    with open(buttons, 'r', encoding='utf8') as girl_groups:
        x, y, w, h = 1670, 10, 240, 45
        for num, line in enumerate(girl_groups):
            if num > 20:
                break
            group = line.split(' ')[0]
            group_btn = Button((x, y, w, h), group, manager)
            all_group_btn.append(group_btn)
            step = 0
            up_frame = 0
            bottom_frame = 22 - len(line.split(' '))
            if num > bottom_frame:
                up_frame -= (num - bottom_frame) * 50
            for girl in line.split(' ')[1:]:
                member = girl.rstrip()
                girl_btn = Button((x - 190, y + up_frame + step, w - 60, h), member, manager, visible=0)
                group_btn.group.append(girl_btn)
                all_girl_btn.append(girl_btn)
                step += 50
            y += 50


def buttons_kill():
    global all_group_btn, all_girl_btn
    [group.kill() for group in all_group_btn]
    [girl.kill() for girl in all_girl_btn]


def read_stat():
    global stat
    try:
        with open('json/stat.json', 'r', encoding='utf8') as stat_file:
            stat = load(stat_file)
    except FileNotFoundError:
        pass


def write_stat():
    folder_stat, sorted_stat = {}, {}
    for name in listdir(saving_folder):
        path_name = path.join(saving_folder, name)
        if path.isdir(path_name):
            folder_stat[name] = len(listdir(path_name))
    for key_value in sorted(folder_stat.items(), key=lambda item: item[1], reverse=True):
        sorted_stat[key_value[0]] = key_value[1]
    with open('json/stat.json', 'w', encoding='utf8') as stat_file:
        dump(sorted_stat, stat_file, indent=2, ensure_ascii=False)


def draw_stat():
    txt_stat = Text(30, position='left')
    place = 1
    for name, value in stat.items():
        if name not in ('[Удалить]', '[Прочее]', '[разобрать]'):
            txt_stat.shadow = 'orange' if name == last_update_folder else 'gray'
            txt_stat.write((10, 50 + place * 32, 300, 30), f'{place}. {name}: {value}')
            place += 1
            if place > 25:
                break


def full_screen_switch():
    global full_screen
    full_screen = not full_screen
    pygame.display.set_mode((W, H), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((W, H))


def color_resolution():  # возвращает цвет, в зависимости от разрешения фото
    if iw > ih:  # горизонтальные фото, смотрим ширину
        if iw < 1000:
            return 'red'
        elif iw < 1300:
            return 'orange'
    else:  # вертикальные фото, смотрим высоту
        if ih < 800:
            return 'red'
        elif ih < 1000:
            return 'orange'
    return 'gray50'


def start():
    global open_folder, saving_folder, stat_option, buttons
    read_conf()
    read_stat()
    buttons_draw()
    del_bt = Button((1300, 1030, 160, 45), '[Удалить]', manager)
    other_bt = Button((1130, 1030, 160, 45), '[Прочее]', manager)
    load_bt = Button((550, 930, 800, 60), 'Загрузить изображение', manager)
    input_bt = Button((10, 1000, 100, 35), '---', manager)
    output_bt = Button((10, 1040, 100, 35), '---', manager)
    stat_bt = Button((10, 10, 200, 45), 'Статистика', manager)
    f_bt = Button((220, 10, 50, 45), 'F', manager)
    z_bt = Button((280, 10, 50, 45), 'Z', manager)
    x_bt = Button((340, 10, 50, 45), 'X', manager)
    txt_brown = Text(30, f_color='brown', position='left')
    txt_file_info = Text(35, font='font/Morice-Bejar.ttf', shadow='orange')
    max_len = len(listdir(open_folder)) if open_folder else 1
    while True:
        time_delta = clock.tick(fps)
        display.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_conf()
                write_stat()
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    full_screen_switch()
                if event.key == pygame.K_z:
                    if last_saving_img_path:
                        pygame.time.wait(500)
                        run('explorer /select, ' + last_saving_img_path)
                if event.key == pygame.K_x:
                    buttons = choice_buttons_layout()
                    buttons_kill()
                    buttons_draw()
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element not in all_girl_btn:
                    switch_btn_visible(event.ui_element.group)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if open_folder:
                    if event.ui_element not in (load_bt, input_bt, output_bt, stat_bt, f_bt, z_bt, x_bt):
                        name_folder = sub('\n', '', event.ui_element.text)
                        save_load(name_folder)
                        stat[name_folder] += 1
                    if event.ui_element == load_bt:
                        image_load()
                    if event.ui_element == stat_bt:
                        stat_option = not stat_option
                if event.ui_element == input_bt:
                    open_folder = prompt_folder()
                    write_stat()
                    read_stat()
                    max_len = len(listdir(open_folder))
                if event.ui_element == output_bt:
                    saving_folder = prompt_folder()
                    write_stat()
                    read_stat()
                if event.ui_element == f_bt:
                    full_screen_switch()
                if event.ui_element == z_bt:
                    if last_saving_img_path:
                        pygame.time.wait(500)
                        run('explorer /select, ' + last_saving_img_path)
                if event.ui_element == x_bt:
                    buttons = choice_buttons_layout()
                    buttons_kill()
                    buttons_draw()

            manager.process_events(event)

        display.blit(img_opened, (W // 2 - img_opened.get_rect().centerx, H // 2 - img_opened.get_rect().centery))
        if open_folder and len(listdir(open_folder)):
            num = len(listdir(open_folder))
            pb = ProgressBar((200, 60), 50, max_bar=max_len, color1='gray50', shadow='orange')
            pb.draw((10, 930), f'{num}', num)
        txt_brown.write((120, 1000, 400, 35), f'Из: {open_folder}')
        txt_brown.write((120, 1040, 400, 35), f'В: {saving_folder}')
        load_bt.show() if open_folder and not img_name else load_bt.hide()
        if img_name:
            txt_file_info.rect = color_resolution()
            txt_file_info.write((800, 1030, 85, 45), f'{img_name.split('.')[-1]}')
            txt_file_info.write((890, 1030, 230, 45), f'{iw} / {ih}')
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
