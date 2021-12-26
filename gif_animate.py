import pygame


class GIFAnimate:

    def __init__(self, x, y):
        # позиции картинки на экране
        self.x, self.y = x, y
        # список всех гифок в программе
        self.gifs_paths = [
            ["gifs/gif_1/0.png", "gifs/gif_1/1.png", "gifs/gif_1/2.png", "gifs/gif_1/3.png"],
            ["gifs/gif_2/0.png", "gifs/gif_2/1.png", "gifs/gif_2/2.png", "gifs/gif_2/3.png"],
            ["gifs/gif_3/0.png", "gifs/gif_3/1.png", "gifs/gif_3/2.png", "gifs/gif_3/3.png", "gifs/gif_3/4.png", "gifs/gif_3/5.png"],
            ["gifs/gif_4/0.png", "gifs/gif_4/1.png", "gifs/gif_4/2.png", "gifs/gif_4/3.png"],
        ]
        # список загруженых картинок
        self.gifs = []
        # текущий индекс гифки
        self.current_gif = 0
        # индекс картинки в текущей гифке
        self.current_index = 0
        # заргужаем все картинки сразу в мапять
        self.pre_load_images()

    def pre_load_images(self):
        # предзагрузка всех изображений
        for gif_paths in self.gifs_paths:
            loaded_images = []
            for path in gif_paths:
                loaded_images.append(pygame.image.load(path))
            self.gifs.append(loaded_images)


    def show_next_image(self, display, fps, current_step):
        # display - экран для отрисовки
        # fps - сколько кадров в секунду поддерживает приложение
        # current_step - какой кадр сейчас проигрывается
        # менять картинку необходимо каждый fps//len(self.gifs[self.current_gif]) шаг
        step = fps//len(self.gifs[self.current_gif])
        # проверяем, если сейчас кадр (fps+current_step)%step == 0, то меняем картинку
        if (fps+current_step)%step == 0:
            self.current_index += 1
        # если индекс новой картинки выходит за количество картинок, то
        # новый индекс картинки равен 0
        if self.current_index >= len(self.gifs[self.current_gif]):
            self.current_index = 0
        # отрисовываем на экране картинку
        display.blit(self.gifs[self.current_gif][self.current_index], (self.x, self.y))

    def change_gif(self, index):
        # если крутим колесиком мыши, то надо делать сдвиг по картинке
        # назад или вперед, для этого просто сохраняем индекс текущей гифки
        self.current_gif += index
        if self.current_gif >= len(self.gifs):
            self.current_gif = 0
        elif self.current_gif < 0:
            self.current_gif = len(self.gifs) - 1
