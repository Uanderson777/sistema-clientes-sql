import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# BANCO DE DADOS
# =========================
conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    endereco TEXT NOT NULL
)
""")
conn.commit()

# =========================
# FUNÇÕES
# =========================
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)

def limpar_busca():
    entry_busca.delete(0, tk.END)
    carregar_clientes()

def carregar_clientes():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM clientes")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def cadastrar():
    if entry_nome.get() == "" or entry_email.get() == "" or entry_telefone.get() == "" or entry_endereco.get() == "":
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, endereco)
        VALUES (?, ?, ?, ?)
    """, (
        entry_nome.get(),
        entry_email.get(),
        entry_telefone.get(),
        entry_endereco.get()
    ))

    conn.commit()
    carregar_clientes()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

def deletar():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um cliente!")
        return

    dados = tree.item(selecionado, "values")

    cursor.execute("DELETE FROM clientes WHERE id=?", (dados[0],))
    conn.commit()

    carregar_clientes()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")

def selecionar(event):
    selecionado = tree.focus()
    if not selecionado:
        return

    dados = tree.item(selecionado, "values")

    limpar_campos()

    entry_nome.insert(0, dados[1])
    entry_email.insert(0, dados[2])
    entry_telefone.insert(0, dados[3])
    entry_endereco.insert(0, dados[4])

def atualizar():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um cliente!")
        return

    dados = tree.item(selecionado, "values")

    cursor.execute("""
        UPDATE clientes SET nome=?, email=?, telefone=?, endereco=?
        WHERE id=?
    """, (
        entry_nome.get(),
        entry_email.get(),
        entry_telefone.get(),
        entry_endereco.get(),
        dados[0]
    ))

    conn.commit()
    carregar_clientes()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

def buscar():
    termo = entry_busca.get()

    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("""
        SELECT * FROM clientes
        WHERE nome LIKE ?
    """, ('%' + termo + '%',))

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        messagebox.showinfo("Resultado", "Nenhum cliente encontrado!")

    for row in resultados:
        tree.insert("", tk.END, values=row)

# =========================
# INTERFACE
# =========================
janela = tk.Tk()
janela.title("Sistema de Clientes")
janela.geometry("900x550")

# FORMULÁRIO
frame_form = tk.Frame(janela)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nome").grid(row=0, column=0)
entry_nome = tk.Entry(frame_form, width=20)
entry_nome.grid(row=0, column=1)

tk.Label(frame_form, text="Email").grid(row=0, column=2)
entry_email = tk.Entry(frame_form, width=25)
entry_email.grid(row=0, column=3)

tk.Label(frame_form, text="Telefone").grid(row=1, column=0)
entry_telefone = tk.Entry(frame_form, width=20)
entry_telefone.grid(row=1, column=1)

tk.Label(frame_form, text="Endereço").grid(row=1, column=2)
entry_endereco = tk.Entry(frame_form, width=25)
entry_endereco.grid(row=1, column=3)

# BOTÕES
frame_btn = tk.Frame(janela)
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Cadastrar", width=15, command=cadastrar).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Atualizar", width=15, command=atualizar).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Deletar", width=15, command=deletar).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Limpar", width=15, command=limpar_campos).grid(row=0, column=3, padx=5)

# BUSCA
frame_busca = tk.Frame(janela)
frame_busca.pack(pady=10)

entry_busca = tk.Entry(frame_busca, width=30)
entry_busca.grid(row=0, column=0, padx=5)

tk.Button(frame_busca, text="Buscar", command=buscar).grid(row=0, column=1)
tk.Button(frame_busca, text="Limpar Busca", command=limpar_busca).grid(row=0, column=2)

# TABELA
tree = ttk.Treeview(janela, columns=("ID", "Nome", "Email", "Telefone", "Endereço"), show="headings")
tree.pack(fill="both", expand=True)

tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("Email", text="Email")
tree.heading("Telefone", text="Telefone")
tree.heading("Endereço", text="Endereço")

tree.bind("<ButtonRelease-1>", selecionar)

carregar_clientes()

janela.mainloop()

