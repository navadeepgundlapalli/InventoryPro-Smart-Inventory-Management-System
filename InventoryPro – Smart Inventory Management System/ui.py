import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from . import database as db

BG = "#081426"
PANEL = "#10233D"
PANEL2 = "#142B49"
BLUE = "#1677F2"
CYAN = "#39B8FF"
TEXT = "#EAF2FF"
MUTED = "#9FB3CC"
DANGER = "#FF647C"
GREEN = "#35D39A"

class InventoryProApp:
    def __init__(self, root, user):
        self.root, self.user = root, user
        self.root.title("InventoryPro | Inventory Management")
        self.root.geometry("1280x800")
        self.root.minsize(1050, 680)
        self.root.configure(bg=BG)
        self.selected_product = None
        self._style()
        self._layout()
        self.show_dashboard()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0D1D32", foreground=TEXT,
                        fieldbackground="#0D1D32", rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#1A3A61", foreground=TEXT,
                        font=("Segoe UI",10,"bold"), relief="flat")
        style.map("Treeview", background=[("selected", "#185DB5")])
        style.configure("TCombobox", fieldbackground="#0D1D32", background=PANEL2,
                        foreground=TEXT, arrowcolor=TEXT)

    def _layout(self):
        header = tk.Frame(self.root, bg="#0B1B30", height=68)
        header.pack(fill="x")
        tk.Label(header,text="◆  INVENTORYPRO",bg="#0B1B30",fg=CYAN,
                 font=("Segoe UI",18,"bold")).pack(side="left",padx=24,pady=16)
        tk.Label(header,text=f"{self.user['full_name']}  ·  {self.user['role'].upper()}",
                 bg="#0B1B30",fg=TEXT,font=("Segoe UI",10)).pack(side="right",padx=18)
        tk.Button(header,text="Logout",command=self.logout,bg="#263F5E",fg=TEXT,
                  activebackground=BLUE,activeforeground="white",relief="flat",
                  padx=16,pady=7).pack(side="right",padx=8)
        body = tk.Frame(self.root,bg=BG)
        body.pack(fill="both",expand=True)
        side = tk.Frame(body,bg="#0B1B30",width=220)
        side.pack(side="left",fill="y")
        side.pack_propagate(False)
        tk.Label(side,text="WORKSPACE",bg="#0B1B30",fg=MUTED,
                 font=("Segoe UI",9,"bold")).pack(anchor="w",padx=20,pady=(24,10))
        nav = [("▦  Dashboard",self.show_dashboard),("▤  Products",self.show_products),
               ("⇄  Stock Movement",self.show_movement),("▧  Suppliers",self.show_suppliers),
               ("◷  Reports",self.show_reports)]
        if self.user["role"] == "admin":
            nav.append(("♙  User Accounts",self.show_users))
        for label, command in nav:
            tk.Button(side,text=label,command=command,anchor="w",bg="#0B1B30",fg=TEXT,
                      activebackground="#173A63",activeforeground=CYAN,relief="flat",
                      font=("Segoe UI",10),padx=20,pady=13).pack(fill="x",padx=8,pady=2)
        self.content = tk.Frame(body,bg=BG)
        self.content.pack(side="left",fill="both",expand=True,padx=24,pady=22)

    def clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def title(self, heading, subtitle=""):
        tk.Label(self.content,text=heading,bg=BG,fg=TEXT,font=("Segoe UI",22,"bold")).pack(anchor="w")
        if subtitle:
            tk.Label(self.content,text=subtitle,bg=BG,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",pady=(3,18))

    def button(self, parent, text, command, color=BLUE):
        return tk.Button(parent,text=text,command=command,bg=color,fg="white",
                         activebackground=CYAN,activeforeground=BG,relief="flat",
                         font=("Segoe UI",9,"bold"),padx=14,pady=8,cursor="hand2")

    def tree(self, parent, columns, headings, height=12):
        frame=tk.Frame(parent,bg=BG)
        frame.pack(fill="both",expand=True,pady=10)
        tree=ttk.Treeview(frame,columns=columns,show="headings",height=height)
        for col,head in zip(columns,headings):
            tree.heading(col,text=head); tree.column(col,width=120,anchor="w")
        scroll=ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")
        return tree

    def show_dashboard(self):
        self.clear(); self.title("Overview","Monitor stock levels, inventory value and recent activity.")
        s=db.dashboard_stats()
        cards=tk.Frame(self.content,bg=BG); cards.pack(fill="x",pady=6)
        metrics=[("PRODUCT TYPES",s["products"],CYAN),("TOTAL UNITS",s["units"],GREEN),
                 ("LOW STOCK ITEMS",s["low_stock"],DANGER),("INVENTORY VALUE",f"₹{s['value']:,.2f}",TEXT)]
        for label,value,color in metrics:
            card=tk.Frame(cards,bg=PANEL,padx=18,pady=16)
            card.pack(side="left",fill="both",expand=True,padx=(0,12))
            tk.Label(card,text=label,bg=PANEL,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
            tk.Label(card,text=str(value),bg=PANEL,fg=color,font=("Segoe UI",22,"bold")).pack(anchor="w",pady=(8,0))
        tk.Label(self.content,text="RECENT STOCK ACTIVITY",bg=BG,fg=TEXT,
                 font=("Segoe UI",12,"bold")).pack(anchor="w",pady=(24,4))
        tree=self.tree(self.content,("date","product","type","qty","user"),
                       ("DATE","PRODUCT","MOVEMENT","QUANTITY","USER"),height=10)
        for r in s["recent"]:
            tree.insert("", "end", values=(r["created_at"],r["product_name"],r["movement_type"],r["quantity"],r["username"] or "—"))

    def show_products(self):
        self.clear(); self.title("Product Catalogue","Create, update, search and maintain inventory items.")
        bar=tk.Frame(self.content,bg=BG); bar.pack(fill="x")
        search=tk.Entry(bar,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat",font=("Segoe UI",10),width=32)
        search.pack(side="left",ipady=9,padx=(0,8)); search.insert(0,"Search SKU, name or category")
        self.button(bar,"Search",lambda: load()).pack(side="left",padx=3)
        self.button(bar,"Add Product",lambda: self.product_form()).pack(side="right",padx=3)
        if self.user["role"]=="admin":
            self.button(bar,"Delete Selected",lambda: delete(),DANGER).pack(side="right",padx=3)
        tree=self.tree(self.content,("id","sku","name","category","qty","reorder","price","supplier"),
                       ("ID","SKU","PRODUCT","CATEGORY","QTY","REORDER AT","UNIT PRICE","SUPPLIER"),height=15)
        def load():
            tree.delete(*tree.get_children())
            for p in db.products(search.get() if search.get()!="Search SKU, name or category" else ""):
                tree.insert("","end",values=(p["id"],p["sku"],p["name"],p["category"],p["quantity"],p["reorder_level"],f"₹{p['unit_price']:.2f}",p["supplier_name"] or "—"))
        def delete():
            sel=tree.selection()
            if not sel: messagebox.showinfo("Select product","Choose a product first."); return
            pid=tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirm","Delete this product and its movement history?"):
                db.delete_product(pid); load()
        def edit(event):
            sel=tree.selection()
            if sel:
                vals=tree.item(sel[0])["values"]
                self.product_form(vals[0])
        tree.bind("<Double-1>",edit); load()

    def product_form(self, product_id=None):
        old=None
        if product_id:
            old=next((p for p in db.products() if p["id"]==product_id),None)
        win=tk.Toplevel(self.root); win.title("Product Details"); win.configure(bg=BG); win.geometry("440x570"); win.transient(self.root); win.grab_set()
        tk.Label(win,text="PRODUCT DETAILS",bg=BG,fg=CYAN,font=("Segoe UI",16,"bold")).pack(pady=18)
        fields={}
        labels=[("SKU","sku"),("Product name","name"),("Category","category"),("Quantity","quantity"),("Reorder level","reorder"),("Unit price (₹)","price")]
        for label,key in labels:
            tk.Label(win,text=label,bg=BG,fg=MUTED).pack(anchor="w",padx=35)
            ent=tk.Entry(win,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief="flat")
            ent.pack(fill="x",padx=35,pady=(4,12),ipady=8)
            if old:
                source={"reorder":old["reorder_level"],"price":old["unit_price"]}.get(key,old[key])
                ent.insert(0,str(source))
            elif key in ("quantity","reorder","price"): ent.insert(0,"0" if key!="reorder" else "5")
            fields[key]=ent
        tk.Label(win,text="Supplier",bg=BG,fg=MUTED).pack(anchor="w",padx=35)
        sup=db.suppliers(); choices={"None":None}
        for s in sup: choices[f"{s['id']} - {s['name']}"]=s["id"]
        combo=ttk.Combobox(win,values=list(choices),state="readonly"); combo.pack(fill="x",padx=35,pady=7); combo.set("None")
        if old and old["supplier_id"]:
            for k,v in choices.items():
                if v==old["supplier_id"]: combo.set(k)
        def save():
            try:
                db.save_product(fields["sku"].get(),fields["name"].get(),fields["category"].get(),
                    fields["quantity"].get(),fields["reorder"].get(),fields["price"].get(),
                    choices.get(combo.get()),product_id)
                messagebox.showinfo("Saved","Product saved successfully."); win.destroy(); self.show_products()
            except Exception as e: messagebox.showerror("Validation error",str(e))
        self.button(win,"Save Product",save).pack(pady=18)

    def show_movement(self):
        self.clear(); self.title("Stock Movement","Record incoming stock and outgoing stock with an audit trail.")
        form=tk.Frame(self.content,bg=PANEL,padx=18,pady=18); form.pack(fill="x")
        prods=db.products(); options={f"{p['id']} | {p['sku']} - {p['name']}":p["id"] for p in prods}
        tk.Label(form,text="Product",bg=PANEL,fg=TEXT).grid(row=0,column=0,sticky="w",padx=6)
        product=ttk.Combobox(form,values=list(options),state="readonly",width=35); product.grid(row=1,column=0,padx=6,pady=8)
        tk.Label(form,text="Movement",bg=PANEL,fg=TEXT).grid(row=0,column=1,sticky="w",padx=6)
        kind=ttk.Combobox(form,values=["STOCK_IN","STOCK_OUT"],state="readonly",width=18); kind.grid(row=1,column=1,padx=6,pady=8); kind.set("STOCK_IN")
        tk.Label(form,text="Quantity",bg=PANEL,fg=TEXT).grid(row=0,column=2,sticky="w",padx=6)
        qty=tk.Entry(form,bg="#0D1D32",fg=TEXT,insertbackground=TEXT,relief="flat",width=12); qty.grid(row=1,column=2,padx=6,pady=8,ipady=7)
        tk.Label(form,text="Note",bg=PANEL,fg=TEXT).grid(row=0,column=3,sticky="w",padx=6)
        note=tk.Entry(form,bg="#0D1D32",fg=TEXT,insertbackground=TEXT,relief="flat",width=24); note.grid(row=1,column=3,padx=6,pady=8,ipady=7)
        def submit():
            try:
                if not product.get(): raise ValueError("Choose a product.")
                db.record_movement(options[product.get()],self.user["id"],kind.get(),qty.get(),note.get())
                messagebox.showinfo("Recorded","Stock movement recorded."); self.show_movement()
            except Exception as e: messagebox.showerror("Could not record movement",str(e))
        self.button(form,"Record Movement",submit).grid(row=1,column=4,padx=8)
        tk.Label(self.content,text="MOVEMENT HISTORY",bg=BG,fg=TEXT,font=("Segoe UI",12,"bold")).pack(anchor="w",pady=(22,3))
        tree=self.tree(self.content,("id","date","sku","name","type","qty","user","note"),
                       ("ID","DATE","SKU","PRODUCT","TYPE","QTY","USER","NOTE"),height=12)
        for r in db.movement_history():
            tree.insert("","end",values=(r["id"],r["created_at"],r["sku"],r["name"],r["movement_type"],r["quantity"],r["username"] or "—",r["note"]))

    def show_suppliers(self):
        self.clear(); self.title("Suppliers","Maintain supplier contacts for purchasing and replenishment.")
        form=tk.Frame(self.content,bg=PANEL,padx=14,pady=14); form.pack(fill="x")
        entries=[]
        for i,label in enumerate(("Supplier name","Contact","Email","Notes")):
            tk.Label(form,text=label,bg=PANEL,fg=MUTED).grid(row=0,column=i,sticky="w",padx=5)
            e=tk.Entry(form,bg="#0D1D32",fg=TEXT,insertbackground=TEXT,relief="flat",width=22)
            e.grid(row=1,column=i,padx=5,pady=7,ipady=7); entries.append(e)
        def add():
            try:
                if not entries[0].get().strip(): raise ValueError("Supplier name is required.")
                db.add_supplier(*(e.get() for e in entries))
                messagebox.showinfo("Added","Supplier added."); self.show_suppliers()
            except Exception as e: messagebox.showerror("Error",str(e))
        self.button(form,"Add Supplier",add).grid(row=1,column=4,padx=8)
        tree=self.tree(self.content,("id","name","contact","email","notes"),("ID","SUPPLIER","CONTACT","EMAIL","NOTES"),height=14)
        for s in db.suppliers(): tree.insert("","end",values=(s["id"],s["name"],s["contact"],s["email"],s["notes"]))

    def show_reports(self):
        self.clear(); self.title("Reports & Export","Export inventory and stock movement data for analysis.")
        tk.Label(self.content,text="Generate CSV files that can be opened in Excel or imported into analysis tools.",
                 bg=BG,fg=MUTED).pack(anchor="w",pady=(0,18))
        def export_products():
            path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files","*.csv")],initialfile="inventory_report.csv")
            if not path:return
            rows=db.products()
            with open(path,"w",newline="",encoding="utf-8-sig") as f:
                w=csv.writer(f); w.writerow(["SKU","Product","Category","Quantity","Reorder Level","Unit Price","Supplier"])
                for p in rows:w.writerow([p["sku"],p["name"],p["category"],p["quantity"],p["reorder_level"],p["unit_price"],p["supplier_name"]])
            messagebox.showinfo("Export complete",f"Saved {len(rows)} products.")
        def export_moves():
            path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV files","*.csv")],initialfile="stock_movements.csv")
            if not path:return
            rows=db.movement_history()
            with open(path,"w",newline="",encoding="utf-8-sig") as f:
                w=csv.writer(f); w.writerow(["Date","SKU","Product","Type","Quantity","User","Note"])
                for r in rows:w.writerow([r["created_at"],r["sku"],r["name"],r["movement_type"],r["quantity"],r["username"],r["note"]])
            messagebox.showinfo("Export complete",f"Saved {len(rows)} movements.")
        self.button(self.content,"Export Inventory CSV",export_products).pack(anchor="w",pady=8)
        self.button(self.content,"Export Stock Movement CSV",export_moves).pack(anchor="w",pady=8)

    def show_users(self):
        if self.user["role"]!="admin": return
        self.clear(); self.title("User Accounts","Admin-only user management. New accounts are staff by default.")
        form=tk.Frame(self.content,bg=PANEL,padx=16,pady=16); form.pack(fill="x")
        labels=("Full name","Username","Password")
        es=[]
        for i,label in enumerate(labels):
            tk.Label(form,text=label,bg=PANEL,fg=MUTED).grid(row=0,column=i,sticky="w",padx=6)
            e=tk.Entry(form,bg="#0D1D32",fg=TEXT,insertbackground=TEXT,relief="flat",width=25,
                       show="*" if label=="Password" else "")
            e.grid(row=1,column=i,padx=6,pady=8,ipady=8); es.append(e)
        def create():
            try:
                db.create_user(es[1].get(),es[2].get(),es[0].get(),"staff")
                messagebox.showinfo("Created","Staff account created."); self.show_users()
            except Exception as e: messagebox.showerror("Could not create account",str(e))
        self.button(form,"Create Staff Account",create).grid(row=1,column=3,padx=8)
        tree=self.tree(self.content,("id","name","username","role","created"),("ID","FULL NAME","USERNAME","ROLE","CREATED"),height=13)
        for u in db.list_users():tree.insert("","end",values=(u["id"],u["full_name"],u["username"],u["role"],u["created_at"]))

    def logout(self):
        if messagebox.askyesno("Logout","Are you sure you want to log out?"):
            self.root.destroy()
            from .auth_ui import launch
            launch()

def launch_app(user):
    root=tk.Tk()
    InventoryProApp(root,user)
    root.mainloop()
