# coding: utf-8

"""
панель с настройками
"""

from tkinter import Label, Button
from tkinter.filedialog import askdirectory

from core.frame import BasePAFrame
from settings.model import settings


class SettingsFrame(BasePAFrame):
    """
    панель с настройками
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_base_path_frame = BasePathFrame(self)
        self.w_about_frame = AboutFrame(self)

    def _pa_layout(self):
        w_base_path_height = 0.15
        self.w_base_path_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=w_base_path_height)
        self.w_about_frame.place(
            relx=0,
            rely=w_base_path_height,
            relwidth=1,
            relheight=1-w_base_path_height)


class BasePathFrame(BasePAFrame):
    """
    фрейм для указания папки с фотографиями
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_label_base_path_label = Label(self, text=u'Папка с фотографиями')
        self.w_label_base_path = Label(self, text=settings.BASE_CATALOG)

        self.w_button_select_base_path = Button(
            self, text=u'Изменить', command=self.click_button_select_base_path)

    def _pa_layout(self):
        label_height = 0.25
        self.w_label_base_path_label.place(
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
        :return:
        """

        path = askdirectory(
            title=u'Выберите папку с фотографиями',
            initialdir=settings.BASE_CATALOG)
        if not path:
            return

        self.w_label_base_path['text'] = path
        settings.BASE_CATALOG = path


class AboutFrame(BasePAFrame):

    about = u"""
    О программе.

    Версия: {}

    Программа для работы с фотографиями.

    Автор: Ильнур Гайфутдинов

    Интернет страница автора: ilnurgi1.ru

    Обратная связь: ilnurgi@mail.ru, ilnurgi87@gmail.com

    Skype: ilnurgi_work
    """.format(settings.VERSION_STR)

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_label_base_path_label = Label(self, text=self.about)

    def _pa_layout(self):
        self.w_label_base_path_label.place(
            relx=0,
            rely=0
        )
