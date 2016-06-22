# coding: utf-8

"""
панель, в которой отображаются картинка и вся остальная информация
"""

from collections import OrderedDict
import datetime
import os

from Tkinter import Label, Button, Entry
from tkMessageBox import showerror

from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

from core.frame import BasePAFrame
from settings import DATE_TIME_FORMAT, DATE_TIME_FORMAT_EXIF

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
    TEXT_DATE_CREATE,
    TEXT_DATE_MODIFY,
    TEXT_DATE_ACCESS,
    TEXT_EXIF_DATE_ORIGINAL,
    TEXT_EXIF_DATE_DIGITIZED,
    TEXT_EXIF_DATE_TIME,
)

LABELS_RENAME = {
    TEXT_DATE_CREATE,
    TEXT_DATE_MODIFY,
    TEXT_DATE_ACCESS,
    TEXT_EXIF_DATE_ORIGINAL,
    TEXT_EXIF_DATE_DIGITIZED,
    TEXT_EXIF_DATE_TIME,
}


class ImageFrame(BasePAFrame):
    """
    фрейм с картинкой
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.image_label = Label(self)

    def _pa_layout(self):
        self.image_label.pack()

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
        self.image_label.config(image=photo_image)
        self.image_label.image = photo_image

    def reset(self):
        self.image_label.config(image=None)
        self.image_label.image = None


class SettingsFrame(BasePAFrame):
    """
    фрейм с параметрами
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.widgets = OrderedDict(
            (label,
             {
                 'label': Label(self, text=label),
                 'label_data': Label(self)
             })
            for label in LABELS)

        _entry_data = Entry(self)
        _btn_rename = Button(self, text=u'Переименовать')
        _btn_rename.bind('<Button-1>', self.click_rename_button)
        _btn_rename.meta = {
            'entry_widget': _entry_data
        }
        self.widgets[TEXT_MY_NAME] = {
            'label': Label(self, text=TEXT_MY_NAME),
            'label_data': _entry_data,
            'button_rename': _btn_rename
        }

        for label, label_widgets in self.widgets.iteritems():
            if label in LABELS_RENAME:
                label_widgets['button_rename'] = Button(
                    self,
                    text=u'Переименовать')
                label_widgets['button_rename'].meta = {}
                label_widgets['button_rename'].bind(
                    '<Button-1>', self.click_rename_button)

    def _pa_layout(self):
        BasePAFrame._pa_layout(self)

        for index, labels in enumerate(self.widgets.values()):
            labels['label'].grid(row=index, column=0)
            labels['label_data'].grid(row=index, column=1)
            if 'button_rename' in labels:
                labels['button_rename'].grid(row=index, column=2)

    def set_file(self, file_path, image):
        stat = os.stat(file_path)

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

        bind_maps = (
            (TEXT_FILE_PATH, file_path),
            (TEXT_DATE_CREATE, date_create.strftime(DATE_TIME_FORMAT)),
            (TEXT_DATE_MODIFY, date_modify.strftime(DATE_TIME_FORMAT)),
            (TEXT_DATE_ACCESS, date_access.strftime(DATE_TIME_FORMAT)),
            (TEXT_SIZE, u'{1} МБ / {0} Б'.format(
                stat.st_size, round(stat.st_size/1024.0/1024, 2))),
            (TEXT_IMAGE_SIZE,
             u'{0} / {1}'.format(*(image.size if image else (0, 0)))),
            (TEXT_EXIF_DATE_ORIGINAL,
             exif_data[EXIF_TAGS_REVERSE['DateTimeOriginal']]),
            (TEXT_EXIF_DATE_DIGITIZED,
             exif_data[EXIF_TAGS_REVERSE['DateTimeDigitized']]),
            (TEXT_EXIF_DATE_TIME,
             exif_data[EXIF_TAGS_REVERSE['DateTime']]),
        )

        for text, data in bind_maps:
            self.widgets[text]['label_data'].config(text=data)
            if text in LABELS_RENAME:
                self.widgets[text]['button_rename'].meta['file_path'] = file_path
                self.widgets[text]['button_rename'].meta['data'] = data
                self.widgets[text]['button_rename'].meta['size'] = stat.st_size

        self.widgets[TEXT_MY_NAME]['button_rename'].meta['file_path'] = file_path
        self.widgets[TEXT_MY_NAME]['button_rename'].meta['data'] = TEXT_MY_NAME
        self.widgets[TEXT_MY_NAME]['button_rename'].meta['size'] = stat.st_size

    def reset(self):
        for labels in self.widgets.values():
            labels['label_data'].config(text=u'')
            if 'button_rename' in labels:
                _entry_widget = labels['button_rename'].meta.get(
                    'entry_widget', None)

                labels['button_rename'].meta = {}

                if _entry_widget:
                    labels['button_rename'].meta['entry_widget'] = _entry_widget

    def click_rename_button(self, event):
        meta = event.widget.meta
        if not meta:
            return

        if 'entry_widget' in meta:
            data = meta['entry_widget'].get()
        else:
            try:
                date = datetime.datetime.strptime(
                    meta['data'], DATE_TIME_FORMAT)
            except ValueError:
                try:
                    date = datetime.datetime.strptime(
                        meta['data'], DATE_TIME_FORMAT_EXIF)
                except ValueError:
                    return

            data = date.strftime(u'%Y%m%d_%H%M%S')
        new_file_name = (
            u'{0}_{1}{2}'.format(
                data,
                meta['size'],
                os.path.splitext(meta['file_path'])[-1]))
        new_file_dir = os.path.dirname(meta['file_path'])
        new_file_path = os.path.join(new_file_dir, new_file_name)
        if os.path.exists(new_file_path):
            showerror(
                u'Ошибка',
                u'Файл ({0}) уже существует, переименовать невозможно'.format(
                    new_file_path))
        else:
            os.rename(meta['file_path'], new_file_path)
            self.master.handle_update_files(new_file_dir, new_file_name)


class RightFrame(BasePAFrame):
    """
    правый фрейм
    """

    catalog = None

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_image_frame = ImageFrame(self)
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
        self.w_image_frame.place(
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
            try:
                image = Image.open(fl['path'])
            except IOError:
                image = None
            self.w_image_frame.set_image(
                image,
                self.w_image_frame.winfo_width(),
                self.w_image_frame.winfo_height())
            self.w_settings_frame.set_file(fl['path'], image)
        else:
            self.reset()

    def reset(self):
        self.w_image_frame.reset()
        self.w_settings_frame.reset()

    def handle_update_files(self, new_file_dir, new_file_name):
        """
        обновляем список файлов
        :param str new_file_dir: новый путь к папке с файлами
        """
        self.master.handle_update_files(new_file_dir, new_file_name)
