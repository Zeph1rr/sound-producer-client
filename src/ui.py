from tkinter import Tk, ttk, Entry, StringVar
from loguru import logger
from os.path import join, dirname, abspath


class ClientUI:
    def __init__(self):
        self.__init_main_window()

        self.url = StringVar(value="localhost")
        self.nickname = StringVar(value="user")

        self.__init_ui()

    def __init_main_window(self):
        self.root: Tk = Tk()
        self.root.geometry('400x220')
        self.root.resizable(False, False)
        self.root.title("SoundProducer")
        self.root.iconbitmap(join(dirname(abspath(__file__)), "assets", "images", "dark_icon.ico"))
        ttk.Style().theme_use('alt')

    def __init_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        self.status_label = ttk.Label(frm, text="", width=60)
        self.status_label.grid(row=0, pady=5, columnspan=3)

        ttk.Label(frm, text="URL").grid(column=0, row=1, padx=10)
        Entry(frm, textvariable=self.url, width=35).grid(column=1, row=1, pady=10, columnspan=2)

        ttk.Label(frm, text="Nickname").grid(column=0, row=2, padx=10)
        Entry(frm, textvariable=self.nickname, width=35).grid(column=1, row=2, pady=10, columnspan=2)

        self.record_button = ttk.Button(frm, text="Start recording")
        self.record_button.grid(column=0, row=3, padx=(40, 0))

        self.send_data_button = ttk.Button(frm, text="Send data")
        self.send_data_button.grid(column=1, row=3, pady=10, padx=40)

        self.create_speaker_button = ttk.Button(frm, text="Create speaker")
        self.create_speaker_button.grid(column=2, row=3, padx=(0, 40), pady=10)

        self.current_file_label = ttk.Label(frm, text="Last file: ", width=60)
        self.current_file_label.grid(row=4, pady=5, columnspan=3)

        self.current_time_label = ttk.Label(frm, text="Current record length: ", width=60)
        self.current_time_label.grid(row=5, pady=5, columnspan=3)

    def mainloop(self):
        try:
            self.root.mainloop()
        except OSError as ex:
            logger.error(ex)
