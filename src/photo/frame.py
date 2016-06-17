# coding: utf-8

"""
панель каталогов
"""

from core.frame import BasePAFrame
from photo.leftframe import LeftFrame
from photo.center_frame import CenterFrame
from photo.rightframe import RightFrame


class PhotoFrame(BasePAFrame):

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        # правый фрейм, где отображается фото и его параметры
        self.w_right_frame = RightFrame(self)

        # центральный фрейм, в котором отображается список файлов
        self.w_center_frame = CenterFrame(self, child_frame=self.w_right_frame)

        # левый фрейм, в котором отображается список каталогов
        self.w_left_frame = LeftFrame(self, child_frame=self.w_center_frame)

    def _pa_configure(self):
        """
        настройка фрейма работы
        :return:
        """
        BasePAFrame._pa_configure(self)

        # задаем размеры и положение фреймов
        self.w_left_frame_rel_x = 0
        self.w_left_frame_rel_y = 0
        self.w_left_frame_rel_width = 0.1
        self.w_left_frame_rel_height = 1

        self.w_center_frame_rel_x = self.w_left_frame_rel_width
        self.w_center_frame_rel_y = 0
        self.w_center_frame_rel_width = 0.1
        self.w_center_frame_rel_height = 1

        self.w_right_frame_rel_x = (
            self.w_left_frame_rel_width + self.w_center_frame_rel_width)
        self.w_right_frame_rel_y = 0
        self.w_right_frame_rel_width = 1 - self.w_right_frame_rel_x
        self.w_right_frame_rel_height = 1

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        self.w_left_frame.place(
            relx=self.w_left_frame_rel_x,
            rely=self.w_left_frame_rel_y,
            relwidth=self.w_left_frame_rel_width,
            relheight=self.w_left_frame_rel_height)

        self.w_center_frame.place(
            relx=self.w_center_frame_rel_x,
            rely=self.w_center_frame_rel_y,
            relwidth=self.w_center_frame_rel_width,
            relheight=self.w_center_frame_rel_height)

        self.w_right_frame.place(
            relx=self.w_right_frame_rel_x,
            rely=self.w_right_frame_rel_y,
            relwidth=self.w_right_frame_rel_width,
            relheight=self.w_right_frame_rel_height)

    def get_save_settings(self):
        save_settings = BasePAFrame.get_save_settings(self)
        save_settings.update(self.w_left_frame.get_save_settings())
        return save_settings

    def handle_update_files(self, new_catalog_path, new_file_name):
        """
        обновить список файлов файлов
        """
        self.w_center_frame.set_catalog(
            {
                'path': new_catalog_path,
                'file_name': new_file_name
            })

