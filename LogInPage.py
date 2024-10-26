import tkinter as tk
import tkinter.font as tkFont

from Client import Client
from RegisterPage import RegisterPage
from MainPage import MainPage


class LogInPage:
    def __init__(self, root):
        self.root = root

        self.client = Client()

        self.gui()

    def gui(self):
        self.root.title("Log In Page")

        width = 680
        height = 433
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        log_in_label = tk.Label(self.root)
        ft = tkFont.Font(family='Readex Pro', size=17)
        log_in_label["font"] = ft
        log_in_label["fg"] = "#333333"
        log_in_label["justify"] = "center"
        log_in_label["text"] = "Log In"
        log_in_label.place(x=90, y=50, width=477, height=30)

        username_label = tk.Label(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        username_label["font"] = ft
        username_label["fg"] = "#333333"
        username_label["justify"] = "center"
        username_label["text"] = "Username:"
        username_label.place(x=180, y=120, width=70, height=25)

        password_label = tk.Label(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        password_label["font"] = ft
        password_label["fg"] = "#333333"
        password_label["justify"] = "center"
        password_label["text"] = "Password:"
        password_label.place(x=180, y=170, width=70, height=25)

        username_entry = tk.Entry(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        username_entry["font"] = ft
        username_entry["fg"] = "#333333"
        username_entry["justify"] = "left"
        username_entry["text"] = "Username:"
        username_entry.place(x=280, y=120, width=217, height=25)

        password_entry = tk.Entry(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        password_entry["font"] = ft
        password_entry["fg"] = "#333333"
        password_entry["justify"] = "left"
        password_entry["text"] = "Password:"
        password_entry.place(x=280, y=170, width=217, height=25)

        login_button = tk.Button(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        login_button["font"] = ft
        login_button["fg"] = "#000000"
        login_button["justify"] = "center"
        login_button["text"] = "Log In"
        login_button.place(x=160, y=230, width=365, height=25)
        login_button["command"] = lambda: self.log_in(username_entry.get(), password_entry.get())

        register_label = tk.Label(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        register_label["font"] = ft
        register_label["fg"] = "#333333"
        register_label["justify"] = "center"
        register_label["text"] = "Create an account instead?"
        register_label.place(x=190, y=280, width=159, height=30)

        register_button = tk.Button(self.root)
        ft = tkFont.Font(family='Readex Pro', size=9)
        register_button["font"] = ft
        register_button["fg"] = "#000000"
        register_button["bg"] = "#dc98ea"
        register_button["justify"] = "center"
        register_button["text"] = "Register"
        register_button.place(x=410, y=285, width=100, height=25)
        register_button["command"] = self.register


    def log_in(self, username, password):
        auth = self.client.log_in(username, password)

        if "Invalid" in auth[0]:
            inv_log_in_label = tk.Label(self.root)
            ft = tkFont.Font(family='Readex Pro', size=10)
            inv_log_in_label["font"] = ft
            inv_log_in_label["fg"] = "#f92f2f"
            inv_log_in_label["justify"] = "center"
            inv_log_in_label["text"] = "Invalid username or password"
            inv_log_in_label.place(x=100, y=200, width=477, height=30)

        else:
            self.root.destroy()

            main_root = tk.Tk()
            main_app = MainPage(main_root, self.client, auth[1])
            main_root.mainloop()


    def register(self):
        self.root.destroy()

        reg_root = tk.Tk()
        reg_gui = RegisterPage(reg_root, self.client)
        reg_root.mainloop()

        self.root = tk.Tk()
        self.gui()
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LogInPage(root)
    root.mainloop()
