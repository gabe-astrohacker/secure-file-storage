import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog


class MainPage:
    def __init__(self, root, client, my_files):
        self.root = root
        self.client = client
        self.my_list = my_files

        self.gui()

    def gui(self):
        files = tk.StringVar(value=self.my_list)

        self.root.title("Files page")

        width = 811
        height = len(self.my_list) * 21 + 370
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        files_label = tk.Label(self.root)
        ft = tkFont.Font(family='Readex Pro', size=12)
        files_label["font"] = ft
        files_label["fg"] = "#333333"
        files_label["justify"] = "center"
        files_label["text"] = "Your files:"
        files_label.place(x=60, y=180, height=20)

        file_box = tk.Listbox(self.root, listvariable=files)

        file_box["borderwidth"] = "1.5px"
        ft = tkFont.Font(family='Readex Pro', size=11)
        file_box["font"] = ft
        file_box["fg"] = "#333333"
        file_box["justify"] = "left"
        file_box.place(x=170, y=180, width=411, height=len(self.my_list) * 22.5)

        download_button = tk.Button(self.root)
        download_button["text"] = "Download"
        download_button["bg"] = "#3cbff7"
        ft = tkFont.Font(family='Readex Pro', size=10)
        download_button["font"] = ft
        download_button["fg"] = "#000000"
        download_button["justify"] = "center"
        download_button.place(x=170, y=130, width=88, height=25)
        download_button["command"] = lambda: self.download(file_box.curselection())

        upload_button = tk.Button(self.root)
        upload_button["text"] = "Upload"
        upload_button["bg"] = "#3cbff7"
        ft = tkFont.Font(family='Readex Pro', size=10)
        upload_button["font"] = ft
        upload_button["fg"] = "#000000"
        upload_button["justify"] = "center"
        upload_button.place(x=490, y=130, width=88, height=25)
        upload_button["command"] = self.upload

        if self.my_list == ["No files have been uploaded yet."]:
            download_button["state"] = "disabled"


    def download(self, index):
        if index == ():
            file_status_label = tk.Label(self.root)
            ft = tkFont.Font(family='Readex Pro', size=8)
            file_status_label["font"] = ft
            file_status_label["justify"] = "left"
            file_status_label["fg"] = "#0000FF"
            file_status_label["text"] = "Please click on a file to download it"
            file_status_label.place(x=60, y=(len(self.my_list) * 22.5 + 180), width=400, height=25)

        else:
            file = self.my_list[index[0]]
            self.client.download(file)

            file_status_label = tk.Label(self.root)
            ft = tkFont.Font(family='Readex Pro', size=8)
            file_status_label["font"] = ft
            file_status_label["justify"] = "left"
            file_status_label["fg"] = "#0000FF"
            file_status_label["text"] = f"{file} has been downloaded"
            file_status_label.place(x=60, y=(len(self.my_list) * 22.5 + 180), width=400, height=25)


    def upload(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            file_addr = self.client.upload(filename)
            self.my_list.append(file_addr)

            if self.my_list[0] == "No files have been uploaded yet.":
                self.my_list.pop(0)

        self.gui()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainPage(root, "", ["No files have been uploaded yet."])
    root.mainloop()
