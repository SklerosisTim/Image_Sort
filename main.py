import pygame
import sys
import tkinter
import tkinter.filedialog
import pygame_gui
from os import listdir, path, remove, mkdir

pygame.init()
W, H = 1920, 1080
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 30
manager = pygame_gui.UIManager((W, H), 'main.json')
saving_folder = r'C:/kpop'
open_folder = "<Папка не выбрана>"
file_types = ['jpg', 'jpeg', 'png']
img_original = pygame.Surface((W, H))
img_opened = pygame.Surface((W, H))
img_name = ''
img_path = ''
all_girl_btn = []
stat_option = False
last_update = ''


# кнопки
class Button(pygame_gui.elements.UIButton):
    def __init__(self, x, y, w, h, text, mngr, visible=1):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (w, h)), text=text, manager=mngr,
                                              visible=visible)
        self.group = []


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
    global img_opened, img_original, img_path, img_name
    if open_folder != "<Папка не выбрана>":
        try:
            img = listdir(open_folder)[0]
            if img.split('.')[-1] in file_types:
                path_img = path.join(open_folder, img)
                original_img = pygame.image.load(path_img).convert()
                iw, ih = original_img.get_size()
                scale = min(W / iw, H / ih)
                new_size = (round(iw * scale), round(ih * scale))
                resize_img = pygame.transform.smoothscale(original_img, new_size)
                img_original = original_img
                img_opened = resize_img
                img_name = img
                img_path = path_img
            else:
                print(f'Формат {img.split(".")[-1]} не поддерживается')
        except IndexError:
            img_opened = pygame.Surface((W, H))


def save_load(name_target_folder):
    global last_update
    last_update = name_target_folder
    target_folder = path.join(saving_folder, name_target_folder)
    if not path.isdir(target_folder):
        mkdir(target_folder)
    if img_name != '':
        pygame.image.save(img_original, path.join(target_folder, img_name))
        print(f'{img_name} сохранено в {target_folder}')
        remove(img_path)
        image_load()


def switch_btn_visible(list_btn):
    if not list_btn:
        pass
    else:
        for btn in all_girl_btn:
            btn.visible = 0
        for btn in list_btn:
            btn.visible = 1


def button_draw():
    global all_girl_btn
    with open('buttons.txt', 'r', encoding='utf8') as girl_groups:
        x, y, w, h = 1670, 10, 240, 45
        for num, line in enumerate(girl_groups):
            if num == 21:
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
    stat = []
    for name in listdir(saving_folder):
        if name != '[Удалить]' and name != '[Прочее]':
            path_name = path.join(saving_folder, name)
            if path.isdir(path_name):
                stat.append([len(listdir(path_name)), name])
    stat.sort(reverse=True)
    place, step, upd = 1, 0, ''
    for value, name in stat:
        upd = '+' if name == last_update else ''
        print_text(f'{place}. {name}: {value} {upd}', 10, 10 + step, 'orange')
        place += 1
        step += 32
        if place == 31:
            break


def start():
    global open_folder, saving_folder, stat_option
    Button(W - 700, 1010, 240, 45, '[Прочее]', manager)
    Button(W - 960, 1010, 240, 45, '[Удалить]', manager)
    cycle = True
    while cycle:
        time_delta = clock.tick(fps)
        display.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if open_folder == "<Папка не выбрана>":
                        open_folder = prompt_folder()
                    else:
                        image_load()
                if event.key == pygame.K_q:
                    saving_folder = prompt_folder()
                if event.key == pygame.K_w:
                    stat_option = not stat_option
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                switch_btn_visible(event.ui_element.group)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                save_load(event.ui_element.text)

            manager.process_events(event)

        display.blit(img_opened, (W // 2 - img_opened.get_rect().centerx, H // 2 - img_opened.get_rect().centery))
        print_text(f'Источник: {open_folder}', 10, H - 40, f_color='red')
        print_text(f'Папка сохранения: {saving_folder}', 450, H - 40, f_color='red')
        if open_folder == "<Папка не выбрана>":
            print_text('<Пробел> - выбрать источник', 10, H - 80, f_color='red')
            print_text('<Q> - поменять папку сохранения', 450, H - 80, f_color='red')
        elif img_name == '':
            print_text('<Пробел> - загрузка изображения', 10, H - 80, f_color='red')
            print_text('<Q> - поменять папку сохранения', 450, H - 80, f_color='red')
        else:
            if not stat_option:
                print_text('<W> - включение статистики', 10, 10, 'red')
            print_text(f'Количество: {len(listdir(open_folder))}', 10, H - 80, f_color='red')
            print_text(img_name, 300, H - 80, f_color='red')

        statistic() if stat_option else None
        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    button_draw()
    statistic()
    start()

pygame.quit()
sys.exit()
