# coding: utf-8

"""
панель, в которой отображаются картинка и вся остальная информация
"""

from collections import OrderedDict
import datetime
import os
import platform

from Tkinter import Label, Button, Entry, END
from tkFileDialog import askdirectory
from tkMessageBox import showerror, askyesno

import vlc

from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

from core.frame import BasePAFrame
from settings.model import settings

AVAILABLE_VIDEO_FRMTS = ('.avi', '.mp4', '.AVI')

date_format = u'%Y-%m-%d %H-%M-%S'

EXIF_TAGS = TAGS
EXIF_TAGS_REVERSE = {v: k for k, v in TAGS.iteritems()}

TEXT_FILE_PATH = u'Путь к файлу'

TEXT_DATE_CREATE = u'Дата создания'
TEXT_DATE_MODIFY = u'Дата изменения'
TEXT_DATE_ACCESS = u'Дата доступа'

TEXT_SIZE = u'Размер файла'
TEXT_IMAGE_SIZE = u'Разрешение файла'

TEXT_EXIF_DATE_ORIGINAL = u'Дата фотографии'
TEXT_EXIF_DATE_DIGITIZED = u'Дата фотографии2'
TEXT_EXIF_DATE_TIME = u'Дата фотографии3'

TEXT_MY_NAME = u'Моё имя'

LABELS = (
    TEXT_FILE_PATH,
    TEXT_SIZE,
    TEXT_IMAGE_SIZE,
)

LABELS_RENAME = (
    TEXT_DATE_CREATE,
    TEXT_DATE_MODIFY,
    TEXT_DATE_ACCESS,
    TEXT_EXIF_DATE_ORIGINAL,
    TEXT_EXIF_DATE_DIGITIZED,
    TEXT_EXIF_DATE_TIME,
)


class ViewMediaFrame(BasePAFrame):
    """
    фрейм с картинкой
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()

        self.platform = platform.system().lower()

        self.media_label = Label(self)

    def _pa_layout(self):
        self.media_label.pack()

    def set_image(self, image, width, height):
        if not image:
            self.reset()
            return

        image_width, image_height = image.size
        if image_height > height:
            percent = height/float(image_height)
            width = int(image_width * percent)
        elif image_width > width:
            percent = width / float(image_width)
            height = int(image_height * percent)
        photo_image = ImageTk.PhotoImage(
            image.resize((width, height), Image.ANTIALIAS))
        self.media_label.config(image=photo_image)
        self.media_label.image = photo_image

    def set_video(self, video_path):
        """
        проигрывает указанное видео
        """
        self.vlc_player.set_media(
            self.vlc_instance.media_new(video_path))
        if self.platform == 'windows':
            self.vlc_player.set_hwnd(self.media_label.winfo_id())
        else:
            self.vlc_player.set_xwindow(self.media_label.winfo_id())
        self.vlc_player.play()

    def reset(self):
        self.media_label.config(image=None)
        self.media_label.image = None


class SettingsFrame(BasePAFrame):
    """
    фрейм с параметрами
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.current_file = {}
        self.last_move_path = settings.BASE_CATALOG

        self.widgets = OrderedDict(
            (label,
             {
                 'label': Label(self, text=label),
                 'label_data': Label(self)
             })
            for label in LABELS)

        # виджеты для преименований
        self.widgets_with_rename = OrderedDict(
            (label,
             {
                 'label': Label(self, text=label),
                 'label_data': Label(self)
             })
            for label in LABELS_RENAME)

        # переименование с моим именем
        self.w_entry_custom_name = Entry(self)
        self.w_btn_rename_custom_name = Button(self, text=u'Переименовать')
        self.w_btn_rename_custom_name.bind(
            '<Button-1>', self.click_rename_button)

        self.widgets_with_rename[TEXT_MY_NAME] = {
            'label': Label(self, text=TEXT_MY_NAME),
            'label_data': self.w_entry_custom_name,
            'button_rename': self.w_btn_rename_custom_name,
        }

        # доп кнопки, переместить удалить
        _btn_mv = Button(self, text=u'Переместить')
        _btn_mv.bind('<Button-1>', self.click_move_button)

        _btn_rm = Button(self, text=u'Удалить')
        _btn_rm.bind('<Button-1>', self.click_remove_button)

        self.buttons = (
            (_btn_mv, _btn_rm),
        )

        # прописываем кнопки переместить
        for label, label_widgets in self.widgets_with_rename.iteritems():
            if label in LABELS_RENAME:
                _btn = Button(self, text=u'Переименовать')
                _btn.bind('<Button-1>', self.click_rename_button)
                _btn.meta = {}
                label_widgets['button_rename'] = _btn

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        for index, labels in enumerate(self.widgets.values()):
            labels['label'].grid(row=index, column=0)
            labels['label_data'].grid(row=index, column=1)

        for index, labels in enumerate(
                self.widgets_with_rename.values(), index+1):
            labels['label'].grid(row=index, column=0)
            labels['label_data'].grid(row=index, column=1)
            labels['button_rename'].grid(row=index, column=2)

        for row, btns in enumerate(self.buttons, index+1):
            for col, btn in enumerate(btns):
                btn.grid(row=row, column=col)

    def set_file(self, file_path, image):
        stat = os.stat(file_path)

        self.current_file['file_path'] = file_path
        self.current_file['size'] = stat.st_size

        date_create = datetime.datetime.fromtimestamp(stat.st_ctime)
        date_modify = datetime.datetime.fromtimestamp(stat.st_mtime)
        date_access = datetime.datetime.fromtimestamp(stat.st_atime)

        try:
            exif_data = image._getexif()
        except AttributeError:
            exif_data = None

        if not exif_data:
            exif_data = {
                EXIF_TAGS_REVERSE['DateTimeOriginal']: u'n/d',
                EXIF_TAGS_REVERSE['DateTimeDigitized']: u'n/d',
                EXIF_TAGS_REVERSE['DateTime']: u'n/d',
            }

        self.widgets[TEXT_FILE_PATH]['label_data']['text'] = (
            self.current_file['file_path'])
        self.widgets[TEXT_IMAGE_SIZE]['label_data']['text'] = (
            u'{0} / {1}'.format(*(image.size if image else (0, 0))))
        self.widgets[TEXT_SIZE]['label_data']['text'] = (
            u'{1} МБ / {0} Б'.format(
                self.current_file['size'],
                round(stat.st_size / 1024.0 / 1024, 2))
        )

        bind_maps = (
            (TEXT_DATE_CREATE, date_create.strftime(settings.DATE_TIME_FORMAT)),
            (TEXT_DATE_MODIFY, date_modify.strftime(settings.DATE_TIME_FORMAT)),
            (TEXT_DATE_ACCESS, date_access.strftime(settings.DATE_TIME_FORMAT)),
            (TEXT_EXIF_DATE_ORIGINAL,
             exif_data.get(EXIF_TAGS_REVERSE['DateTimeOriginal'], u'n/a')),
            (TEXT_EXIF_DATE_DIGITIZED,
             exif_data.get(EXIF_TAGS_REVERSE['DateTimeDigitized'], u'n/a')),
            (TEXT_EXIF_DATE_TIME,
             exif_data.get(EXIF_TAGS_REVERSE['DateTime'], u'n/a')),
        )

        for text, data in bind_maps:
            self.widgets_with_rename[text]['label_data'].config(text=data)
            self.widgets_with_rename[text]['button_rename'].meta['data'] = data

    def reset(self):
        self.current_file = {}

    def click_rename_button(self, event):
        if not self.current_file:
            return

        if event.widget == self.w_btn_rename_custom_name:
            data = self.w_entry_custom_name.get()
            self.w_entry_custom_name.delete(0, END)
        else:
            meta = event.widget.meta
            if not meta:
                return

            try:
                date = datetime.datetime.strptime(
                    meta['data'], settings.DATE_TIME_FORMAT)
            except ValueError:
                try:
                    date = datetime.datetime.strptime(
                        meta['data'], settings.DATE_TIME_FORMAT_EXIF)
                except ValueError:
                    return

            data = date.strftime(date_format)
        new_file_name = (
            u'{0} {1}{2}'.format(
                data,
                self.current_file['size'],
                os.path.splitext(self.current_file['file_path'])[-1]))
        new_file_dir = os.path.dirname(self.current_file['file_path'])
        new_file_path = os.path.join(new_file_dir, new_file_name)
        if new_file_path != self.current_file['file_path']:
            if os.path.exists(new_file_path):
                showerror(
                    u'Ошибка',
                    u'Файл ({0}) уже существует, '
                    u'переименовать невозможно'.format(new_file_path))
            else:
                os.rename(self.current_file['file_path'], new_file_path)
                self.master.handle_update_files()

    def click_move_button(self, event):
        """
        переместить файл
        :param event:
        :return:
        """
        if self.current_file:
            path = askdirectory(
                title=u'Выберите папку для перемещения',
                initialdir=self.last_move_path)
            if not path:
                return

            self.last_move_path = path

            src = self.current_file['file_path']
            file_name = os.path.basename(src)
            dst = os.path.join(path, file_name)
            os.rename(src, dst)

            self.master.reset()
            self.master.handle_update_files()

    def click_remove_button(self, event):
        # error, info, question, or warning
        if askyesno(
                u'Удалить файл?',
                self.current_file['file_path'],
                icon='warning'):
            os.remove(self.current_file['file_path'])
            self.master.reset()
            self.master.handle_update_files()


class RightFrame(BasePAFrame):
    """
    правый фрейм
    """

    catalog = None

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_view_frame = ViewMediaFrame(self)
        self.w_settings_frame = SettingsFrame(self)

        self.w_image_frame_rel_x = 0
        self.w_image_frame_rel_y = 0
        self.w_image_frame_rel_width = 1
        self.w_image_frame_rel_height = 0.5

        self.w_settings_frame_rel_x = 0
        self.w_settings_frame_rel_y = 1 - self.w_image_frame_rel_height
        self.w_settings_frame_rel_width = 1
        self.w_settings_frame_rel_height = 1 - self.w_settings_frame_rel_y

    def _pa_layout(self):
        self.w_view_frame.place(
            relx=self.w_image_frame_rel_x,
            rely=self.w_image_frame_rel_y,
            relwidth=self.w_image_frame_rel_width,
            relheight=self.w_image_frame_rel_height)
        self.w_settings_frame.place(
            relx=self.w_settings_frame_rel_x,
            rely=self.w_settings_frame_rel_y,
            relwidth=self.w_settings_frame_rel_width,
            relheight=self.w_settings_frame_rel_height)

    def set_file(self, fl):
        """
        устанавливает параметры по указаннмоу файлу
        :param fl:
        :return:
        """
        if fl:
            image = video = None
            try:
                image = Image.open(fl['path'])
            except IOError:
                if any(fl['path'].endswith(i) for i in AVAILABLE_VIDEO_FRMTS):
                    video = fl['path']

            if video:
                self.w_view_frame.set_video(video)
            else:
                self.w_view_frame.set_image(
                    image,
                    self.w_view_frame.winfo_width(),
                    self.w_view_frame.winfo_height())
            self.w_settings_frame.set_file(fl['path'], image)
        else:
            self.reset()

    def reset(self):
        self.w_view_frame.reset()
        self.w_settings_frame.reset()

    def handle_update_files(self):
        self.reset()
        self.master.handle_update_files()
