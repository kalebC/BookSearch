from tkinter import *
from tkinter import ttk, messagebox
import backend


class LoginScreen(Tk):
    def __init__(self):
        super().__init__()

        self.title("Janela de login")
        self.geometry("400x300")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.frame = Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label = Label(self.frame, text="BookSearch", font=("Georgia", 24))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.lg_label = Label(self.frame, text="Usuário:")
        self.lg_label.grid(row=1, column=0, padx=10, pady=5)

        self.lg_entry = Entry(self.frame)
        self.lg_entry.grid(row=1, column=1)

        self.ps_label = Label(self.frame, text="Senha:")
        self.ps_label.grid(row=2, column=0, padx=10, pady=5)

        self.ps_entry = Entry(self.frame, show="*")
        self.ps_entry.grid(row=2, column=1)

        self.button = Button(self.frame, text="Entrar", width=8, command=lambda: validate(self.lg_entry.get(),
                                                                                          self.ps_entry.get()))
        self.button.grid(row=3, columnspan=2, padx=10, pady=5)

        rg_label = Label(self.frame, text="Criar conta", fg="blue", cursor="hand2")
        rg_label.grid(row=4, columnspan=2)
        rg_label.bind("<Button-1>", lambda e: backend.callback())

        def validate(username, password):
            if username == "admin" and password == "admin":
                messagebox.showinfo("", "Logado com sucesso!")
                self.withdraw()
                self.lg_entry.delete(0, END)
                self.ps_entry.delete(0, END)
                MainScreen()
            else:
                messagebox.showerror("Erro", "Login e/ou senha incorretos!")


class MainScreen(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("BookSearch")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview",
                             background="white",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#D3D3D3")
        self.style.map("Treeview", background=[("selected", "#347083")])

        self.tree_frame = Frame(self)
        self.tree_frame.pack(pady=10)

        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(self.tree_frame,
                                 show="headings",
                                 yscrollcommand=self.tree_scroll.set,
                                 selectmode="extended")
        self.tree.pack()

        self.tree_scroll.config(command=self.tree.yview)

        self.tree['columns'] = ("Title", "Author", "Year", "ISBN")

        self.tree.column("Title", anchor=W, width=300)
        self.tree.column("Author", anchor=W, width=175)
        self.tree.column("Year", anchor=CENTER, width=60, minwidth=40)
        self.tree.column("ISBN", anchor=CENTER, width=175)

        self.tree.heading("Title", text=" Título", anchor=W)
        self.tree.heading("Author", text=" Autor", anchor=W)
        self.tree.heading("Year", text="Ano", anchor=CENTER)
        self.tree.heading("ISBN", text="ISBN", anchor=CENTER)

        self.entry_frame = LabelFrame(self, text="Dados de entrada")
        self.entry_frame.pack(fill="x", expand=1, padx=20)

        # Labels and entry boxes
        self.label1 = Label(self.entry_frame, text="Título")
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.entry1 = Entry(self.entry_frame)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)
        self.label2 = Label(self.entry_frame, text="Autor")
        self.label2.grid(row=0, column=2, padx=10, pady=10)
        self.entry2 = Entry(self.entry_frame)
        self.entry2.grid(row=0, column=3, padx=10, pady=10)
        self.label3 = Label(self.entry_frame, text="Ano")
        self.label3.grid(row=0, column=4, padx=10, pady=10)
        self.entry3 = Entry(self.entry_frame)
        self.entry3.grid(row=0, column=5, padx=10, pady=10)
        self.label4 = Label(self.entry_frame, text="ISBN")
        self.label4.grid(row=0, column=6, padx=10, pady=10)
        self.entry4 = Entry(self.entry_frame)
        self.entry4.grid(row=0, column=7, padx=10, pady=10)

        # Button frame
        self.button_frame = LabelFrame(self, text="Ações")
        self.button_frame.pack(fill="x", expand=1, padx=20, pady=10)

        # Buttons
        self.button1 = Button(self.button_frame, text="Mostrar tudo", command=self.show_command)
        self.button1.grid(row=0, column=0, padx=10, pady=10, ipadx=5)
        self.button2 = Button(self.button_frame, text="Buscar livro", command=self.search_command)
        self.button2.grid(row=0, column=1, padx=10, pady=10, ipadx=5)
        self.button3 = Button(self.button_frame, text="Adicionar livro", command=self.add_command)
        self.button3.grid(row=0, column=2, padx=10, pady=10, ipadx=5)
        self.button4 = Button(self.button_frame, text="Limpar entradas", command=self.clear_command)
        self.button4.grid(row=0, column=3, padx=10, pady=10, ipadx=5)
        self.button5 = Button(self.button_frame, text="Atualizar seleção", command=self.update_command)
        self.button5.grid(row=0, column=4, padx=10, pady=10, ipadx=5)
        self.button6 = Button(self.button_frame, text="Deletar seleção", command=self.delete_command)
        self.button6.grid(row=0, column=5, padx=10, pady=10, ipadx=5)
        self.button7 = Button(self.button_frame, text="Sair", command=self.logout)
        self.button7.grid(row=0, column=6, padx=10, pady=10, ipadx=5)

        # Execute 'select_book' function upon clicking on an item in the list
        self.tree.bind("<ButtonRelease-1>", self.select_command)

        # Disable closing Toplevel window by clicking on X
        self.protocol("WM_DELETE_WINDOW", self.disable_event)

        self.show_command()  # Populate tree with books
        self.mainloop()

    def disable_event(self):
        pass

    def select_command(self, e):
        self.clear_command()
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        try:
            self.entry1.insert(0, values[0])
            self.entry2.insert(0, values[1])
            self.entry3.insert(0, values[2])
            self.entry4.insert(0, values[3])
        except IndexError:
            self.clear_command()

    def show_command(self):
        self.tree.delete(*self.tree.get_children())
        for row in backend.show():
            self.tree.insert(parent='', index='end', text="", values=(row[1], row[2], row[3], row[4]))

    def search_command(self):
        # Delete items on tree
        self.tree.delete(*self.tree.get_children())

        # List of entries
        search = [self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get()]
        tuple_results = backend.search(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
        results = []

        # Remove all empty strings from list
        search = list(filter(None, search))

        # Change numeric strings to integers
        for i in range(len(search)):
            if search[i].isnumeric():
                search[i] = int(search[i])

        tuple_search = tuple(search)

        # if items in search tuple are part of backend.search tuple, add to results list
        for i in tuple_results:
            if set(tuple_search).issubset(i):
                results.append(i)

        # insert results onto tree
        if len(results) > 0:
            for row in results:
                self.tree.insert(parent='', index='end', text="", values=(row[1],
                                                                          row[2],
                                                                          row[3],
                                                                          row[4]))
        else:
            messagebox.showinfo("Erro", "Sua busca retornou 0 resultados!")

    def add_command(self):
        not_in_db = True
        entries = [self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get()]

        for entry in entries:
            if len(entry) == 0:
                messagebox.showerror("Erro", "Preencha todas as caixas de entrada!")
                return

        for n in range(2, 4):
            if all(c.isdigit() for c in entries[n]):
                entries[n] = int(entries[n])
            else:
                messagebox.showerror("Erro", "Use apenas números para Ano/ISBN!")
                return

        entries = tuple(entries)

        for row in backend.show():
            tuple_row = (row[1], row[2], row[3], row[4])
            if entries == tuple_row:
                not_in_db = False
            elif entries[3] == row[4]:
                not_in_db = False

        if not_in_db:
            backend.add(entries[0], entries[1], entries[2], entries[3])
            self.tree.insert(parent='', index='end', text="", values=(entries[0],
                                                                      entries[1],
                                                                      entries[2],
                                                                      entries[3]))
            messagebox.showinfo("", "Livro adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Esse livro/ISBN já está cadastrado!")

    def clear_command(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry1.focus()

    def update_command(self):
        not_in_db = True
        entries = [self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get()]

        for entry in entries:
            if len(entry) == 0:
                messagebox.showerror("Erro", "Preencha todas as caixas de entrada!")
                return

        for n in range(2, 4):
            if all(c.isdigit() for c in entries[n]):
                entries[n] = int(entries[n])
            else:
                messagebox.showerror("Erro", "Use apenas números para Ano/ISBN!")
                return

        entries = tuple(entries)
        selected = self.tree.focus()

        for row in backend.show():
            tuple_row = (row[1], row[2], row[3], row[4])
            if entries == tuple_row:
                not_in_db = False
            elif entries[3] == row[4]:
                not_in_db = False

        if not_in_db:
            for row in backend.show():
                if row[1] == self.tree.item(selected)["values"][0] \
                        and row[2] == self.tree.item(selected)["values"][1] \
                        and row[3] == self.tree.item(selected)["values"][2] \
                        and row[4] == self.tree.item(selected)["values"][3]:
                    backend.update(row[0], entries[0], entries[1], entries[2], entries[3])
                    break
            self.tree.item(selected, text="", values=(entries[0], entries[1], entries[2], entries[3]))
        else:
            messagebox.showerror("Erro", "Esse livro/ISBN já está cadastrado!")

    def delete_command(self):
        selection = self.tree.selection()
        for item in selection:
            for row in backend.show():
                if row[1] == self.tree.item(item)["values"][0] \
                        and row[2] == self.tree.item(item)["values"][1] \
                        and row[3] == self.tree.item(item)["values"][2] \
                        and row[4] == self.tree.item(item)["values"][3]:
                    backend.delete(row[0])
            self.tree.delete(item)
        messagebox.showinfo("", "Livro(s) deletado(s) com sucesso!")

    def logout(self):
        self.destroy()
        app.deiconify()


app = LoginScreen()
app.mainloop()
