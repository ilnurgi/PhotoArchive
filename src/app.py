# coding: utf-8

"""
приложение
"""

from Tkinter import Tk, BOTH, TOP

import yaml

import settings

from helpers import parsegeometry
from navigation.frame import NavigationFrame
from photo.frame import PhotoFrame
from people.frame import PeopleFrame
from settings import default_settings


class App(object):
    """
    приложение
    """

    def __init__(self):
        """
        инициализация приложения
        """
        self.w_window = Tk()

        # фрейм навигации
        self.w_frame_toolbar = NavigationFrame(self.w_window)

        # фрейм с фотографиями
        self.w_frame_photo = PhotoFrame(self.w_window)

        # фрейм с людьми
        self.w_frame_people = PeopleFrame(self.w_window)

        # список фреймов, вкладок
        self.frames = (
            self.w_frame_photo,
            self.w_frame_people)

    def start(self):
        """
        стартуем приложение
        """
        self._pa_configure()
        self._pa_layout()
        self.w_window.mainloop()

    def _pa_configure(self):
        """
        настройка приложения
        """
        self.w_window.protocol('WM_DELETE_WINDOW', self.save_settings)
        self.w_window.minsize(
            width=settings.MAIN_WINDOW_MIN_WIDTH,
            height=settings.MAIN_WINDOW_MIN_HEIGHT)
        self.w_window.geometry(
            u'{0}x{1}+{2}+{3}'.format(
                settings.MAIN_WINDOW_WIDTH,
                settings.MAIN_WINDOW_HEIGHT,
                settings.MAIN_WINDOW_X,
                settings.MAIN_WINDOW_Y))

        self.w_frame_toolbar.add_button(
            text=u'Фотографии', command=self.click_photo_button)
        # self.w_frame_toolbar.add_button(
        #     text=u'Люди', command=self.click_people_button)

        # задаем размеры и положение фреймов
        # фрейм тулбара
        self.w_frame_toolbar_rel_x = 0
        self.w_frame_toolbar_rel_y = 0
        self.w_frame_toolbar_rel_width = 1
        self.w_frame_toolbar_rel_height = 0.06
        # фрейм инструментов - фотографии, люди и т.б.
        self.w_frame_tools_rel_x = 0
        self.w_frame_tools_rel_y = self.w_frame_toolbar_rel_height
        self.w_frame_tools_rel_width = 1
        self.w_frame_tools_rel_height = 1 - self.w_frame_tools_rel_y

    def _pa_layout(self):
        """
        отображаем приложение
        """
        self.w_frame_toolbar.place(
            relx=self.w_frame_toolbar_rel_x,
            rely=self.w_frame_toolbar_rel_y,
            relwidth=self.w_frame_toolbar_rel_width,
            relheight=self.w_frame_toolbar_rel_height)
        self.click_photo_button()

    def save_settings(self):
        """
        сохраняем какие то настройки
        """

        save_settings = {}
        for frame in self.frames:
            save_settings.update(frame.get_save_settings())

        width, height, x, y = parsegeometry(self.w_window.geometry())

        for attr, dattr in (
                (width, 'MAIN_WINDOW_WIDTH'),
                (height, 'MAIN_WINDOW_HEIGHT'),
                (x, 'MAIN_WINDOW_X'),
                (y, 'MAIN_WINDOW_Y'),
            ):
            if attr != getattr(default_settings, dattr):
                save_settings[dattr] = attr

        with open(settings.config_path, 'w') as stream:
            yaml.dump(save_settings, stream, default_flow_style=False, indent=4)

        self.w_window.destroy()

    def click_photo_button(self):
        """
        обработчик отображения вкладки фотографии
        """
        for frame in self.frames:
            frame.pack_forget()
        self.w_frame_photo.place(
            relx=self.w_frame_tools_rel_x,
            rely=self.w_frame_tools_rel_y,
            relwidth=self.w_frame_tools_rel_width,
            relheight=self.w_frame_tools_rel_height)

    def click_people_button(self):
        """
        обработчик отображения вкладки людей
        """
        for frame in self.frames:
            frame.pack_forget()
        self.w_frame_people.pack(fill=BOTH)


App().start()
