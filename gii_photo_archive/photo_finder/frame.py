# coding: utf-8

from core.frame import BasePAFrame

from .frame_source_path import SourcePathFrame
from .frame_find_files import FindFilesFrame


class PhotoFinderFrame(BasePAFrame):
    """
    поиск новых фотографии
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_base_path_frame = SourcePathFrame(self)
        self.w_base_finder_frame = FindFilesFrame(self)

    def _pa_layout(self):
        w_base_path_height = 0.15
        self.w_base_path_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=w_base_path_height)
        self.w_base_finder_frame.place(
            relx=0,
            rely=w_base_path_height,
            relwidth=1,
            relheight=1-w_base_path_height)


