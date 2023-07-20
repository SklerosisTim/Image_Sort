import pygame
import sys
import tkinter
import tkinter.filedialog
import pygame_gui as pg
from os import listdir, path, remove, mkdir

pygame.init()
W, H = 1920, 1080
display = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 30
manager = pg.UIManager((W, H), 'json/main.json')
open_folder = "<No File Selected>"
file_types = ['jpg', 'jpeg', 'png']
img_opened = pygame.Surface((1920, 1080))
img_name = ''
img_path = ''


# кнопки
class Button(pg.elements.UIButton):
    def __init__(self, x, y, w, h, text, mngr, visible=1):
        pg.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (w, h)), text=text, manager=mngr,
                                      visible=visible)


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
            else:
                print(f'Формат {img.split(".")[-1]} не поддерживается')
        except IndexError:
            img_opened = pygame.image.load('Mina-Sana-Kfapfakes.jpg').convert()


def save_load(name_target_folder):
    target_folder = path.join(r'C:\kpop\[Тест]', name_target_folder)
    if not path.isdir(target_folder):
        mkdir(target_folder)
    pygame.image.save(img_opened, path.join(target_folder, img_name))
    remove(img_path)
    image_load()


def switch_btn_visible(list_btn):
    global all_btn
    for btn in all_btn:
        btn.visible = 0
    for btn in list_btn:
        btn.visible = 1


Aespa = Button(W - 250, 10, 240, 45, 'Aespa', manager)
winter = Button(W - 440, 10, 180, 45, 'Винтер', manager, visible=0)
giselle = Button(W - 440, 60, 180, 45, 'Жизель', manager, visible=0)
karina = Button(W - 440, 110, 180, 45, 'Карина', manager, visible=0)
ningning = Button(W - 440, 160, 180, 45, 'НинНин', manager, visible=0)
Aespa_btn = [winter, giselle, karina, ningning]

Blackpink = Button(W - 250, 60, 240, 45, 'Blackpink', manager)
jennie = Button(W - 440, 60, 180, 45, 'Дженни', manager, visible=0)
jisoo = Button(W - 440, 110, 180, 45, 'Джису', manager, visible=0)
lisa = Button(W - 440, 160, 180, 45, 'Лиса', manager, visible=0)
rose = Button(W - 440, 210, 180, 45, 'Розэ', manager, visible=0)
Blackpink_btn = [jennie, jisoo, lisa, rose]

Dreamcatcher = Button(W - 250, 110, 240, 45, 'Dreamcatcher', manager)
gah = Button(W - 440, 110, 180, 45, 'Гахён', manager, visible=0)
dami = Button(W - 440, 160, 180, 45, 'Дами', manager, visible=0)
jiu = Button(W - 440, 210, 180, 45, 'Джию', manager, visible=0)
sua = Button(W - 440, 260, 180, 45, 'Суа', manager, visible=0)
dongie = Button(W - 440, 310, 180, 45, 'Хандон', manager, visible=0)
sieon = Button(W - 440, 360, 180, 45, 'Шиён', manager, visible=0)
yooheon = Button(W - 440, 410, 180, 45, 'Юхён', manager, visible=0)
Dreamcatcher_btn = [gah, dami, jiu, sua, dongie, sieon, yooheon]

Everglow = Button(W - 250, 160, 240, 45, 'Everglow', manager)
aisha = Button(W - 440, 160, 180, 45, 'Айша', manager, visible=0)
iron = Button(W - 440, 210, 180, 45, 'Ирон', manager, visible=0)
mia = Button(W - 440, 260, 180, 45, 'Миа', manager, visible=0)
onda = Button(W - 440, 310, 180, 45, 'Онда', manager, visible=0)
siheon = Button(W - 440, 360, 180, 45, 'Шихён', manager, visible=0)
eu = Button(W - 440, 410, 180, 45, 'EU', manager, visible=0)
Everglow_btn = [aisha, iron, mia, onda, siheon, eu]

Fromis_9 = Button(W - 250, 210, 240, 45, 'Fromis_9', manager)
guri = Button(W - 440, 210, 180, 45, 'Гюри', manager, visible=0)
jiwon = Button(W - 440, 260, 180, 45, 'Дживон', manager, visible=0)
jisun = Button(W - 440, 310, 180, 45, 'Джисун', manager, visible=0)
jiheon = Button(W - 440, 360, 180, 45, 'Джихён', manager, visible=0)
nageon = Button(W - 440, 410, 180, 45, 'Нагён', manager, visible=0)
saerom = Button(W - 440, 460, 180, 45, 'Сэром', manager, visible=0)
haeon = Button(W - 440, 510, 180, 45, 'Хаён', manager, visible=0)
Fromis_9_btn = [guri, jiwon, jisun, jiheon, nageon, saerom, haeon]

Gidle = Button(W - 250, 260, 240, 45, 'Gidle', manager)
mieon = Button(W - 440, 260, 180, 45, 'Миён', manager, visible=0)
minni = Button(W - 440, 310, 180, 45, 'Минни', manager, visible=0)
soeon = Button(W - 440, 360, 180, 45, 'Соён', manager, visible=0)
sujin = Button(W - 440, 410, 180, 45, 'Суджин', manager, visible=0)
shuhua = Button(W - 440, 460, 180, 45, 'Шухуа', manager, visible=0)
uqi = Button(W - 440, 510, 180, 45, 'Юки', manager, visible=0)
Gidle_btn = [mieon, minni, soeon, sujin, shuhua, uqi]

ITZY = Button(W - 250, 310, 240, 45, 'ITZY', manager)
eji = Button(W - 440, 310, 180, 45, 'Еджи', manager, visible=0)
lia = Button(W - 440, 360, 180, 45, 'Лиа', manager, visible=0)
rujin = Button(W - 440, 410, 180, 45, 'Рюджин', manager, visible=0)
chaeren = Button(W - 440, 460, 180, 45, 'Чeрён', manager, visible=0)
yuna = Button(W - 440, 510, 180, 45, 'Юна', manager, visible=0)
ITZY_btn = [eji, lia, rujin, chaeren, yuna]

IVE = Button(W - 250, 360, 240, 45, 'IVE', manager)
woneon = Button(W - 440, 360, 180, 45, 'Вонён', manager, visible=0)
yujin = Button(W - 440, 410, 180, 45, 'Юджин', manager, visible=0)
IVE_btn = [woneon, yujin]

Kep1er = Button(W - 250, 410, 240, 45, 'Kep1er', manager)
dayeon = Button(W - 440, 410, 180, 45, 'Даён', manager, visible=0)
yenyn = Button(W - 440, 460, 180, 45, 'Енын', manager, visible=0)
xaotin = Button(W - 440, 510, 180, 45, 'Сяотин', manager, visible=0)
yujin_kp = Button(W - 440, 560, 180, 45, 'Юджин', manager, visible=0)
Kep1er_btn = [dayeon, yenyn, xaotin, yujin_kp]

LeSserafim = Button(W - 250, 460, 240, 45, 'LeSserafim', manager)
kazuha = Button(W - 440, 460, 180, 45, 'Казуха', manager, visible=0)
sakura = Button(W - 440, 510, 180, 45, 'Сакура', manager, visible=0)
chaewon = Button(W - 440, 560, 180, 45, 'Чевон', manager, visible=0)
yunjin = Button(W - 440, 610, 180, 45, 'Юнджин', manager, visible=0)
LeSserafim_btn = [kazuha, sakura, chaewon, yunjin]

LOONA = Button(W - 250, 510, 240, 45, 'LOONA', manager)
vivi = Button(W - 440, 460, 180, 45, 'Виви', manager, visible=0)
gowon = Button(W - 440, 510, 180, 45, 'Говон', manager, visible=0)
jinsoul = Button(W - 440, 560, 180, 45, 'Джинсоль', manager, visible=0)
yojin = Button(W - 440, 610, 180, 45, 'Ёджин', manager, visible=0)
ives = Button(W - 440, 660, 180, 45, 'Ив', manager, visible=0)
kimlip = Button(W - 440, 710, 180, 45, 'Ким Лип', manager, visible=0)
olivia = Button(W - 440, 760, 180, 45, 'Оливия Хе', manager, visible=0)
hasyl = Button(W - 440, 810, 180, 45, 'Хасыль', manager, visible=0)
heonjin = Button(W - 440, 860, 180, 45, 'Хёнджин', manager, visible=0)
heejin = Button(W - 440, 910, 180, 45, 'Хиджин', manager, visible=0)
choerry = Button(W - 440, 960, 180, 45, 'Чоерри', manager, visible=0)
chu = Button(W - 440, 1010, 180, 45, 'Чу', manager, visible=0)
LOONA_btn = [vivi, gowon, jinsoul, yojin, ives, kimlip, olivia, hasyl, heonjin, heejin, choerry, chu]

Mamamoo = Button(W - 250, 560, 240, 45, 'Mamamoo', manager)
moon = Button(W - 440, 560, 180, 45, 'Мунбёль', manager, visible=0)
solar = Button(W - 440, 610, 180, 45, 'Сола', manager, visible=0)
hwasa = Button(W - 440, 660, 180, 45, 'Хваса', manager, visible=0)
wheen = Button(W - 440, 710, 180, 45, 'Хвиин', manager, visible=0)
Mamamoo_btn = [moon, solar, hwasa, wheen]

Momoland = Button(W - 250, 610, 240, 45, 'Momoland', manager)
ahin = Button(W - 440, 610, 180, 45, 'Ахин', manager, visible=0)
jooe = Button(W - 440, 660, 180, 45, 'Джуи', manager, visible=0)
nancy = Button(W - 440, 710, 180, 45, 'Нэнси', manager, visible=0)
Momoland_btn = [ahin, jooe, nancy]

NMIXX = Button(W - 250, 660, 240, 45, 'NMIXX', manager)
bae = Button(W - 440, 660, 180, 45, 'Бае', manager, visible=0)
sollun = Button(W - 440, 710, 180, 45, 'Соллюн', manager, visible=0)
haewon = Button(W - 440, 760, 180, 45, 'Хэвон', manager, visible=0)
NMIXX_btn = [bae, sollun, haewon]

Oh_My_Girl = Button(W - 250, 710, 240, 45, 'Oh My Girl', manager)
arin = Button(W - 440, 710, 180, 45, 'Арин', manager, visible=0)
binnie = Button(W - 440, 760, 180, 45, 'Бинни', manager, visible=0)
jiho = Button(W - 440, 810, 180, 45, 'Джихо', manager, visible=0)
mimi = Button(W - 440, 860, 180, 45, 'Мими', manager, visible=0)
synghee = Button(W - 440, 910, 180, 45, 'Сынхи', manager, visible=0)
hyojeon = Button(W - 440, 960, 180, 45, 'Хёджон', manager, visible=0)
yua = Button(W - 440, 1010, 180, 45, 'Юа', manager, visible=0)
Oh_My_Girl_btn = [arin, binnie, jiho, mimi, synghee, hyojeon, yua]

Red_Velvet = Button(W - 250, 760, 240, 45, 'Red Velvet', manager)
irene = Button(W - 440, 760, 180, 45, 'Айрин', manager, visible=0)
wendy = Button(W - 440, 810, 180, 45, 'Вэнди', manager, visible=0)
joy = Button(W - 440, 860, 180, 45, 'Джой', manager, visible=0)
seulgi = Button(W - 440, 910, 180, 45, 'Сыльги', manager, visible=0)
Red_Velvet_btn = [irene, wendy, joy, seulgi]

Rocket_Punch = Button(W - 250, 810, 240, 45, 'Rocket Punch', manager)
juri = Button(W - 440, 810, 180, 45, 'Джури', manager, visible=0)
yeonhee = Button(W - 440, 860, 180, 45, 'Ёнхи', manager, visible=0)
suyun = Button(W - 440, 910, 180, 45, 'Суюн', manager, visible=0)
yunkyon = Button(W - 440, 960, 180, 45, 'Юнкён', manager, visible=0)
Rocket_Punch_btn = [juri, yeonhee, suyun, yunkyon]

TWICE = Button(W - 250, 860, 240, 45, 'TWICE', manager)
dahyeon = Button(W - 440, 710, 180, 45, 'Дахён', manager, visible=0)
jihyo = Button(W - 440, 760, 180, 45, 'Джихё', manager, visible=0)
mina = Button(W - 440, 810, 180, 45, 'Мина', manager, visible=0)
momo = Button(W - 440, 860, 180, 45, 'Момо', manager, visible=0)
nayeon = Button(W - 440, 910, 180, 45, 'Наён', manager, visible=0)
sana = Button(W - 440, 960, 180, 45, 'Сана', manager, visible=0)
tzu = Button(W - 440, 1010, 180, 45, 'Тзуи', manager, visible=0)
TWICE_btn = [dahyeon, jihyo, mina, momo, nayeon, sana, tzu]

VIVIZ = Button(W - 250, 910, 240, 45, 'VIVIZ', manager)
sinb = Button(W - 440, 860, 180, 45, 'Синби', manager, visible=0)
umji = Button(W - 440, 910, 180, 45, 'Умджи', manager, visible=0)
eunha = Button(W - 440, 960, 180, 45, 'Ынха', manager, visible=0)
sowon = Button(W - 440, 1010, 180, 45, 'Совон', manager, visible=0)
VIVIZ_btn = [sinb, umji, eunha, sowon]

WJSN = Button(W - 250, 960, 240, 45, 'WJSN', manager)
bona = Button(W - 440, 810, 180, 45, 'Бона', manager, visible=0)
dayeon_wj = Button(W - 440, 860, 180, 45, 'Даён', manager, visible=0)
yeorym = Button(W - 440, 910, 180, 45, 'Ерым', manager, visible=0)
seola = Button(W - 440, 960, 180, 45, 'Сольа', manager, visible=0)
chenxao = Button(W - 440, 1010, 180, 45, 'Чэнь Сяо', manager, visible=0)
WJSN_btn = [bona, dayeon_wj, yeorym, seola, chenxao]

Solo = Button(W - 250, 1010, 240, 45, 'SOLO', manager)
eyn = Button(W - 440, 460, 180, 45, 'Еын', manager, visible=0)
yena = Button(W - 440, 510, 180, 45, 'Йена', manager, visible=0)
chaeyon = Button(W - 440, 560, 180, 45, 'Ли Чеён', manager, visible=0)
nayn = Button(W - 440, 610, 180, 45, 'Наын', manager, visible=0)
somi = Button(W - 440, 660, 180, 45, 'Соми', manager, visible=0)
sunmi = Button(W - 440, 710, 180, 45, 'Сонми', manager, visible=0)
sohee = Button(W - 440, 760, 180, 45, 'Сохи', manager, visible=0)
eunbi = Button(W - 440, 810, 180, 45, 'Ынби', manager, visible=0)
choa = Button(W - 440, 860, 180, 45, 'Чоа', manager, visible=0)
chungha = Button(W - 440, 910, 180, 45, 'Чонха', manager, visible=0)
tsuki = Button(W - 440, 960, 180, 45, 'Цуки', manager, visible=0)
yuri = Button(W - 440, 1010, 180, 45, 'Юри', manager, visible=0)
Solo_btn = [eyn, yena, chaeyon, nayn, somi, sunmi, sohee, eunbi, choa, chungha, tsuki, yuri]

all_btn = Aespa_btn + Blackpink_btn + Dreamcatcher_btn + Everglow_btn + Fromis_9_btn + Gidle_btn + ITZY_btn + IVE_btn\
          + Kep1er_btn + LeSserafim_btn + LOONA_btn + Mamamoo_btn + Momoland_btn + NMIXX_btn + Oh_My_Girl_btn\
          + Red_Velvet_btn + Rocket_Punch_btn + TWICE_btn + VIVIZ_btn + WJSN_btn + Solo_btn

not_sort = Button(W - 700, 1010, 240, 45, 'Прочее', manager)
del_img = Button(W - 960, 1010, 240, 45, 'Удалить', manager)


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

            if event.type == pg.UI_BUTTON_ON_HOVERED:
                if event.ui_element == Aespa:
                    switch_btn_visible(Aespa_btn)
                if event.ui_element == Blackpink:
                    switch_btn_visible(Blackpink_btn)
                if event.ui_element == Dreamcatcher:
                    switch_btn_visible(Dreamcatcher_btn)
                if event.ui_element == Everglow:
                    switch_btn_visible(Everglow_btn)
                if event.ui_element == Fromis_9:
                    switch_btn_visible(Fromis_9_btn)
                if event.ui_element == Gidle:
                    switch_btn_visible(Gidle_btn)
                if event.ui_element == ITZY:
                    switch_btn_visible(ITZY_btn)
                if event.ui_element == IVE:
                    switch_btn_visible(IVE_btn)
                if event.ui_element == Kep1er:
                    switch_btn_visible(Kep1er_btn)
                if event.ui_element == LeSserafim:
                    switch_btn_visible(LeSserafim_btn)
                if event.ui_element == LOONA:
                    switch_btn_visible(LOONA_btn)
                if event.ui_element == Mamamoo:
                    switch_btn_visible(Mamamoo_btn)
                if event.ui_element == Momoland:
                    switch_btn_visible(Momoland_btn)
                if event.ui_element == NMIXX:
                    switch_btn_visible(NMIXX_btn)
                if event.ui_element == Oh_My_Girl:
                    switch_btn_visible(Oh_My_Girl_btn)
                if event.ui_element == Red_Velvet:
                    switch_btn_visible(Red_Velvet_btn)
                if event.ui_element == Rocket_Punch:
                    switch_btn_visible(Rocket_Punch_btn)
                if event.ui_element == TWICE:
                    switch_btn_visible(TWICE_btn)
                if event.ui_element == VIVIZ:
                    switch_btn_visible(VIVIZ_btn)
                if event.ui_element == WJSN:
                    switch_btn_visible(WJSN_btn)
                if event.ui_element == Solo:
                    switch_btn_visible(Solo_btn)
            if event.type == pg.UI_BUTTON_PRESSED:
                if event.ui_element == winter:
                    save_load('Винтер')
                if event.ui_element == giselle:
                    save_load('Жизель')
                if event.ui_element == karina:
                    save_load('Карина')
                if event.ui_element == ningning:
                    save_load('НинНин')

                if event.ui_element == jennie:
                    save_load('Дженни')
                if event.ui_element == jisoo:
                    save_load('Джису')
                if event.ui_element == lisa:
                    save_load('Лиса')
                if event.ui_element == rose:
                    save_load('Розэ')

                if event.ui_element == gah:
                    save_load('Гахён')
                if event.ui_element == dami:
                    save_load('Дами')
                if event.ui_element == jiu:
                    save_load('Джию')
                if event.ui_element == sua:
                    save_load('Суа')
                if event.ui_element == dongie:
                    save_load('Хандон')
                if event.ui_element == sieon:
                    save_load('Шиён')
                if event.ui_element == yooheon:
                    save_load('Юхён')

                if event.ui_element == aisha:
                    save_load('Айша')
                if event.ui_element == iron:
                    save_load('Ирон')
                if event.ui_element == mia:
                    save_load('Миа')
                if event.ui_element == onda:
                    save_load('Онда')
                if event.ui_element == siheon:
                    save_load('Шихён')
                if event.ui_element == eu:
                    save_load('EU')

                if event.ui_element == guri:
                    save_load('Гюри')
                if event.ui_element == jiwon:
                    save_load('Дживон')
                if event.ui_element == jisun:
                    save_load('Джисун')
                if event.ui_element == jiheon:
                    save_load('Джихён')
                if event.ui_element == nageon:
                    save_load('Нагён')
                if event.ui_element == saerom:
                    save_load('Сэром')
                if event.ui_element == haeon:
                    save_load('Хаён')

                if event.ui_element == mieon:
                    save_load('Миён')
                if event.ui_element == minni:
                    save_load('Минни')
                if event.ui_element == soeon:
                    save_load('Соён')
                if event.ui_element == sujin:
                    save_load('Суджин')
                if event.ui_element == shuhua:
                    save_load('Шухуа')
                if event.ui_element == uqi:
                    save_load('Юки')

                if event.ui_element == eji:
                    save_load('Еджи')
                if event.ui_element == lia:
                    save_load('Лиа')
                if event.ui_element == rujin:
                    save_load('Рюджин')
                if event.ui_element == chaeren:
                    save_load('Чeрён')
                if event.ui_element == yuna:
                    save_load('Юна')

                if event.ui_element == woneon:
                    save_load('Вонён')
                if event.ui_element == yujin:
                    save_load('Юджин')

                if event.ui_element == dayeon:
                    save_load('Даён')
                if event.ui_element == yenyn:
                    save_load('Енын')
                if event.ui_element == xaotin:
                    save_load('Сяотин')
                if event.ui_element == yujin_kp:
                    save_load('Юджин(k)')

                if event.ui_element == kazuha:
                    save_load('Казуха')
                if event.ui_element == sakura:
                    save_load('Сакура')
                if event.ui_element == chaewon:
                    save_load('Чевон')
                if event.ui_element == yunjin:
                    save_load('Юнджин')

                if event.ui_element == vivi:
                    save_load('Виви')
                if event.ui_element == gowon:
                    save_load('Говон')
                if event.ui_element == jinsoul:
                    save_load('Джинсоль')
                if event.ui_element == yojin:
                    save_load('Ёджин')
                if event.ui_element == ives:
                    save_load('Ив')
                if event.ui_element == kimlip:
                    save_load('Ким Лип')
                if event.ui_element == olivia:
                    save_load('Оливия Хе')
                if event.ui_element == hasyl:
                    save_load('Хасыль')
                if event.ui_element == heonjin:
                    save_load('Хёнджин')
                if event.ui_element == heejin:
                    save_load('Хиджин')
                if event.ui_element == choerry:
                    save_load('Чоерри')
                if event.ui_element == chu:
                    save_load('Чу')

                if event.ui_element == moon:
                    save_load('Мунбёль')
                if event.ui_element == solar:
                    save_load('Сола')
                if event.ui_element == hwasa:
                    save_load('Хваса')
                if event.ui_element == wheen:
                    save_load('Хвиин')

                if event.ui_element == ahin:
                    save_load('Ахин')
                if event.ui_element == jooe:
                    save_load('Джуи')
                if event.ui_element == nancy:
                    save_load('Нэнси')

                if event.ui_element == bae:
                    save_load('Бае')
                if event.ui_element == sollun:
                    save_load('Соллюн')
                if event.ui_element == haewon:
                    save_load('Хэвон')

                if event.ui_element == arin:
                    save_load('Арин')
                if event.ui_element == binnie:
                    save_load('Бинни')
                if event.ui_element == jiho:
                    save_load('Джихо')
                if event.ui_element == mimi:
                    save_load('Мими')
                if event.ui_element == synghee:
                    save_load('Сынхи')
                if event.ui_element == hyojeon:
                    save_load('Хёджон')
                if event.ui_element == yua:
                    save_load('Юа')

                if event.ui_element == irene:
                    save_load('Айрин')
                if event.ui_element == wendy:
                    save_load('Вэнди')
                if event.ui_element == joy:
                    save_load('Джой')
                if event.ui_element == seulgi:
                    save_load('Сыльги')

                if event.ui_element == juri:
                    save_load('Джури')
                if event.ui_element == yeonhee:
                    save_load('Ёнхи')
                if event.ui_element == suyun:
                    save_load('Суюн')
                if event.ui_element == yunkyon:
                    save_load('Юнкён')

                if event.ui_element == dahyeon:
                    save_load('Дахён')
                if event.ui_element == jihyo:
                    save_load('Джихё')
                if event.ui_element == mina:
                    save_load('Мина')
                if event.ui_element == momo:
                    save_load('Момо')
                if event.ui_element == nayeon:
                    save_load('Наён')
                if event.ui_element == sana:
                    save_load('Сана')
                if event.ui_element == tzu:
                    save_load('Тзуи')

                if event.ui_element == sinb:
                    save_load('Синби')
                if event.ui_element == umji:
                    save_load('Умджи')
                if event.ui_element == eunha:
                    save_load('Ынха')
                if event.ui_element == sowon:
                    save_load('Совон')

                if event.ui_element == bona:
                    save_load('Бона')
                if event.ui_element == dayeon_wj:
                    save_load('Даён(wj)')
                if event.ui_element == yeorym:
                    save_load('Ерым')
                if event.ui_element == seola:
                    save_load('Сольа')
                if event.ui_element == chenxao:
                    save_load('Чэнь Сяо')

                if event.ui_element == eyn:
                    save_load('Еын')
                if event.ui_element == yena:
                    save_load('Йена')
                if event.ui_element == chaeyon:
                    save_load('Ли Чеён')
                if event.ui_element == nayn:
                    save_load('Наын')
                if event.ui_element == somi:
                    save_load('Соми')
                if event.ui_element == sunmi:
                    save_load('Сонми')
                if event.ui_element == sohee:
                    save_load('Сохи')
                if event.ui_element == eunbi:
                    save_load('Ынби')
                if event.ui_element == choa:
                    save_load('Чоа')
                if event.ui_element == chungha:
                    save_load('Чонха')
                if event.ui_element == tsuki:
                    save_load('Цуки')
                if event.ui_element == yuri:
                    save_load('Юри')

                if event.ui_element == not_sort:
                    save_load('[Прочее]')
                if event.ui_element == del_img:
                    remove(img_path)
                    image_load()

            manager.process_events(event)

        display.blit(img_opened, (W // 2 - img_opened.get_rect().centerx, H // 2 - img_opened.get_rect().centery))
        print_text(f'{open_folder}', 10, H - 40, f_color='red')
        if open_folder != "<No File Selected>":
            print_text(f'{len(listdir(open_folder))}', 10, H - 80, f_color='red')
        manager.update(time_delta)
        manager.draw_ui(display)
        pygame.display.update()
        clock.tick(fps)


if __name__ == '__main__':
    start()

pygame.quit()
sys.exit()
