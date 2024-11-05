import tkinter as tk
import tkinter.font as tk_font
from tkinter import filedialog


class MainPage:
    def __init__(self, root, client, files):
        self.root = root
        self.client = client
        self.files = files

        self.NO_FILES = ["No files have been uploaded yet."]

        self.gui()

    def gui(self):
        self.root.title("Files page")

        width = 811
        height = len(self.files) * 21 + 370
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        files_label = tk.Label(self.root)
        ft = tk_font.Font(family='Readex Pro', size=12)
        files_label["font"] = ft
        files_label["fg"] = "#333333"
        files_label["justify"] = "center"
        files_label["text"] = "Your files:"
        files_label.place(x=60, y=180, height=20)

        if not self.files:
            self.files = self.NO_FILES

        file_box = tk.Listbox(self.root, listvariable=tk.StringVar(value=self.files))
        file_box["borderwidth"] = "1.5px"
        ft = tk_font.Font(family='Readex Pro', size=11)
        file_box["font"] = ft
        file_box["fg"] = "#333333"
        file_box["justify"] = "left"
        file_box.place(x=170, y=180, width=411, height=len(self.files) * 22.5)

        file_status_label = tk.Label(self.root)
        ft = tk_font.Font(family='Readex Pro', size=8)
        file_status_label["font"] = ft
        file_status_label["justify"] = "left"
        file_status_label["fg"] = "#0000FF"
        file_status_label.place(x=60, y=(len(self.files) * 22.5 + 180), width=400, height=25)

        download_button = tk.Button(self.root)
        download_button["text"] = "Download"
        download_button["bg"] = "#3cbff7"
        ft = tk_font.Font(family='Readex Pro', size=10)
        download_button["font"] = ft
        download_button["fg"] = "#000000"
        download_button["justify"] = "center"
        download_button.place(x=170, y=130, width=88, height=25)
        download_button["command"] = lambda: self.download(file_box.curselection(), file_status_label)

        if self.files == self.NO_FILES:
            download_button["state"] = "disabled"

        upload_button = tk.Button(self.root)
        upload_button["text"] = "Upload"
        upload_button["bg"] = "#3cbff7"
        ft = tk_font.Font(family='Readex Pro', size=10)
        upload_button["font"] = ft
        upload_button["fg"] = "#000000"
        upload_button["justify"] = "center"
        upload_button.place(x=490, y=130, width=88, height=25)
        upload_button["command"] = lambda: self.upload(file_status_label)


    def download(self, selection: tuple, file_status_label: tk.Label):

        if selection == ():
            file_status_label["text"] = "Please click on a file to download it"
        else:
            file_idx = selection[0]
            file = self.files[file_idx]
            self.client.download(file)

            file_status_label["text"] = f"{file} has been downloaded"

    def upload(self, file_status_label: tk.Label) -> None:
        filename = filedialog.askopenfilename()

        if filename:
            if "." not in filename:
                file_status_label["text"] = f"file requires extension"
            else:
                file_addr = self.client.upload(filename)

                if self.files == self.NO_FILES:
                    self.files = []

                self.files.append(file_addr)

        self.gui()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainPage(root, "", ["No files have been uploaded yet."])
    root.mainloop()
