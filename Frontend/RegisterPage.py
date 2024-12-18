import tkinter as tk
import tkinter.font as tk_font
import re


class RegisterPage:
    def __init__(self, root, client):
        self.root = root
        self.client = client

        self.root.title("Sign Up page")
        width = 680
        height = 433
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2, (screen_height - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        register_label = tk.Label(self.root)
        ft = tk_font.Font(family='Readex Pro', size=17)
        register_label["font"] = ft
        register_label["fg"] = "#333333"
        register_label["justify"] = "center"
        register_label["text"] = "Create an account"
        register_label.place(x=90, y=50, width=477, height=30)

        ft = tk_font.Font(family='Readex Pro', size=9)

        username_label = tk.Label(self.root)
        username_label["font"] = ft
        username_label["fg"] = "#333333"
        username_label["justify"] = "center"
        username_label["text"] = "Username:"
        username_label.place(x=180, y=120, width=70, height=25)

        password_label = tk.Label(self.root)
        password_label["font"] = ft
        password_label["fg"] = "#333333"
        password_label["justify"] = "center"
        password_label["text"] = "Password:"
        password_label.place(x=180, y=170, width=70, height=25)

        self.confirm_password = tk.Label(self.root)
        self.confirm_password["font"] = ft
        self.confirm_password["fg"] = "#333333"
        self.confirm_password["justify"] = "center"
        self.confirm_password["text"] = "Confirm password:"
        self.confirm_password.place(x=150, y=220, width=120, height=25)

        self.username_entry = tk.Entry(self.root)
        self.username_entry["borderwidth"] = "1px"
        ft = tk_font.Font(family='Readex Pro', size=8)
        self.username_entry["font"] = ft
        self.username_entry["fg"] = "#333333"
        self.username_entry["justify"] = "left"
        self.username_entry["text"] = "hi"
        self.username_entry.place(x=280, y=120, width=217, height=25)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry["borderwidth"] = "1px"
        ft = tk_font.Font(family='Readex Pro', size=9)
        self.password_entry["font"] = ft
        self.password_entry["fg"] = "#333333"
        self.password_entry["justify"] = "left"
        self.password_entry.place(x=280, y=170, width=217, height=25)

        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry["borderwidth"] = "1px"
        ft = tk_font.Font(family='Readex Pro', size=9)
        self.confirm_password_entry["font"] = ft
        self.confirm_password_entry["fg"] = "#333333"
        self.confirm_password_entry["justify"] = "left"
        self.confirm_password_entry.place(x=280, y=220, width=217, height=25)

        register_button = tk.Button(self.root)
        register_button["bg"] = "#3c59cc"
        ft = tk_font.Font(family='Readex Pro', size=10)
        register_button["font"] = ft
        register_button["fg"] = "#333333"
        register_button["justify"] = "left"
        register_button["text"] = "Sign Up"
        register_button.place(x=160, y=280, width=365, height=25)
        register_button["command"] = lambda: self.register(self.username_entry.get(), self.password_entry.get(),
                                                           self.confirm_password_entry.get())

        register_label = tk.Label(self.root)
        ft = tk_font.Font(family='Readex Pro', size=9)
        register_label["font"] = ft
        register_label["fg"] = "#333333"
        register_label["justify"] = "center"
        register_label["text"] = "Log In instead?"
        register_label.place(x=190, y=325, width=159, height=30)

        login_button = tk.Button(self.root)
        login_button["bg"] = "#dc98ea"
        ft = tk_font.Font(family='Readex Pro', size=9)
        login_button["font"] = ft
        login_button["fg"] = "#000000"
        login_button["justify"] = "center"
        login_button["text"] = "Log In"
        login_button.place(x=410, y=330, width=100, height=25)
        login_button["command"] = self.log_in

    def register(self, username: str, password: str, confirm_password: str) -> None:
        register_err_label = tk.Label(self.root)
        ft = tk_font.Font(family='Readex Pro', size=7)
        register_err_label["font"] = ft
        register_err_label["fg"] = "#f92f2f"
        register_err_label["justify"] = "center"
        register_err_label.place(x=100, y=250, width=477, height=30)

        err_text = None
        if username == "" or password == "":
            err_text = "Username already in use."

        elif password != confirm_password:
            err_text = "Passwords do not match."

        elif len(password) < 8:
            err_text = "Password must be at least 8 characters long."

        elif re.search("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*(\\W))", password) is None:
            err_text = "Passwords should have upper and lower case letters, one number and one special character."

        if err_text is None and "User created successfully" in self.client.sign_up(username, password):
            self.root.destroy()
        else:
            register_err_label["text"] = err_text

    def log_in(self) -> None:
        self.root.destroy()


if __name__ == "__main__":
    rootq = tk.Tk()
    app = RegisterPage(rootq, "")
    rootq.mainloop()
