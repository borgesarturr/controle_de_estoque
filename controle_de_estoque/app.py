import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

id_produto = None


# FUNÇÃO CADASTRAR PRODUTO

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
    
    registrar_log(
    f"""
    PRODUTO CADASTRADO

    Nome: {nome}
    Quantidade: {quantidade}
    Preço: {preco}
    """
    )
    
    listar_produtos()

    limpar_campos()

# SELECIONAR PRODUTO

def selecionar_produto(event):

    global id_produto

    item_selecionado = tabela.selection()

    if item_selecionado:

        valores = tabela.item(
            item_selecionado,
            "values"
        )

        id_produto = valores[0]

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])

        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(0, valores[2])

        entry_preco.delete(0, tk.END)
        entry_preco.insert(0, valores[3])

    
# ATUALIZAR PRODUTO

def atualizar_produto():

    global id_produto

    if id_produto is None:

        messagebox.showwarning(
            "Atenção",
            "Selecione um produto."
        )

        return

    nome = entry_nome.get().strip()

    try:

        quantidade = int(
            entry_quantidade.get()
        )

        preco = float(
            entry_preco.get()
        )

    except ValueError:

        messagebox.showerror(
            "Erro",
            "Quantidade e preço devem ser números."
        )

        return

    conexao = sqlite3.connect(
        "estoque.db"
    )

    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE produtos
    SET nome = ?, quantidade = ?, preco = ?
    WHERE id = ?
    """, (
        nome,
        quantidade,
        preco,
        id_produto
    ))

    conexao.commit()

    conexao.close()

    messagebox.showinfo(
        "Sucesso",
        "Produto atualizado!"
    )

    listar_produtos()

    limpar_campos()

    id_produto = None
    
    registrar_log(
    f"""
    PRODUTO ATUALIZADO

    ID: {id_produto}
    Nome: {nome}
    Quantidade: {quantidade}
    Preço: {preco}
    """
    )

    listar_produtos()

    limpar_campos()

# EXCLUIR PRODUTOS

def excluir_produto():

    itens_selecionados = tabela.selection()

    if not itens_selecionados:

        messagebox.showwarning(
            "Atenção",
            "Selecione um ou mais produtos."
        )

        return

    confirmar = messagebox.askyesno(
        "Confirmar Exclusão",
        "Deseja realmente excluir os produtos selecionados?"
    )

    if confirmar:

        conexao = sqlite3.connect(
            "estoque.db"
        )

        cursor = conexao.cursor()

        for item in itens_selecionados:

            valores = tabela.item(
                item,
                "values"
            )
            
            nome_produto = valores[1]

            id_produto = valores[0]
            
            registrar_log(
         f"""
        PRODUTO EXCLUÍDO

        ID: {id_produto}
        Nome: {nome_produto}
        """
    )

            cursor.execute("""
            DELETE FROM produtos
            WHERE id = ?
            """, (id_produto,))

        conexao.commit()

        conexao.close()

        listar_produtos()

        limpar_campos()

# LIMPAR CAMPOS

def limpar_campos():

    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_preco.delete(0, tk.END)

# LISTAR PRODUTOS

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
    
# REGISTRAR LOG

def registrar_log(mensagem):

    data_hora = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    with open(
        "log_estoque.txt",
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            f"[{data_hora}]\n"
        )

        arquivo.write(
            f"{mensagem}\n"
        )

        arquivo.write(
            "-" * 40 + "\n"
        )    


# JANELA PRINCIPAL

janela = tk.Tk()

janela.title("Controle de Estoque")

janela.geometry("500x300")


# LABELS

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


# BOTÃO

botao_cadastrar = tk.Button(
    janela,
    text="Cadastrar Produto",
    command=cadastrar_produto
)

botao_cadastrar.pack(pady=20)

botao_atualizar = tk.Button(
    janela,
    text="Atualizar Produto",
    command=atualizar_produto
)

botao_atualizar.pack(pady=10)

botao_excluir = tk.Button(
    janela,
    text="Excluir Produto",
    command=excluir_produto
)

botao_excluir.pack(pady=10)


# TABELA

colunas = (
    "ID",
    "Nome",
    "Quantidade",
    "Preço"
)

tabela = ttk.Treeview(
    janela,
    columns=colunas,
    show="headings",
    selectmode="extended"
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
tabela.bind(
    "<<TreeviewSelect>>",
    selecionar_produto
)


listar_produtos()

janela.mainloop()

