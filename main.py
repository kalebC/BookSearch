import json
import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import webbrowser
# import mysql.connector


def validate(username, password):
    if username == "admin" and password == "admin":
        messagebox.showinfo("", "Logado com sucesso!")
        login.withdraw()
        lg_entry.delete(0, END)
        ps_entry.delete(0, END)
        open_main()
    else:
        messagebox.showinfo("Erro", "Usuário e/ou senha inválidos!")


def logout():
    root.destroy()
    login.deiconify()


def open_main():
    
    with open("new.json", "r") as file:
        data = json.load(file)

    def dump_data():
        with open("new.json", "w") as fw:
            json.dump(data, fw, indent=4)

    def show_all():
        tree.delete(*tree.get_children())
        for x in data:
            tree.insert(parent='', index='end', text="", values=(x["title"],
                                                                 x["author"],
                                                                 x["year"],
                                                                 x["isbn"]))

    def search_book():
        tree.delete(*tree.get_children())
        entries = [entry1, entry2, entry3, entry4]
        sdata = []

        v_entries = {"title": entries[0].get(),  # store entries in a dict
                     "author": entries[1].get(),
                     "year": entries[2].get(),
                     "isbn": entries[3].get()
                     }
        v_entries = {k: v for k, v in v_entries.items() if v}  # remove empty values from dict

        for k, v in v_entries.items():  # converts all number values from str to int
            if v_entries[k].isnumeric():
                v_entries[k] = int(v)

        for i in range(len(data)):
            if v_entries.items() <= data[i].items():
                sdata.append(data[i])

        if len(sdata) > 0:
            for i in sdata:
                tree.insert(parent='', index='end', text="", values=(i["title"],
                                                                     i["author"],
                                                                     i["year"],
                                                                     i["isbn"]))
        else:
            messagebox.showinfo("Erro", "Sua busca retornou 0 resultados!")
            show_all()

    def add_book():
        not_in_db = True
        # get data from entry boxes
        new_title = entry1.get()
        new_author = entry2.get()
        new_year = entry3.get()
        new_isbn = entry4.get()
        e_list = [new_title, new_author, new_year, new_isbn]

        for entry in e_list:
            if len(entry) == 0:
                messagebox.showinfo("Erro", "Preencha todas as caixas de entrada!")
                return

        for n in range(2, 4):
            if e_list[n].isalpha():
                messagebox.showinfo("Erro", "Use apenas números para Ano/ISBN!")
                return

        e_dict = {"title": new_title,
                  "author": new_author,
                  "year": int(new_year),
                  "isbn": int(new_isbn)
                  }

        for i in range(len(data)):
            if data[i] == e_dict:
                not_in_db = False

        # store data from entry boxes in a dict
        if not_in_db:
            data.append(e_dict)  # add dict to list books
            dump_data()  # dumps altered list in .json file
            tree.insert(parent='', index='end', text="", values=(new_title,  # insert data in tree
                                                                 new_author,
                                                                 new_year,
                                                                 new_isbn))
            # delete text from entry boxes
            clear_entries()
            messagebox.showinfo("", "Livro adicionado com sucesso!")
        else:
            messagebox.showinfo("Erro", "Esse livro já está na lista!")

    def select_book(e):
        clear_entries()
        selected = tree.focus()
        values = tree.item(selected, "values")
        try:
            entry1.insert(0, values[0])
            entry2.insert(0, values[1])
            entry3.insert(0, values[2])
            entry4.insert(0, values[3])
        except IndexError:
            clear_entries()

    def clear_entries():
        entry1.delete(0, "end")
        entry2.delete(0, "end")
        entry3.delete(0, "end")
        entry4.delete(0, "end")
        entry1.focus()

    def update_book():
        not_in_db = True
        # get data from entry boxes
        new_title = entry1.get()
        new_author = entry2.get()
        new_year = entry3.get()
        new_isbn = entry4.get()
        e_list = [new_title, new_author, new_year, new_isbn]

        for entry in e_list:
            if len(entry) == 0:
                messagebox.showinfo("Erro", "Preencha todas as caixas de entrada!")
                return

        for n in range(2, 4):
            if e_list[n].isalpha():
                messagebox.showinfo("Erro", "Use apenas números para Ano/ISBN!")
                return

        selected = tree.focus()
        selected_values = tree.item(selected)["values"]

        e_dict = {"title": new_title,
                  "author": new_author,
                  "year": int(new_year),
                  "isbn": int(new_isbn)
                  }

        for i in range(len(data)):
            if data[i] == e_dict:
                not_in_db = False

        if not_in_db:
            for i in data:
                if list(i.values()) == selected_values:
                    i["title"] = new_title
                    i["author"] = new_author
                    i["year"] = int(new_year)
                    i["isbn"] = int(new_isbn)

            dump_data()
            tree.item(selected, text="", values=(new_title, new_author, new_year, new_isbn))
            clear_entries()
            messagebox.showinfo("", "Livro editado com sucesso!")
        else:
            messagebox.showinfo("Erro", "Esse livro já está na lista!")

    def delete_book():
        cur_items = tree.selection()  # store selected item(s) in a tuple
        for cur_item in cur_items:  # loops through the tuple
            # print(cur_item)
            for i in range(len(data)):  # loops through the list of books
                if list(data[i].values()) == tree.item(cur_item)["values"]:  # if book selected equals to book looped
                    data.pop(i)
                    # print(f"length: {len(data)}")
                    break
            tree.delete(cur_item)  # deletes item from tree
        messagebox.showinfo("", "Livro(s) deletado(s) com sucesso!")
        dump_data()  # saves new list on json file

    global root
    root = tkinter.Toplevel()  # starts window
    root.title("BookSearch")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map("Treeview", background=[("selected", "#347083")])

    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    tree = ttk.Treeview(tree_frame,
                        show="headings",
                        yscrollcommand=tree_scroll.set,
                        selectmode="extended")
    tree.pack()

    tree_scroll.config(command=tree.yview)

    tree['columns'] = ("Title", "Author", "Year", "ISBN")

    # tree.column("#0", width=0, stretch=NO)
    tree.column("Title", anchor=W, width=300)
    tree.column("Author", anchor=W, width=175)
    tree.column("Year", anchor=CENTER, width=60, minwidth=40)
    tree.column("ISBN", anchor=W, width=175)

    tree.heading("Title", text="Título", anchor=W)
    tree.heading("Author", text="Autor", anchor=W)
    tree.heading("Year", text="Ano", anchor=CENTER)
    tree.heading("ISBN", text="ISBN", anchor=CENTER)

    # Populate the Treeview with books from the list
    for item in data:
        tree.insert(parent='', index='end', text="", values=(item["title"],
                                                             item["author"],
                                                             item["year"],
                                                             item["isbn"]))

    # Entry frame
    entry_frame = LabelFrame(root, text="Dados de entrada")
    entry_frame.pack(fill="x", expand=1, padx=20)

    # Labels and entry boxes
    label1 = Label(entry_frame, text="Título")
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = Entry(entry_frame)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    label2 = Label(entry_frame, text="Autor")
    label2.grid(row=0, column=2, padx=10, pady=10)
    entry2 = Entry(entry_frame)
    entry2.grid(row=0, column=3, padx=10, pady=10)
    label3 = Label(entry_frame, text="Ano")
    label3.grid(row=0, column=4, padx=10, pady=10)
    entry3 = Entry(entry_frame)
    entry3.grid(row=0, column=5, padx=10, pady=10)
    label4 = Label(entry_frame, text="ISBN")
    label4.grid(row=0, column=6, padx=10, pady=10)
    entry4 = Entry(entry_frame)
    entry4.grid(row=0, column=7, padx=10, pady=10)

    # Button frame
    button_frame = LabelFrame(root, text="Ações")
    button_frame.pack(fill="x", expand=1, padx=20, pady=10)

    # Buttons
    button1 = tkinter.Button(button_frame, text="Mostrar tudo", command=show_all)
    button1.grid(row=0, column=0, padx=10, pady=10, ipadx=5)
    button2 = tkinter.Button(button_frame, text="Buscar livro", command=search_book)
    button2.grid(row=0, column=1, padx=10, pady=10, ipadx=5)
    button3 = tkinter.Button(button_frame, text="Adicionar livro", command=add_book)
    button3.grid(row=0, column=2, padx=10, pady=10, ipadx=5)
    button4 = tkinter.Button(button_frame, text="Limpar entradas", command=clear_entries)
    button4.grid(row=0, column=3, padx=10, pady=10, ipadx=5)
    button5 = tkinter.Button(button_frame, text="Atualizar seleção", command=update_book)
    button5.grid(row=0, column=4, padx=10, pady=10, ipadx=5)
    button6 = tkinter.Button(button_frame, text="Deletar seleção", command=delete_book)
    button6.grid(row=0, column=5, padx=10, pady=10, ipadx=5)
    button7 = tkinter.Button(button_frame, text="Sair", command=logout)
    button7.grid(row=0, column=6, padx=10, pady=10, ipadx=5)

    # Execute 'select_book' function upon clicking on an item in the list
    tree.bind("<ButtonRelease-1>", select_book)


def callback():
    webbrowser.open("www.google.com")


login = tkinter.Tk()
login.title("Login")
login.eval('tk::PlaceWindow . center')
login.geometry("300x300")

lg_frame = Frame(login)
lg_frame.place(relx=0.5, rely=0.5, anchor="center")
# lg_frame.pack(fill=BOTH, expand=1)

tl_label = Label(lg_frame, text="BookSearch", font=("Georgia", 24))
tl_label.grid(row=0, column=0, columnspan=2, pady=25, sticky=EW)

lg_label = Label(lg_frame, text="Usuário")
lg_label.grid(row=1, column=0, padx=10, pady=5)
ps_label = Label(lg_frame, text="Senha")
ps_label.grid(row=2, column=0, padx=10, pady=5)
rg_label = Label(lg_frame, text="Criar conta", fg="blue", cursor="hand2")
rg_label.grid(row=4, column=1)
rg_label.bind("<Button-1>", lambda e: callback())

lg_entry = Entry(lg_frame)
lg_entry.grid(row=1, column=1, columnspan=1, padx=10, pady=5)
ps_entry = Entry(lg_frame, show="*")
ps_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=5)

login_bt = Button(lg_frame, text="Entrar", width=10, command=lambda: validate(lg_entry.get(), ps_entry.get()))
login_bt.grid(row=3, column=1, padx=10, pady=5)

mainloop()
