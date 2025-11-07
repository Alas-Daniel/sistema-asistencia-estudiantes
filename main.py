from ui_login import AdminLogin
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = AdminLogin(root)
    app.mainloop()
  