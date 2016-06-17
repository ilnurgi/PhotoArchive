# coding: utf-8

from Tkinter import Listbox, RIGHT

from core.frame import BasePAFrame


class PeopleFrame(BasePAFrame):

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_listbox_photos = Listbox(self)

    def _pa_configure(self):
        BasePAFrame._pa_configure(self)

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        self.w_listbox_photos.pack(side=RIGHT)
