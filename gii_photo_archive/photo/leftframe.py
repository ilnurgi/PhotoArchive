# coding: utf-8

"""
панель каталогов
"""

import os

from tkinter import Listbox, END

from settings.model import settings

from core.frame import BasePAFrame

PREFIX_LEN = 2
BACK_DIR_PATH = u'...'


class LeftFrame(BasePAFrame):
    """
    левый фрейм,
    в котором у нас находится список папок
    """

    def __init__(self, *args, **kwargs):
        self.w_frame_child = kwargs.pop('child_frame')

        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_listbox_catalogs = Listbox(self)

        self.current_catalog = settings.BASE_CATALOG
        self.catalogs = []

        # текущий активный каталог, необходим для дабл клика,
        # т.к. переходит фокус
        self.current_catalog_clicked = None

    def _pa_configure(self):
        BasePAFrame._pa_configure(self)

        self.w_listbox_catalogs.bind(
            '<<ListboxSelect>>', self.select_listbox_catalog)

        self.w_listbox_catalogs.bind(
            '<Double-Button-1>', self.select_listbox_catalogs)

        # задаем размеры и положение фреймов
        self.w_listbox_catalogs_rel_x = 0
        self.w_listbox_catalogs_rel_y = 0
        self.w_listbox_catalogs_rel_width = 1
        self.w_listbox_catalogs_rel_height = 1 - self.w_listbox_catalogs_rel_y

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        self.w_listbox_catalogs.place(
            relx=self.w_listbox_catalogs_rel_x,
            rely=self.w_listbox_catalogs_rel_y,
            relwidth=self.w_listbox_catalogs_rel_width,
            relheight=self.w_listbox_catalogs_rel_height)

    def set_catalog(self, catalog=None):
        """
        задаем новый корневой каталог
        :param catalog:
        :return:
        """

        catalog = catalog or self.current_catalog

        if not os.path.isdir(catalog):
            return

        # if isinstance(catalog, str):
            # catalog = catalog.decode('utf-8')

        self.current_catalog = catalog

        if catalog != settings.BASE_CATALOG:
            catalogs = [
                u'{0}{1}'.format(
                    BACK_DIR_PATH,
                    self.current_catalog.replace(settings.BASE_CATALOG, ''))]
        else:
            catalogs = []

        for _catalog in os.listdir(catalog):
            _path = os.path.join(catalog, _catalog)
            if (os.path.isdir(_path) and
                    u'system volume information' not in _path.lower()):
                if any(
                        i for i in os.listdir(_path)
                        if os.path.isdir(os.path.join(_path, i))):
                    prefix = u'+ {0}'
                else:
                    prefix = u'- {0}'
                catalogs.append(prefix.format(_catalog))

        catalogs.sort(key=lambda x: x[PREFIX_LEN:])

        if catalog == settings.BASE_CATALOG or len(catalogs) > 1:
            self.catalogs = catalogs
            self.w_listbox_catalogs.delete(0, END)
            self.w_listbox_catalogs.insert(
                END, *self.catalogs)

    def select_listbox_catalogs(self, event):
        """
        обработчик выбора каталога в списке каталогов, для проваливания внутрь

        :param event:
        :return:
        """
        if self.current_catalog_clicked == self.current_catalog:
            self.set_catalog(os.path.dirname(self.current_catalog))
        else:
            self.set_catalog(
                os.path.join(self.current_catalog_clicked))

    def select_listbox_catalog(self, event):
        """
        обработчик выбора каталога в списке каталогов, для просмотра картинок

        :param event:
        :return:
        """
        try:
            index = self.w_listbox_catalogs.curselection()[0]
            catalog = self.catalogs[index]
        except IndexError:
            return
        else:
            if catalog.startswith(BACK_DIR_PATH):
                self.w_frame_child.set_catalog(self.current_catalog)
                self.current_catalog_clicked = self.current_catalog
            else:
                path = os.path.join(self.current_catalog, catalog[PREFIX_LEN:])
                self.w_frame_child.set_catalog(path)
                self.current_catalog_clicked = path
