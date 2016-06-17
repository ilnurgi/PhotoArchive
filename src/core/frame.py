# coding: utf-8

"""
базовые фрейм для приложения
"""

from Tkinter import Frame, SOLID


class BasePAFrame(Frame):

    def pack(self, *args, **kwargs):
        """
        перед отрисовкой мы конфигугрируем фрейм и его виджеты
        потом отрисовываем фрейм и виджеты
        """
        Frame.pack(self, *args, **kwargs)

        self._pa_configure()
        self._pa_layout()

    def place(self, *args, **kwargs):
        """
        перед отрисовкой мы конфигугрируем фрейм и его виджеты
        потом отрисовываем фрейм и виджеты
        """
        Frame.place(self, *args, **kwargs)

        self._pa_configure()
        self._pa_layout()

    def grid(self, *args, **kwargs):
        """
        перед отрисовкой мы конфигугрируем фрейм и его виджеты
        потом отрисовываем фрейм и виджеты
        """
        Frame.grid(self, *args, **kwargs)

        self._pa_configure()
        self._pa_layout()

    def _pa_configure(self):
        """
        конфигурируем фрейм и его виджеты
        """
        self.config(borderwidth=3)
        self.config(relief=SOLID)

    def _pa_layout(self):
        """
        отображаем виджеты фрейма
        """

    def get_save_settings(self):
        """
        возвращаем настройки для сохранения
        """
        return {}
