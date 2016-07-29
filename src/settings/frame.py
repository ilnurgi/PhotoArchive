# coding: utf-8

"""
панель с настройками
"""

from Tkinter import Label, Button

from tkFileDialog import askdirectory

from core.frame import BasePAFrame
from settings.model import settings


class SettingsFrame(BasePAFrame):
    """
    панель с настройками
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_label_base_path_label = Label(self, text=u'Папка с фотографиями')
        self.w_label_base_path = Label(self, text=settings.BASE_CATALOG)

        self.w_button_select_base_path = Button(
            self, text=u'Изменить', command=self.click_button_select_base_path)

    def _pa_layout(self):
        self.w_label_base_path_label.pack()
        self.w_label_base_path.pack()
        self.w_button_select_base_path.pack()

    def click_button_select_base_path(self):
        """
        обработчик выбора папки с фотографиями
        :return:
        """

        path = askdirectory(
            title=u'Выберите папку с фотографиями',
            initialdir=settings.BASE_CATALOG)
        if not path:
            return

        self.w_label_base_path['text'] = path
        settings.BASE_CATALOG = path
