# coding: utf-8

from Tkinter import Label, Button

from tkFileDialog import askdirectory

from core.frame import BasePAFrame
from settings.model import settings


class SourcePathFrame(BasePAFrame):
    """
    фрейм для выбора источника
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_label_source_path_label = Label(
            self, text=u'Папка источник с фотографиями ')
        self.w_label_base_path = Label(
            self, text=settings.PHOTO_FINDER_LAST_DIR)

        self.w_button_select_base_path = Button(
            self, text=u'Изменить', command=self.click_button_select_base_path)

    def _pa_layout(self):
        label_height = 0.25
        self.w_label_source_path_label.place(
            relx=0,
            rely=0
        )
        self.w_label_base_path.place(
            relx=0,
            rely=label_height
        )
        self.w_button_select_base_path.place(
            relx=0,
            rely=label_height * 2
        )

    def click_button_select_base_path(self):
        """
        обработчик выбора папки с фотографиями
        """

        path = askdirectory(
            title=u'Выберите папку с фотографиями',
            initialdir=settings.PHOTO_FINDER_LAST_SIR)
        if not path:
            return

        self.w_label_base_path['text'] = path
        settings.PHOTO_FINDER_LAST_SIR = path
