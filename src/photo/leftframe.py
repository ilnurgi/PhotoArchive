# coding: utf-8

"""
панель каталогов
"""

import os

from Tkinter import Listbox, BOTH, Button, TOP, X, END, E, W, S, N
from tkFileDialog import askdirectory

import settings

from core.frame import BasePAFrame


class LeftFrame(BasePAFrame):
    """
    левый фрейм,
    в котором у нас находятся кнопка добавить каталог и список каталогов
    """

    def __init__(self, *args, **kwargs):
        self.w_frame_child = kwargs.pop('child_frame')

        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_button_add_catalog = Button(
            self, text=u'Добавить', command=self.click_button_add_catalog)
        self.w_button_del_catalog = Button(
            self, text=u'Удалить', command=self.click_button_del_catalog)
        self.w_listbox_catalogs = Listbox(self) 

        self.catalogs = []
        self.update_catalogs(settings.CATALOGS)

    def _pa_configure(self):
        BasePAFrame._pa_configure(self)

        self.w_listbox_catalogs.bind(
            '<<ListboxSelect>>', self.select_listbox_catalogs)

        # задаем размеры и положение фреймов
        self.w_button_add_catalog_rel_x = 0
        self.w_button_add_catalog_rel_y = 0
        self.w_button_add_catalog_rel_width = 1
        self.w_button_add_catalog_rel_height = 0.05

        self.w_button_del_catalog_rel_x = 0
        self.w_button_del_catalog_rel_y = self.w_button_add_catalog_rel_height
        self.w_button_del_catalog_rel_width = 1
        self.w_button_del_catalog_rel_height = (
            self.w_button_add_catalog_rel_height)

        self.w_listbox_catalogs_rel_x = 0
        self.w_listbox_catalogs_rel_y = (
            self.w_button_add_catalog_rel_height +
            self.w_button_del_catalog_rel_height)
        self.w_listbox_catalogs_rel_width = 1
        self.w_listbox_catalogs_rel_height = 1 - self.w_listbox_catalogs_rel_y

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        self.w_button_add_catalog.place(
            relx=self.w_button_add_catalog_rel_x,
            rely=self.w_button_add_catalog_rel_y,
            relwidth=self.w_button_add_catalog_rel_width,
            relheight=self.w_button_add_catalog_rel_height)

        self.w_button_del_catalog.place(
            relx=self.w_button_del_catalog_rel_x,
            rely=self.w_button_del_catalog_rel_y,
            relwidth=self.w_button_del_catalog_rel_width,
            relheight=self.w_button_del_catalog_rel_height)

        self.w_listbox_catalogs.place(
            relx=self.w_listbox_catalogs_rel_x,
            rely=self.w_listbox_catalogs_rel_y,
            relwidth=self.w_listbox_catalogs_rel_width,
            relheight=self.w_listbox_catalogs_rel_height)

    def get_save_settings(self):
        save_settings = BasePAFrame.get_save_settings(self)
        save_settings['LAST_CATALOG_DIR'] = settings.LAST_CATALOG_DIR
        save_settings['CATALOGS'] = self.catalogs
        return save_settings

    def update_catalogs(self, catalogs):
        exist_catalog_paths = set(catalog['path'] for catalog in self.catalogs)
        for new_catalog in catalogs:
            if new_catalog['path'] not in exist_catalog_paths:
                self.catalogs.append(new_catalog)
        self.catalogs.sort(key=lambda x: x['name'])
        self.w_listbox_catalogs.delete(0, END)
        self.w_listbox_catalogs.insert(
            END, *(catalog['name'] for catalog in self.catalogs))

    def click_button_add_catalog(self):
        """
        обработчик добавления каталога фотографии
        :return:
        """
        path = askdirectory(
            title=u'Выберите папку с фотографиями', 
            initialdir=settings.LAST_CATALOG_DIR)
        if not path:
            return
            
        settings.LAST_CATALOG_DIR = path

        # TODO: необъодимо выводить прогрессбар, т.к. процесс может быть долгим
        new_catalogs = []
        new_catalogs_append = new_catalogs.append
        catalog_paths = set()
        for root, dirs, files in os.walk(path):
            if root not in catalog_paths:
                new_catalogs_append({
                    'name': os.path.basename(root),
                    'path': root
                })
                catalog_paths.add(root)

            for _dir in dirs:
                path = os.path.join(root, _dir)
                if path in catalog_paths:
                    new_catalogs_append({
                        'name': _dir,
                        'path': os.path.join(root, _dir)
                    })
                    catalog_paths.add(path)
        self.update_catalogs(new_catalogs)

    def click_button_del_catalog(self):
        """
        обработчик удаления каталога из списка каталогов
        """
        try:
            index = self.w_listbox_catalogs.curselection()[0]
            self.w_listbox_catalogs.delete(index)
            del self.catalogs[index]
        except IndexError:
            return
        else:
            self.w_frame_child.set_catalog(None)

    def select_listbox_catalogs(self, event):
        """
        обработчик выбора каталога в списке каталогов

        :param event:
        :return:
        """
        try:
            index = self.w_listbox_catalogs.curselection()[0]
            catalog = self.catalogs[index]
        except IndexError:
            return
        else:
            self.w_frame_child.set_catalog(catalog)
