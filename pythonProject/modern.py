import os
import tkinter.messagebox as tkmb
import subprocess
import customtkinter as ctk


def show_register_window():
    register_window = ctk.CTkToplevel(app)
    register_window.title("Kayıt Ol")
    register_window.geometry("400x300")

    register_frame = ctk.CTkFrame(master=register_window)
    register_frame.pack(pady=20, padx=40, fill='both', expand=True)

    register_label = ctk.CTkLabel(master=register_frame, text='Kayıt Formu')
    register_label.pack(pady=12, padx=10)

    register_username_entry = ctk.CTkEntry(master=register_frame, placeholder_text="Kullanıcı Adı")
    register_username_entry.pack(pady=12, padx=10)

    register_password_entry = ctk.CTkEntry(master=register_frame, placeholder_text="Şifre", show="*")
    register_password_entry.pack(pady=12, padx=10)

    def register():
        new_username = register_username_entry.get()
        new_password = register_password_entry.get()

        if not username_exists(new_username):
            save_user_credentials(new_username, new_password)
            tkmb.showinfo(title="Kayıt Başarılı", message="Kayıt işlemi tamamlandı")
            register_window.destroy()
        else:
            tkmb.showerror(title="Hata", message="Bu kullanıcı adı zaten mevcut!")

    register_button = ctk.CTkButton(master=register_frame, text='Kayıt Ol', command=register)
    register_button.pack(pady=12, padx=10)

def login():
    entered_username = user_entry.get()
    entered_password = user_pass.get()

    if validate_credentials(entered_username, entered_password):
        tkmb.showinfo(title="Giriş Başarılı", message="Giriş yaptınız")
        open_second_file()
        app.destroy()  # Ana pencereyi kapat
    else:
        tkmb.showerror(title="Giriş Başarısız", message="Yanlış şifre veya kullanıcı adı")

def validate_credentials(entered_username, entered_password):
    user_credentials = read_user_credentials()
    return user_credentials.get(entered_username) == entered_password

def open_second_file():
    try:
        subprocess.run(["python", "main.py"])
    except Exception as e:
        print(f"Hata: {e}")
def username_exists(username):
    user_credentials = read_user_credentials()
    return username in user_credentials

def save_user_credentials(username, password):
    user_credentials = read_user_credentials()
    user_credentials[username] = password

    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, "user_credentials.txt")

    with open(file_path, "a") as file:
        file.write(f"{username}:{password}\n")

def read_user_credentials():
    user_credentials = {}

    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, "user_credentials.txt")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(":")
                user_credentials[username] = password

    return user_credentials


app = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

label = ctk.CTkLabel(app, text="Bu ana UI sayfasıdır")
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Giriş Sayfasi')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Kullanıcı Adı")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Şifre", show="*")
user_pass.pack(pady=12, padx=10)

login_button = ctk.CTkButton(master=frame, text='Giriş', command=login)
login_button.pack(pady=12, padx=10)

register_button = ctk.CTkButton(master=frame, text='Kayıt Ol', command=show_register_window)
register_button.pack(pady=12, padx=10)

app.mainloop()
