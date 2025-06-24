import tkinter as tk
from tkinter import ttk, messagebox
from produto import adicionar_produto, listar_produtos, remover_produto

def atualizar_lista(tree):
    for item in tree.get_children():
        tree.delete(item)
    for produto in listar_produtos():
        tree.insert("", "end", values=produto)

def adicionar(tree, nome, quantidade, preco, validade):
    if nome and quantidade and preco and validade:
        try:
            adicionar_produto(nome, int(quantidade), float(preco), validade)
            atualizar_lista(tree)
            messagebox.showinfo("Sucesso", "Produto adicionado!")
        except:
            messagebox.showerror("Erro", "Verifique os dados.")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

def remover(tree):
    selecionado = tree.selection()
    if selecionado:
        item = tree.item(selecionado)
        produto_id = item['values'][0]
        remover_produto(produto_id)
        atualizar_lista(tree)
    else:
        messagebox.showwarning("Atenção", "Selecione um produto para remover.")

def criar_interface():
    janela = tk.Tk()
    janela.title("Sistema de Estoque")
    janela.geometry("700x400")

    # Campos de entrada
    tk.Label(janela, text="Nome").grid(row=0, column=0)
    nome_entry = tk.Entry(janela)
    nome_entry.grid(row=0, column=1)

    tk.Label(janela, text="Quantidade").grid(row=1, column=0)
    qtd_entry = tk.Entry(janela)
    qtd_entry.grid(row=1, column=1)

    tk.Label(janela, text="Preço").grid(row=2, column=0)
    preco_entry = tk.Entry(janela)
    preco_entry.grid(row=2, column=1)

    tk.Label(janela, text="Validade (AAAA-MM-DD)").grid(row=3, column=0)
    validade_entry = tk.Entry(janela)
    validade_entry.grid(row=3, column=1)

    # Botão de adicionar
    add_btn = tk.Button(janela, text="Adicionar Produto", command=lambda: adicionar(
        tree, nome_entry.get(), qtd_entry.get(), preco_entry.get(), validade_entry.get()
    ))
    add_btn.grid(row=4, column=1, pady=10)

    # Tabela
    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Quantidade", "Preço", "Validade"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.grid(row=5, column=0, columnspan=4)

    atualizar_lista(tree)

    # Botão de remover
    rmv_btn = tk.Button(janela, text="Remover Selecionado", command=lambda: remover(tree))
    rmv_btn.grid(row=6, column=1, pady=10)

    janela.mainloop()
