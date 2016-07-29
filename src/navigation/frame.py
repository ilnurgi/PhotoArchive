# coding: utf-8

"""
панель навигации
"""

from Tkinter import Button

from core.frame import BasePAFrame


class NavigationFrame(BasePAFrame):

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.buttons = []

    def _pa_configure(self):
        BasePAFrame._pa_configure(self)

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        relx = 0

        # ширина кнопки навигации
        relwidth = 0.13

        for button in self.buttons:
            button.place(relx=relx, rely=0, relwidth=relwidth, relheight=1)
            relx += relwidth

    def add_button(self, text, command):
        """
        добавляем кнопку в панель навигации

        :param unicode text: текст кнопки
        :param command: ссылка на обработчик
        """
        self.buttons.append(Button(self, text=text, command=command))
        return self.buttons[-1]
