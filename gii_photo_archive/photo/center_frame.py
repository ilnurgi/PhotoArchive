# coding: utf-8

"""
панель списка файлов
"""

import os

from tkinter import Listbox, BOTH, TOP, END, Scrollbar, RIGHT, LEFT, Y

from core.frame import BasePAFrame


class CenterFrame(BasePAFrame):
    """
    фрейм со списком файлов
    """

    def __init__(self, *args, **kwargs):
        self.w_frame_child = kwargs.pop('child_frame')

        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_listbox_files = Listbox(self)
        self.w_scrollbar_files = Scrollbar(self)

        self.catalog = None
        self.catalog_files = []

    def _pa_configure(self):
        BasePAFrame._pa_configure(self)

        self.w_listbox_files.config(yscrollcommand=self.w_scrollbar_files.set)
        self.w_scrollbar_files.config(command=self.w_listbox_files.yview)

        self.w_listbox_files.bind(
            '<<ListboxSelect>>', self.select_listbox_file)

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        w_listbox_files_width = 0.95
        self.w_listbox_files.place(
            relx=0,
            rely=0,
            relwidth=w_listbox_files_width,
            relheight=1)
        self.w_scrollbar_files.place(
            relx=w_listbox_files_width,
            rely=0,
            relwidth=1-w_listbox_files_width,
            relheight=1)

    def set_catalog(self, catalog=None):
        """
        задаем новый каталог для отображения

        :param catalog: словарь
            {
                'path': путь к каталогу
            }
        :return:
        """

        try:
            current_index = self.w_listbox_files.curselection()[0]
        except IndexError:
            current_index = 0

        if 0 < current_index < len(self.catalog_files):
            set_index = current_index + 1
        else:
            set_index = current_index

        self.catalog = catalog
        self.catalog_files = []
        self.w_listbox_files.delete(0, END)
        self.w_frame_child.set_file(None)

        if self.catalog is not None:
            catalog_path = self.catalog

            for file_name in os.listdir(catalog_path):
                file_path = os.path.join(catalog_path, file_name)
                if os.path.isfile(file_path):
                    self.catalog_files.append({
                        'name': file_name,
                        'path': file_path})
            self.catalog_files.sort(key=lambda x: x['name'])
            catalog_files = [catalog['name'] for catalog in self.catalog_files]
            self.w_listbox_files.insert(END, *catalog_files)

            self.w_listbox_files.selection_set(set_index)
            self.w_listbox_files.see(set_index)
            self.w_listbox_files.event_generate("<<ListboxSelect>>")

    def update_catalog(self):
        self.set_catalog(self.catalog)

    def select_listbox_file(self, event):
        """
        обработчик выбора файла в списке файлов

        :param event:
        :return:
        """
        try:
            index = self.w_listbox_files.curselection()[0]
            file_ = self.catalog_files[index]
        except IndexError:
            return
        else:
            self.w_frame_child.set_file(file_)
