import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------
# BANCO DE DADOS
# -------------------------
con = sqlite3.connect("clientes.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    cidade TEXT NOT NULL
)
""")

con.commit()

# -------------------------
# FUNÇÕES DO SISTEMA
# -------------------------
def adicionar_cliente():
    nome = entry_nome.get()
    email = entry_email.get()
    cidade = entry_cidade.get()

    if nome == "" or email == "" or cidade == "":
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    cur.execute("INSERT INTO clientes (nome, email, cidade) VALUES (?, ?, ?)",
                (nome, email, cidade))
    con.commit()

    carregar_clientes()

    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_cidade.delete(0, tk.END)

    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")

def carregar_clientes():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM clientes")
    for cliente in cur.fetchall():
        tree.insert("", tk.END, values=cliente)

def deletar_cliente():
    try:
        item = tree.selection()[0]
        cliente_id = tree.item(item, "values")[0]

        cur.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        con.commit()

        carregar_clientes()
        messagebox.showinfo("Sucesso", "Cliente deletado!")
    
    except:
        messagebox.showwarning("Erro", "Selecione um cliente para deletar.")

# -------------------------
# INTERFACE GRÁFICA
# -------------------------
root = tk.Tk()
root.title("Sistema de Clientes")
root.geometry("650x400")

label_titulo = tk.Label(root, text="Sistema de Gestão de Clientes", font=("Arial", 16, "bold"))
label_titulo.pack(pady=10)

frame_form = tk.Frame(root)
frame_form.pack()

tk.Label(frame_form, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(frame_form)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Email:").grid(row=1, column=0)
entry_email = tk.Entry(frame_form)
entry_email.grid(row=1, column=1)

tk.Label(frame_form, text="Cidade:").grid(row=2, column=0)
entry_cidade = tk.Entry(frame_form)
entry_cidade.grid(row=2, column=1)

btn_add = tk.Button(root, text="Adicionar Cliente", command=adicionar_cliente)
btn_add.pack(pady=5)

btn_del = tk.Button(root, text="Deletar Cliente Selecionado", command=deletar_cliente)
btn_del.pack(pady=5)

tree = ttk.Treeview(root, columns=("ID", "Nome", "Email", "Cidade"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Cidade", text="Cidade")
tree.pack(pady=10, fill="x")

carregar_clientes()

root.mainloop()
