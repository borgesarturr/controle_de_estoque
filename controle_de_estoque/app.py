import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# -------------------------------
# FUNÇÃO CADASTRAR PRODUTO
# -------------------------------

def cadastrar_produto():

    nome = entry_nome.get().strip()

    try:
        quantidade = int(entry_quantidade.get())
        preco = float(entry_preco.get())

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Quantidade e preço devem ser números."
        )
        return

    if nome == "":
        messagebox.showwarning(
            "Atenção",
            "Digite o nome do produto."
        )
        return

    conexao = sqlite3.connect("estoque.db")

    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, quantidade, preco)
    VALUES (?, ?, ?)
    """, (nome, quantidade, preco))

    conexao.commit()

    conexao.close()

    messagebox.showinfo(
        "Sucesso",
        "Produto cadastrado!"
    )

    listar_produtos()

    limpar_campos()


# -------------------------------
# LIMPAR CAMPOS
# -------------------------------

def limpar_campos():

    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

# -------------------------------
# LISTAR PRODUTOS
# -------------------------------

def listar_produtos():

    for item in tabela.get_children():
        tabela.delete(item)

    conexao = sqlite3.connect("estoque.db")

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT * FROM produtos
    """)

    produtos = cursor.fetchall()

    for produto in produtos:

        tabela.insert(
            "",
            tk.END,
            values=produto
        )

    conexao.close()    


# -------------------------------
# JANELA PRINCIPAL
# -------------------------------

janela = tk.Tk()

janela.title("Controle de Estoque")

janela.geometry("500x300")


# -------------------------------
# LABELS
# -------------------------------

label_nome = tk.Label(janela, text="Nome")

label_nome.pack()

entry_nome = tk.Entry(janela, width=40)

entry_nome.pack()


label_quantidade = tk.Label(
    janela,
    text="Quantidade"
)

label_quantidade.pack()

entry_quantidade = tk.Entry(
    janela,
    width=40
)

entry_quantidade.pack()


label_preco = tk.Label(
    janela,
    text="Preço"
)

label_preco.pack()

entry_preco = tk.Entry(
    janela,
    width=40
)

entry_preco.pack()


# -------------------------------
# BOTÃO
# -------------------------------

botao_cadastrar = tk.Button(
    janela,
    text="Cadastrar Produto",
    command=cadastrar_produto
)

botao_cadastrar.pack(pady=20)


# -------------------------------
# TABELA
# -------------------------------

colunas = (
    "ID",
    "Nome",
    "Quantidade",
    "Preço"
)

tabela = ttk.Treeview(
    janela,
    columns=colunas,
    show="headings"
)

for coluna in colunas:

    tabela.heading(
        coluna,
        text=coluna
    )

tabela.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

listar_produtos()

janela.mainloop()