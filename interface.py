import pygame
from pygame_gui import elements

pygame.init()
W, H = 1920, 1080
display = pygame.display.set_mode((W, H))


class Button(elements.UIButton):  # кнопки
    def __init__(self, pos: tuple, text, manager, tooltip=None, object_id=None, visible=1):
        elements.UIButton.__init__(self, relative_rect=pygame.Rect(pos), text=text, manager=manager,
                                   tool_tip_text=tooltip, object_id=object_id, visible=visible)


class DDMenu(elements.UIDropDownMenu):  # выпадающее меню
    def __init__(self, pos: tuple, options_list, starting_option, manager, object_id=None):
        elements.UIDropDownMenu.__init__(self, relative_rect=pygame.Rect(pos), object_id=object_id,
                                         options_list=options_list, starting_option=starting_option, manager=manager)


class HSlider(elements.UIHorizontalSlider):  # горизонтальные слайдеры
    def __init__(self, pos: tuple, value_range, start_value, manager):
        elements.UIHorizontalSlider.__init__(self, relative_rect=pygame.Rect(pos),
                                             value_range=value_range, start_value=start_value, manager=manager)


class TextLine(elements.UITextEntryLine):  # текстовые поля для ввода с клавиатуры
    def __init__(self, pos: tuple, manager, visible=0):
        elements.UITextEntryLine.__init__(self, relative_rect=pygame.Rect(pos),
                                          manager=manager, visible=visible)


class InfoPanel:  # вывод журнала
    def __init__(self, font_size=25, font_='comicsans'):
        self.font_size = font_size
        self.font = font_

    def draw(self, text):
        y = 1080
        offset = 1 + self.font_size // 20
        ip_font = pygame.font.SysFont(self.font, self.font_size)
        for line in text:
            ln = len(text)
            t = str(line)
            ip_surf = ip_font.render(t, True, 'orange')  # создание поверхности с записью
            shadow_surf = ip_font.render(t, True, 'black')  # поверхность с тенью
            display.blit(shadow_surf, (1920 - ip_surf.get_rect().width - 5 + offset,
                                       y - (self.font_size + 5) * ln + offset))  # отрисовка тени
            display.blit(ip_surf, (1920 - ip_surf.get_rect().width - 5, y - (self.font_size + 5) * ln))  # текста
            y += self.font_size + 5  # прибавка к высоте для след записи


class Text:
    def __init__(self, f_size: int, rect=None, shadow: any = 'gray', f_color: str = 'black', position: str = 'center'):
        self.f_size = f_size
        self.rect = rect
        self.shadow = shadow
        self.f_color = f_color
        self.position = position
        self.font = 'font/Morice-Bejar.ttf'

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
        text = Text(self.f_size, shadow=self.shadow, f_color=self.f_color)
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


class RecruitGirlSprite(pygame.sprite.Sprite):  # для виджетов рекрутов (wid_recruit_spr)
    def __init__(self, image, group, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(group)


class DragAndDropIcon(pygame.sprite.Sprite):  # Drag&Drop спрайты иконок на главном экране
    def __init__(self, image, x_pos, y_pos, idol):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.idol = idol
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.clicked = False
        self.already_pressed = False
        self.font_color = self.idol.hp_color()
        self.work_mark = self.idol.work
        self.date_mark = '*' * self.idol.date['timeout']

    def update(self):
        name = Text(24, shadow=None, f_color=self.font_color, position='left')
        work = Text(20, shadow=None, f_color=self.font_color, position='left')
        date = Text(36, shadow=None, f_color=self.font_color, position='left')
        bar = ProgressBar((100, 10), max_bar=self.idol.max_hp(), color1=self.idol.hp_color(), radius=2)
        name.write((self.rect.x, self.rect.y - 34, 100, 24), self.idol.name)
        work.write((self.rect.x, self.rect.y, 100, 20), self.work_mark)
        date.write((self.rect.x + 90 - (self.idol.date['timeout'] * 10), self.rect.y + 80, 100, 36), self.date_mark)
        bar.draw((self.rect.x, self.rect.y - 10), '', self.idol.hp)
        pos = pygame.mouse.get_pos()
        if self.clicked:
            self.rect.x = pos[0] - (self.rect.width / 2)
            self.rect.y = pos[1] - (self.rect.height / 2)

    def action(self, action=None):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed(num_buttons=3)[2]:
                if not self.already_pressed:
                    if action is not None:
                        action()
                        self.already_pressed = True
                    else:
                        return True
            else:
                self.already_pressed = False
