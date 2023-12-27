from subprocess import run
from sys import exit
from os import listdir, path, remove, mkdir
from json import load, dump
from interface import *

iw, ih = 1920, 1080
clock = pygame.time.Clock()
fps = 30
img_original = pygame.Surface((W, H))  # оригинальная фото
img_opened = pygame.Surface((W, H))  # подогнанная под экран фото
file_types = ('jpg', 'jpeg', 'png')  # поддерживаемые расширения
buttons = 'buttons.txt'  # макет кнопок
saving_folder = r'D:/[Photo]'  # целевая папка
open_folder = ''  # рабочая папка
img_name = ''  # имя открытой фото
img_path = ''  # путь к открытой фото
last_saving_img_path = ''  # путь к последней сохраненной фото
last_update_folder = ''  # папка последней сохраненной фото
all_group_btn = []  # родительские кнопки
all_girl_btn = []  # дочерние кнопки
stat = {}  # статистика
stat_option = False
full_screen = False
scroll = False
stat_num = 0  # начальное положение статистики


def read_conf():  # чтение конфига из json
    global open_folder, saving_folder, buttons
    try:
        with open('json/config.json', 'r', encoding='utf8') as config_file:
            conf_dict = load(config_file)
            open_folder = conf_dict['open_folder']
            saving_folder = conf_dict['saving_folder']
            buttons = conf_dict['buttons']
    except FileNotFoundError:  # если конфига нет - используем настройки по умолчанию
        pass


def write_conf():  # запись конфига в json
    conf_dict = {'open_folder': open_folder, 'saving_folder': saving_folder, 'buttons': buttons}
    with open('json/config.json', 'w', encoding='utf8') as config_file:
        dump(conf_dict, config_file, indent=2, ensure_ascii=False)


def image_load():  # отрисовка фото на экране
    global open_folder, img_opened, img_path, img_name, img_original, iw, ih
    img_list = listdir(open_folder)
    if len(img_list) > 0:  # проверка на наличие фото в рабочей папке
        for img in img_list:
            if img.split('.')[-1] in file_types:  # проверка поддерживаемых расширений фото
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
                return  # закрываем функцию если фото успешно загружено, если нет - идем дальше по циклу
    open_folder = ''  # если рабочая папка не содержит файлов с поддерживаемыми расширениями - обнуляем все переменные
    img_opened = pygame.Surface((W, H))
    img_name = ''
    img_path = ''


def save_load(name_target_folder):  # перенос фото из рабочей папки в целевую
    global last_update_folder, last_saving_img_path
    last_update_folder = name_target_folder
    target_folder = path.normpath(path.join(saving_folder, name_target_folder))  # путь к целевой папке
    if not path.isdir(target_folder):  # если целевой папки нет - создаем
        mkdir(target_folder)
    if img_name:
        last_saving_img_path = path.normpath(path.join(target_folder, img_name))  # путь к фото для сохранения
        pygame.image.save(img_original, last_saving_img_path)  # сохраняем фото в целевую папку
        print(f'{img_name} сохранено в {target_folder}')
        remove(img_path)  # удаляем фото из рабочей папки
        image_load()


def switch_btn_visible(list_btn):  # переключение отображения дочерних кнопок
    for btn in all_girl_btn:  # сначала выключается видимость всех дочерних кнопок
        btn.visible = 0
    if list_btn:  # если передан список дочерних кнопок - включается их видимость
        for btn in list_btn:
            btn.visible = 1


def buttons_draw():  # отрисовка кнопок
    global all_group_btn, all_girl_btn
    with open(buttons, 'r', encoding='utf8') as girl_groups:  # читаем макет кнопок из txt-файла
        x, y, w, h = 1670, 10, 240, 45
        for num, line in enumerate(girl_groups):  # построчный перебор макета
            if num > 20:  # максимум кнопок - 21
                break
            group = line.split(' ')[0]  # родительская кнопка - первое слово в строке
            group_btn = Button((x, y, w, h), group, manager)
            all_group_btn.append(group_btn)  # добавление в группу родительских кнопок
            step = 0  # сдвиг дочерних кнопок по вертикали вниз
            up_frame = 0  # положение верхней дочерней кнопки по отношению к родительской
            bottom_frame = 22 - len(line.split(' '))  # положение нижней кнопки
            if num > bottom_frame:  # если нижняя кнопка выходит за рамки экрана
                up_frame -= (num - bottom_frame) * 50  # тогда верхняя кнопка сдвигается вверх на нужное расстояние
            for girl in line.split(' ')[1:]:
                member = girl.rstrip()  # дочерние кнопки - все последующие слова в строке
                girl_btn = Button((x - 190, y + up_frame + step, w - 60, h), member, manager, visible=0)
                group_btn.group.append(girl_btn)  # присвоение дочерней кнопки к родительской
                all_girl_btn.append(girl_btn)  # добавление в группу дочерних кнопок
                step += 50  # для дочерних кнопок
            y += 50  # для родительских кнопок


def buttons_kill():  # очистка списков кнопок
    global all_group_btn, all_girl_btn
    [group.kill() for group in all_group_btn]
    [girl.kill() for girl in all_girl_btn]


def read_stat():  # чтение статистики из json
    global stat
    try:
        with open('json/stat.json', 'r', encoding='utf8') as stat_file:
            stat = load(stat_file)
    except FileNotFoundError:
        pass


def write_stat():  # реальный подсчет, сортировка и запись статистики в json
    folder_stat, sorted_stat = {}, {}
    for name in listdir(saving_folder):
        path_name = path.join(saving_folder, name)
        if path.isdir(path_name) and not name.startswith('['):
            folder_stat[name] = len(listdir(path_name))
    for key_value in sorted(folder_stat.items(), key=lambda item: item[1], reverse=True):
        sorted_stat[key_value[0]] = key_value[1]
    with open('json/stat.json', 'w', encoding='utf8') as stat_file:
        dump(sorted_stat, stat_file, indent=2, ensure_ascii=False)


def update_stat(name_folder):  # упрощенное обновление статистики без реального подсчета файлов
    global stat
    if name_folder.startswith('['):
        return
    sorted_stat = {}
    stat[name_folder] = stat[name_folder] + 1 if name_folder in stat else 1
    for key_value in sorted(stat.items(), key=lambda item: item[1], reverse=True):  # заново сортируем словарь
        sorted_stat[key_value[0]] = key_value[1]
    stat = sorted_stat


def draw_stat():  # отрисовка статистики
    place = 1
    for num, name_value in enumerate(stat.items()):
        if num >= stat_num:  # определяем начало статистики для отрисовки
            txt_stat.shadow = 'orange' if name_value[0] == last_update_folder else 'gray'
            txt = f'{place + stat_num}. {name_value[0]}: {name_value[1]}'
            txt_stat.write((10, 30 + place * 32, 300, 30), txt)
            place += 1
            if num > 23 + stat_num:  # определяем конец статистики для отрисовки
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


def stat_scroll(vector):  # прокрутка статистики
    global stat_num
    if vector < 0:
        if stat_num > 0:
            stat_num -= 1
    else:
        if stat_num < len(stat) - 25:
            stat_num += 1


def start():  # главный цикл
    global open_folder, saving_folder, stat_option, buttons, scroll, stat_num
    read_conf()
    read_stat()
    buttons_draw()
    max_len = len(listdir(open_folder)) if open_folder else 1
    show_message, timer = False, 30
    while True:
        time_delta = clock.tick(fps)
        display.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # запись конфига и статистики при закрытии программы
                write_conf()
                write_stat()
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:  # горячие клавиши
                if event.key == pygame.K_f:  # полноэкранный режим
                    full_screen_switch()
                if event.key == pygame.K_z:  # открытие последнего сохраненного фото в проводнике
                    if last_saving_img_path:
                        pygame.time.wait(500)
                        run('explorer /select, ' + last_saving_img_path)
                if event.key == pygame.K_x:  # смена макета кнопок
                    buttons = choice_buttons_layout()
                    buttons_kill()
                    buttons_draw()
            if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
                if event.ui_element in all_group_btn:  # при наведении на родительскую кнопку
                    switch_btn_visible(event.ui_element.group)  # показываются ее дочерние - чужие скрываются
                if event.ui_element == stat_bt:  # включение режима прокрутки при наведении на кнопку
                    scroll = True
            if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                if event.ui_element == stat_bt:  # выключение режима прокрутки
                    scroll = False
            if event.type == pygame.MOUSEBUTTONDOWN and scroll:  # прокрутка статистики
                if event.button == 4:
                    stat_scroll(-1)
                if event.button == 5:
                    stat_scroll(1)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if open_folder:
                    if event.ui_element in all_girl_btn + all_group_btn + [del_bt, other_bt]:
                        name_folder = event.ui_element.text.rstrip()  # текст кнопки = папка переноса
                        save_load(name_folder)  # перенос фото в новую папку
                        update_stat(name_folder)  # упрощенное обновление статистики
                        if not show_message:  # включение сообщения о сохранении фото
                            show_message = True
                        else:  # если сообщение уже было - таймер запускается заново
                            timer = 30
                    if event.ui_element == load_bt:
                        image_load()
                    if event.ui_element == stat_bt:  # вкл./откл. статистики
                        stat_option = not stat_option
                        stat_num = 0
                if event.ui_element == input_bt:  # выбор рабочей папки
                    open_folder = prompt_folder()
                    max_len = len(listdir(open_folder)) if open_folder else 1
                if event.ui_element == output_bt:  # выбор папки сохранения
                    saving_folder = prompt_folder()
                    write_stat()
                    read_stat()
                if event.ui_element == f_bt:  # полноэкранный режим
                    full_screen_switch()
                if event.ui_element == z_bt:  # открытие последнего сохраненного фото в проводнике
                    if last_saving_img_path:
                        pygame.time.wait(500)
                        run('explorer /select, ' + last_saving_img_path)
                if event.ui_element == x_bt:  # смена макета кнопок
                    buttons = choice_buttons_layout()
                    buttons_kill()
                    buttons_draw()

            manager.process_events(event)

        timer = timer - 1 if show_message else 30  # если показано сообщение - работает таймер
        show_message = False if timer < 1 else show_message  # сообщение тушится когда таймер на 0
        display.blit(img_opened, (960 - img_opened.get_rect().centerx, 540 - img_opened.get_rect().centery))
        if open_folder and len(listdir(open_folder)):  # прогресс бар со счетчиком файлов в рабочей папке
            num = len(listdir(open_folder))
            pb = ProgressBar((200, 60), 50, max_bar=max_len, color1='gray50', shadow='orange')
            pb.draw((10, 930), f'{num}', num)
        txt_brown.write((120, 1000, 400, 35), f'Из: {open_folder}')
        txt_brown.write((120, 1040, 400, 35), f'В: {saving_folder}')
        load_bt.show() if open_folder and not img_name else load_bt.hide()
        if show_message:  # сообщение о сохраненном фото с указанием целевой папки
            w = 280 + (len(last_update_folder) * 20)  # ширина сообщения зависит от длинны названия целевой папки
            txt_message.write(((960 - (w // 2)), 980, w, 45), f'Сохранено в {last_update_folder}')
        if img_name:  # отрисовка инфо о фото, расширение и размеры
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
