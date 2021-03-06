# coding: utf-8

import hashlib
import os
from threading import Thread

import tkinter
from tkinter.filedialog import askdirectory

from PIL import ImageTk, Image

from core.frame import BasePAFrame
from settings.model import settings


class FindFilesFrame(BasePAFrame):
    """
    фрейм для поиска новых фотографии
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.w_button_find_start = tkinter.Button(
            self, text=u'Поиск', command=self.click_button_find)
        self.w_button_move = tkinter.Button(
            self, text=u'Переместить', command=self.click_button_move)

        self.w_listbox_files = tkinter.Listbox(
            self, selectmode=tkinter.EXTENDED)
        self.w_listbox_scroll = tkinter.Scrollbar(self)

        self.w_text_debugger = tkinter.Text(self)
        self.w_text_debugger_scroll = tkinter.Scrollbar(self)

        self.w_image_frame = ImageFrame(self)

        self.w_checkbutton_only_size_variable = tkinter.BooleanVar()
        self.w_checkbutton_only_size = tkinter.Checkbutton(
            self,
            text=u'Только по размеру',
            variable=self.w_checkbutton_only_size_variable)

        self.last_move_path = settings.BASE_CATALOG

    def _pa_configure(self):
        self.w_listbox_files.bind(
            '<<ListboxSelect>>', self.select_listbox_files)

        self.w_listbox_files.insert(
            tkinter.END, *settings.PHOTO_FINDER_LAST_NEW_FILES)
        self.w_listbox_files.insert(
            tkinter.END, *settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS)

        self.w_listbox_scroll.config(command=self.w_listbox_files.yview)
        self.w_listbox_files.config(yscrollcommand=self.w_listbox_scroll.set)

        self.w_text_debugger_scroll.config(command=self.w_text_debugger.yview)
        self.w_text_debugger.config(
            yscrollcommand=self.w_text_debugger_scroll.set)

    def _pa_layout(self):
        w_button_relwidth = 0.15
        w_button_relheight = 0.1
        w_check_relx = w_button_relwidth
        w_check_relwidth = 0.2
        w_check_relheight = 0.1
        w_text_debugger_scroll_width = 0.01
        w_text_debugger_x = w_button_relwidth + w_check_relwidth
        w_text_debugger_width = (
            1 - w_button_relwidth - w_text_debugger_scroll_width -
            w_check_relwidth)
        w_text_debugger_scroll_x = (
            w_button_relwidth + w_text_debugger_width + w_check_relwidth)
        w_text_debugger_height = w_button_relheight * 2
        w_listbox_files_height = 1 - w_text_debugger_height
        w_listbox_files_width = 0.49

        self.w_button_find_start.place(
            relx=0,
            rely=0,
            relheight=w_button_relheight,
            relwidth=w_button_relwidth,
        )
        self.w_button_move.place(
            relx=0,
            rely=w_button_relheight,
            relheight=w_button_relheight,
            relwidth=w_button_relwidth,
        )
        self.w_checkbutton_only_size.place(
            relx=w_check_relx,
            rely=0,
            relwidth=w_check_relwidth,
            relheight=w_check_relheight,
        )
        self.w_text_debugger.place(
            relx=w_text_debugger_x,
            rely=0,
            relwidth=w_text_debugger_width,
            relheight=w_text_debugger_height,
        )
        self.w_text_debugger_scroll.place(
            relx=w_text_debugger_scroll_x,
            rely=0,
            relwidth=w_text_debugger_scroll_width,
            relheight=w_text_debugger_height,
        )
        self.w_listbox_files.place(
            relx=0,
            rely=w_text_debugger_height,
            relheight=w_listbox_files_height,
            relwidth=w_listbox_files_width
        )
        self.w_listbox_scroll.place(
            relx=w_listbox_files_width,
            rely=w_text_debugger_height,
            relheight=w_listbox_files_height,
            relwidth=0.01
        )
        self.w_image_frame.place(
            relx=0.5,
            rely=w_text_debugger_height,
            relheight=w_listbox_files_height,
            relwidth=0.5
        )

    def select_listbox_files(self, event):
        self.w_image_frame.reset()

        try:
            image_path = self.w_listbox_files.selection_get()
        except (IndexError, tkinter.TclError):
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
            image_paths = self.w_listbox_files.selection_get()
        except (IndexError, tkinter.TclError):
            return
        if image_paths:        
            path = askdirectory(
                title=u'Выберите папку для перемещения',
                initialdir=self.last_move_path)
            if not path:
                return

            self.last_move_path = path

            for image_path in image_paths.splitlines():
                if os.path.exists(image_path):
                    dst = os.path.join(path, os.path.basename(image_path))
                    while os.path.exists(dst):
                        p, e = dst.rsplit(".", 1)
                        dst = dst.replcae(u"."+e, u"1."+e)
                    try:
                        os.rename(image_path, dst)
                    except IOError:
                        print('ERROR: ({}) ->({})'.format(image_path, dst))
                        break

    def click_button_find(self):
        """
        обработчик кнопки старта поиска фотграфии
        """
        self.w_listbox_files.delete(0, tkinter.END)
        self.w_text_debugger.delete(1.0, tkinter.END)
        self.w_image_frame.reset()

        thread = Thread(target=self._find_new_fils)
        thread.start()

    def _find_new_fils(self):
        """
        ищем новые файлы, лучше запускать в отдельном потоке
        """
        new_files, new_dubl_files = self._get_new_files(
            settings.PHOTO_FINDER_LAST_SIR, settings.BASE_CATALOG)

        settings.PHOTO_FINDER_LAST_NEW_FILES = [
            u'Совершенно новые файлы',
            u''
        ]
        settings.PHOTO_FINDER_LAST_NEW_FILES.extend(new_files)

        settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS = [
            u"",
            u"",
            u"Вроде дубликаты",
            u""
        ]
        [(            
            settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS.extend(
                item['dst_files']),
            settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS.extend(
                item['src_files']),
            settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS.append(u''))
            for item in new_dubl_files]
        
        self.w_listbox_files.insert(
            tkinter.END, *settings.PHOTO_FINDER_LAST_NEW_FILES)
        self.w_listbox_files.insert(
            tkinter.END, *settings.PHOTO_FINDER_LAST_NEW_FILES_DUBLS)

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

        self.w_text_debugger.insert(tkinter.END, u"Ищем новые фотографии\n")
        # собираем данные по файлам которые у нас уже есть
        dst_map = {}
        for root, dirs, files in os.walk(dst):
            for f in files:
                path = os.path.join(root, f)
                dst_map.setdefault(os.stat(path).st_size, []).append(path)

        self.w_text_debugger.insert(
            tkinter.END,
            u"Количесвто файлов нашего архива: {}\n".format(
                sum(len(i) for i in dst_map.values())))

        # собираем данные по файлам которых у нас нет
        src_map = {}
        for root, dirs, files in os.walk(src):
            for f in files:
                path = os.path.join(root, f)
                if f in (u'печать фото ', ):
                    continue

                # FIXME: тут может возникнуть ошибка с файлами в винде
                src_map.setdefault(os.stat(path).st_size, []).append(path)

        self.w_text_debugger.insert(
            tkinter.END,
            u"Количесвто файлов стороннего архива: {}\n".format(
                sum(len(i) for i in src_map.values())))

        # новые файлы по размеру
        new_files = []

        # новые файлы,
        # которые совпали по размеру и имени но не совпали по хешу
        new_dubl_files = []
        counter = 0
        count_src = len(src_map.keys()) 
        step = count_src / 10 or 1
        for size, photos in src_map.items():
            counter += 1
            if counter % step == 0:
                self.w_text_debugger.insert(
                    tkinter.END,
                    u"{}0%, ".format(counter/step))
            if size not in dst_map:
                # у нас нету файла с таким размером, значит он новый
                new_files.extend(photos)
            elif not self.w_checkbutton_only_size_variable.get():
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
                                buf = f.read(65536)
                                while buf:
                                    hasher.update(buf)
                                    buf = f.read(65536)
                                hashs.append(hasher.hexdigest())
                        for src_photo in photos:
                            with open(src_photo, "rb") as f:
                                hasher = hashlib.md5()
                                buf = f.read(65536)
                                while buf:
                                    hasher.update(buf)
                                    buf = f.read(65536)
                                if hasher.hexdigest() not in hashs:
                                    new_dubl_files.append({
                                        "src_files": photos,
                                        "dst_files": dst_photos,
                                    })
                                    break

        self.w_text_debugger.insert(
            tkinter.END,
            u"\nНайдено совсем новых файлов: {}\n".format(len(new_files)))

        self.w_text_debugger.insert(
            tkinter.END,
            u"Найдено новых файлов: {}\n".format(len(new_dubl_files)))

        new_files.sort()
        new_dubl_files.sort(key=lambda x: x['dst_files'])
        return new_files, new_dubl_files


class ImageFrame(BasePAFrame):
    """
    фрейм с картинкой
    """

    def __init__(self, *args, **kwargs):
        BasePAFrame.__init__(self, *args, **kwargs)

        self.image_label = tkinter.Label(self)

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
