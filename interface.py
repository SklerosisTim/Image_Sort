import pygame
import pygame_gui
import tkinter
import tkinter.filedialog

pygame.init()
W, H = 1920, 1080
display = pygame.display.set_mode((W, H))


class Button(pygame_gui.elements.UIButton):  # кнопки
    def __init__(self, pos: tuple, text, manager_, tooltip=None, object_id=None, visible=1):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect(pos), text=text, manager=manager_,
                                              tool_tip_text=tooltip, object_id=object_id, visible=visible)
        self.group = []


class Text:
    def __init__(self, f_size: int, rect=None, shadow: any = 'gray', f_color: str = 'black',
                 position: str = 'center', font='font/Alice-Regular.ttf'):
        self.f_size = f_size
        self.rect = rect
        self.shadow = shadow
        self.f_color = f_color
        self.position = position
        self.font = font

    def write(self, pos: tuple, txt: str):
        text_rect = pygame.Rect(pos)
        font_type = pygame.font.Font(self.font, self.f_size)
        text_surf = font_type.render(txt, True, self.f_color)
        if self.rect:
            pygame.draw.rect(display, self.rect, pos, border_radius=10)
        pos_y = text_rect.centery - text_surf.get_rect().centery
        if self.position == 'center':
            pos_x = text_rect.centerx - text_surf.get_rect().centerx
        elif self.position == 'left':
            pos_x = text_rect.x + 5
        else:  # self.position == 'right'
            pos_x = text_rect.x + text_rect.width - text_surf.get_rect().width - 5
        if self.shadow:
            shadow_offset = 1 + (self.f_size // 20)
            shadow_surf = font_type.render(txt, True, self.shadow)
            display.blit(shadow_surf, (pos_x + shadow_offset, pos_y + shadow_offset))
        display.blit(text_surf, (pos_x, pos_y))


class ProgressBar:
    def __init__(self, b_size, f_size=0, bg=None, max_bar=1000, color1='blue', color2='red',
                 border=2, radius=5, shadow='gray'):
        self.b_size = b_size
        self.f_size = f_size
        self.f_color = 'black'
        self.color1 = color1
        self.color2 = color2
        self.max = max_bar
        self.background = bg
        self.border = border
        self.radius = radius
        self.shadow = shadow
        self.font = 'font/Morice-Bejar.ttf'

    def draw(self, pos, txt: str, bar):
        text = Text(self.f_size, shadow=self.shadow, f_color=self.f_color, font=self.font)
        rect_bg = pygame.Rect(pos, self.b_size)
        if self.background:
            pygame.draw.rect(display, self.background, rect_bg, border_radius=self.radius)
        if bar >= 0:
            bar = self.max if bar > self.max else bar
            rect_progress = (pos[0], pos[1], bar / self.max * self.b_size[0], self.b_size[1])
            pygame.draw.rect(display, self.color1, rect_bg, self.border, self.radius)
            pygame.draw.rect(display, self.color1, rect_progress, border_radius=self.radius)
        else:  # bar < 0
            bar = -abs(self.max) if bar < -abs(self.max) else bar
            rect_minus = (pos[0] + self.b_size[0] + bar / self.max * self.b_size[0], pos[1],
                          abs(bar / self.max * self.b_size[0]), self.b_size[1])
            pygame.draw.rect(display, self.color2, rect_bg, self.border, self.radius)
            pygame.draw.rect(display, self.color2, rect_minus, border_radius=self.radius)
        if self.f_size:
            text.write((pos, self.b_size), txt)


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


manager = pygame_gui.UIManager((W, H), 'json/main.json')
txt_brown = Text(30, f_color='brown', position='left')
txt_file_info = Text(35, font='font/Morice-Bejar.ttf', shadow='orange')
txt_message = Text(35, shadow='orange', position='left')
del_bt = Button((1300, 1030, 160, 45), '[Удалить]', manager)
other_bt = Button((1130, 1030, 160, 45), '[Прочее]', manager)
load_bt = Button((550, 930, 800, 60), 'Загрузить изображение', manager)
input_bt = Button((10, 1000, 100, 35), '---', manager)
output_bt = Button((10, 1040, 100, 35), '---', manager)
stat_bt = Button((10, 10, 200, 45), 'Статистика', manager)
f_bt = Button((220, 10, 50, 45), 'F', manager)
z_bt = Button((280, 10, 50, 45), 'Z', manager)
x_bt = Button((340, 10, 50, 45), 'X', manager)
