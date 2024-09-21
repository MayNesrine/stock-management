import mysql.connector
from tkinter import messagebox
import tkinter as tk

class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        master.title("Login")
        master.geometry("400x250")
        master.configure(bg="lightblue")
        master.resizable(False, False)  

        self.label_username = tk.Label(master, text="Username:",bg="lightblue")
        self.label_username.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=1, column=1, padx=10, pady=20)

        self.label_password = tk.Label(master, text="Password:",bg="lightblue")
        self.label_password.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=20, sticky="w")

        self.btn_login = tk.Button(master, text="Login", command=self.login,bg="#6b9aaf")
        self.btn_login.grid(row=3, column=1, columnspan=2, padx=20, pady=10, ipadx=25, ipady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rpi",
            database="project_Omar"
        )
        cursor = conn.cursor()
            # Vérification des informations d'identification dans la base de données
        cursor.execute("SELECT * FROM login WHERE Username=%s AND Password=%s", (username, password))
        row = cursor.fetchone()
        if row:
           messagebox.showinfo("Login", "Login successful!")
                # Si l'authentification est réussie, détruire la fenêtre de connexion et afficher la fenêtre principale de l'application
           self.master.destroy()
           self.app.show_main_window() 
        else:
           messagebox.showerror("Login", "Invalid username or password")
                # Efface les champs de saisie pour un nouvel essai
           self.entry_username.delete(0, tk.END)
           self.entry_password.delete(0, tk.END)

"""root = tk.Tk()
main_app = GestionStock(root)
login_window = LoginWindow(root, main_app)
root.mainloop()"""
