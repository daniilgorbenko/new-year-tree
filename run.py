import pygame
from screeninfo import get_monitors
import os
import win32api
import win32con
import win32gui

from gif_animate import GIFAnimate

# получаем информацию о мониторах
monitors = get_monitors()
# получаем данные о разрешении
screen_width = monitors[0].width
screen_height = monitors[0].height

# создаем класс работы с анимациями и указываем начальную позицию анимации
gif_anim = GIFAnimate(100, 100)


# -> создаем окно PyGame
pygame.init()
# сразу укажем, что окно должно открываться в левом верхнем углу экрана
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
# размер окна - максимальный по нашим параметрам,
# pygame.NOFRAME - означает, что окно должно открываться без рамок
screen = pygame.display.set_mode([screen_width, screen_height], pygame.NOFRAME)
# Clock нужен быть для того, чтобы ограничить fps программы
# ограничение fps необходимо для того, чтобы сделать анимацию картинок более простой
Clock = pygame.time.Clock()
running = True

# -> делаем прозрачный фон
# для этого определим цвет, который будет меняться на прозрачный
fuchsia = (255, 0, 128)
# получаем окно pygame
hwnd = pygame.display.get_wm_info()["window"]
# указываем параметры, какой цвет в программе должен меняться на прозрачный
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
# -> убираем с панели задач иконку программы
# для этого возьмем текущее окно, которое получили в hwnd = pygame.display.get_wm_info()["window"]
# указываем параметры для того, чтобы скрыть иконки
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)| win32con.WS_EX_TOOLWINDOW)

# количество fps
FPS = 30
# текущий фрейм
current_frame = 0
# начальная позиция мышки
start_mouse_pos = [500, 500]
# была ли зажата мышка
mouse_pressed = False
# -> Главный цикл программы
print("START")
while running:
    # считаем индекс текущего фрейма
    if current_frame > FPS: current_frame = 0
    current_frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # обработка ивента с перетягиванием картинки
        # если нажали ЛКМ на картинке, то считаем, что начали перетягивать картинку
        # и при этом запоминаем текущую позицию мышки
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            start_mouse_pos = pygame.mouse.get_pos()
        # если отпустили ЛКМ, то считаем, что перетягивание закончилось
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False
        # правая кнопка мыши - выход из приложения
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            running = False
        # колесико мыши - меняем анимацию
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 4:
            gif_anim.change_gif(1)
        # колесико в обратную сторону
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 5:
            gif_anim.change_gif(-1)
        # если мышка зажата, то смотрим разницу между предыдущей позицией мышки и текущей
        if mouse_pressed:
            current_pos = pygame.mouse.get_pos()
            delta_x, delta_y = start_mouse_pos[0] - current_pos[0], start_mouse_pos[1] - current_pos[1]
            start_mouse_pos = current_pos
            # передвигаем картинку на разницу между позициями мышки
            gif_anim.x -= delta_x
            gif_anim.y -= delta_y
    # закрасили окно бесцветным
    screen.fill(fuchsia)
    # нарисовали следующий кадр
    gif_anim.show_next_image(screen, FPS, current_frame)
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    pygame.display.update()
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%i,%i" % (screen_width - width + i, screen_height - height + i)
    Clock.tick(FPS)

pygame.quit()