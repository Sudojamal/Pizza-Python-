import tkinter as tk
from tkinter import messagebox
import requests
import json

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("300x200")
        
        # Username Label and Entry
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        
        # Password Label and Entry
        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        # Login Button
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(root, text="", fg="red")
        self.status_label.pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            response = requests.post(
                "http://localhost:5000/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                messagebox.showinfo("Success", f"Welcome, {data['username']}!")
                self.status_label.config(text="Login successful!", fg="green")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", response.json().get("message", "Login failed"))
                self.status_label.config(text="Login failed!", fg="red")
        
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Error", "Cannot connect to server")
            self.status_label.config(text="Connection error!", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()
