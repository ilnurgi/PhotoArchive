# coding: utf-8

import hashlib
import os
from threading import Thread

from Tkinter import Button, Listbox, END, Text, Label
from tkFileDialog import askdirectory

from PIL import ImageTk, Image

from core.frame import BasePAFrame
from settings.model import settings


class FindFilesFrame(BasePAFrame):
    """
    фрейм для поиска новых фотографии
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_button_select_base_path = Button(
            self, text=u'Поиск', command=self.click_button_find)
        self.w_button_move = Button(
            self, text=u'Переместить', command=self.click_button_move)

        self.w_listbox_files = Listbox(self)
        self.w_text_debugger = Text(self)
        self.w_image_frame = ImageFrame(self)

        self.last_move_path = settings.BASE_CATALOG

    def _pa_configure(self):
        self.w_listbox_files.bind(
            '<<ListboxSelect>>', self.select_listbox_files)

    def _pa_layout(self):
        w_button_relwidth = 0.15
        w_button_relheight = 0.2

        self.w_button_select_base_path.place(
            relx=0,
            rely=0,
            relheight=w_button_relheight,
            relwidth=w_button_relwidth,
        )
        self.w_button_move.place(
            relx=w_button_relwidth,
            rely=0,
            relheight=w_button_relheight,
            relwidth=w_button_relwidth,
        )
        self.w_text_debugger.place(
            relx=w_button_relwidth*2,
            rely=0,
            relwidth=1-w_button_relwidth*2,
            relheight=w_button_relheight,
        )
        self.w_listbox_files.place(
            relx=0,
            rely=w_button_relheight,
            relheight=1-w_button_relheight,
            relwidth=0.5
        )
        self.w_image_frame.place(
            relx=0.5,
            rely=w_button_relheight,
            relheight=1 - w_button_relheight,
            relwidth=0.5
        )

    def select_listbox_files(self, event):
        self.w_image_frame.reset()

        try:
            index = self.w_listbox_files.curselection()[0]
            image_path = self.listbox_items[index]
        except IndexError:
            return
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
            except IOError:
                image = None
            self.w_image_frame.set_image(
                image,
                self.w_image_frame.winfo_width(),
                self.w_image_frame.winfo_height())

    def click_button_move(self):
        """
        обработчик кнопки переноса
        """
        try:
            index = self.w_listbox_files.curselection()[0]
            image_path = self.listbox_items[index]
        except IndexError:
            return

        if os.path.exists(image_path):
            path = askdirectory(
                title=u'Выберите папку для перемещения',
                initialdir=self.last_move_path)
            if not path:
                return

            self.last_move_path = path

            dst = os.path.join(path, os.path.basename(image_path))
            os.rename(image_path, dst)

    def click_button_find(self):
        """
        обработчик кнопки старта поиска фотграфии
        """
        self.w_listbox_files.delete(0, END)
        self.w_text_debugger.delete(1.0, END)
        self.w_image_frame.reset()

        thread = Thread(target=self._find_new_fils)
        thread.start()

    def _find_new_fils(self):
        """
        ищем новые файлы, лучше запускать в отдельном потоке
        """
        new_files, new_dubl_files = self._get_new_files(
            settings.PHOTO_FINDER_LAST_SIR, settings.BASE_CATALOG)

        self.listbox_items = [
            u'Совершенно новые файлы',
            u''
        ]
        self.listbox_items.extend(new_files)
        self.listbox_items.extend((
            u"",
            u"",
            u"Вроде дубликаты",
            u""
        ))
        [(self.listbox_items.extend(item['src_files']),
          self.listbox_items.extend(item['dst_files']),
          self.listbox_items.append(u''))
         for item in new_dubl_files]
        self.w_listbox_files.insert(END, *self.listbox_items)

    def _get_new_files(self, src, dst, use_hash=False):
        """
        функция возвращает список новых файлов, найденных в указанной папке
        src - папка, где смотрим новые файлы
        dst - папка, где эти файлы должны появиться потом, т.е. архивная
        новым считается файл:
            если такого размера файла у нас нет совсем
            если размер совпадает, но не совпадает название и хеш
        если размер и название совпадают то файлы считаются одинаковыми
        """

        self.w_text_debugger.insert(END, u"Ищем новые фотографии\n")
        # собираем данные по файлам которые у нас уже есть
        dst_map = {}
        for root, dirs, files in os.walk(dst):
            for f in files:
                path = os.path.join(root, f)
                dst_map.setdefault(os.stat(path).st_size, []).append(path)

        self.w_text_debugger.insert(
            END,
            u"Количесвто файлов нашего архива: {}\n".format(
                sum(len(i) for i in dst_map.itervalues())))

        # собираем данные по файлам которых у нас нет
        src_map = {}
        for root, dirs, files in os.walk(src):
            for f in files:
                path = os.path.join(root, f)
                src_map.setdefault(os.stat(path).st_size, []).append(path)

        self.w_text_debugger.insert(
            END,
            u"Количесвто файлов стороннего архива: {}\n".format(
                sum(len(i) for i in src_map.itervalues())))

        # новые файлы по размеру
        new_files = []

        # новые файлы,
        # которые совпали по размеру и имени но не совпали по хешу
        new_dubl_files = []

        for size, photos in src_map.iteritems():
            if size not in dst_map:
                # у нас нету файла с таким размером, значит он новый
                new_files.extend(photos)
            else:
                dst_photos = dst_map[size]
                # у нас есть файлы такого размера
                # сравним их названия
                dst_names = [os.path.basename(p) for p in dst_photos]
                for photo in photos:
                    photo_name = os.path.basename(photo)

                    if photo_name not in dst_names or use_hash:
                        # названия файлов не совпадают, сравниваем хеши
                        # или принудительно сравниваем хеши
                        hashs = []
                        for dst_photo in dst_photos:
                            with open(dst_photo, "rb") as f:
                                hasher = hashlib.md5()
                                hasher.update(f.read())
                                hashs.append(hasher.hexdigest())
                        for src_photo in photos:
                            with open(src_photo, "rb") as f:
                                hasher = hashlib.md5()
                                hasher.update(f.read())
                                if hasher.hexdigest() not in hashs:
                                    new_dubl_files.append({
                                        "src_files": photos,
                                        "dst_files": photos,
                                    })

        self.w_text_debugger.insert(
            END,
            u"Найдено совсем новых файлов: {}\n".format(len(new_files)))

        self.w_text_debugger.insert(
            END,
            u"Найдено новых файлов: {}\n".format(len(new_dubl_files)))

        return new_files, new_dubl_files


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
