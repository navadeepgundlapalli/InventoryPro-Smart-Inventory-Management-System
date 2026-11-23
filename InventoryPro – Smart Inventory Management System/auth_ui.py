import tkinter as tk
from tkinter import messagebox
from . import database as db
from .ui import launch_app, BG, PANEL, BLUE, CYAN, TEXT, MUTED

def launch():
    db.initialize()
    root=tk.Tk(); root.title("InventoryPro | Secure Sign In"); root.geometry("900x590")
    root.resizable(False,False); root.configure(bg=BG)
    left=tk.Frame(root,bg="#0D2543",width=390); left.pack(side="left",fill="y"); left.pack_propagate(False)
    tk.Label(left,text="◆",bg="#0D2543",fg=CYAN,font=("Segoe UI",52,"bold")).pack(pady=(95,8))
    tk.Label(left,text="INVENTORYPRO",bg="#0D2543",fg=TEXT,font=("Segoe UI",23,"bold")).pack()
    tk.Label(left,text="CONTROL YOUR STOCK.\nPOWER YOUR BUSINESS.",bg="#0D2543",fg=MUTED,
             font=("Segoe UI",11),justify="center").pack(pady=18)
    tk.Label(left,text="PYTHON • SQLITE • DESKTOP GUI",bg="#0D2543",fg="#6E91B9",
             font=("Segoe UI",8,"bold")).pack(side="bottom",pady=28)
    right=tk.Frame(root,bg=BG,padx=58,pady=60); right.pack(side="left",fill="both",expand=True)
    tk.Label(right,text="Welcome back",bg=BG,fg=TEXT,font=("Segoe UI",25,"bold")).pack(anchor="w")
    tk.Label(right,text="Sign in to access your inventory workspace.",bg=BG,fg=MUTED,
             font=("Segoe UI",10)).pack(anchor="w",pady=(6,30))
    tk.Label(right,text="USERNAME",bg=BG,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
    username=tk.Entry(right,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",font=("Segoe UI",11))
    username.pack(fill="x",pady=(7,18),ipady=11); username.insert(0,"admin")
    tk.Label(right,text="PASSWORD",bg=BG,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
    password=tk.Entry(right,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",font=("Segoe UI",11),show="•")
    password.pack(fill="x",pady=(7,22),ipady=11)
    def login():
        user=db.authenticate(username.get(),password.get())
        if not user:
            messagebox.showerror("Sign in failed","Invalid username or password."); return
        root.destroy(); launch_app(user)
    def register():
        win=tk.Toplevel(root); win.title("Create Staff Account"); win.geometry("380x410"); win.configure(bg=BG); win.transient(root); win.grab_set()
        fields={}
        for label,key in [("Full name","name"),("Username","username"),("Password (8+ characters)","password")]:
            tk.Label(win,text=label,bg=BG,fg=MUTED).pack(anchor="w",padx=30,pady=(14,3))
            e=tk.Entry(win,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",show="*" if key=="password" else "")
            e.pack(fill="x",padx=30,ipady=8); fields[key]=e
        def save():
            try:
                db.create_user(fields["username"].get(),fields["password"].get(),fields["name"].get(),"staff")
                messagebox.showinfo("Account created","Your staff account is ready. Sign in now."); win.destroy()
            except Exception as e: messagebox.showerror("Registration error",str(e))
        tk.Button(win,text="CREATE ACCOUNT",command=save,bg=BLUE,fg="white",relief="flat",pady=10).pack(fill="x",padx=30,pady=24)
    tk.Button(right,text="SIGN IN",command=login,bg=BLUE,fg="white",activebackground=CYAN,
              relief="flat",font=("Segoe UI",10,"bold"),pady=12).pack(fill="x")
    tk.Button(right,text="Create staff account",command=register,bg=BG,fg=CYAN,
              activebackground=BG,relief="flat",pady=12).pack(anchor="center",pady=10)
    tk.Label(right,text="First run admin: admin  |  password: Admin@123\nChange this password before real use.",
             bg=BG,fg="#F0B95B",font=("Segoe UI",8),justify="center").pack(side="bottom",pady=5)
    password.bind("<Return>",lambda e:login())
    root.mainloop()
