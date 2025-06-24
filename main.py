import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

ARQUIVO_PRODUTOS = 'produtos.json'

# Funções para manipular produtos no JSON
def carregar_produtos():
    try:
        with open(ARQUIVO_PRODUTOS, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_produtos(produtos):
    with open(ARQUIVO_PRODUTOS, 'w') as f:
        json.dump(produtos, f, indent=4)

# Janela principal
class EstoqueApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Estoque")
        self.geometry("600x400")
        self.configure(bg='#ADD8E6')  # Azul claro

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#FFD700', foreground='black', font=('Arial', 11, 'bold'))
        self.style.map('TButton', background=[('active', '#FFC300')])

        self.create_widgets()

    def create_widgets(self):
        # Título com contorno preto e texto amarelo usando Canvas
        canvas = tk.Canvas(self, width=600, height=50, bg='#ADD8E6', highlightthickness=0)
        canvas.pack(pady=15)

        texto = "Sistema de Gestão de Estoque"
        x, y = 300, 25
        fonte = ("Arial", 20, "bold")
        cor_texto = "#FFD700"  # amarelo

        # Desenha o contorno (8 vezes em preto ao redor)
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            canvas.create_text(x+dx, y+dy, text=texto, font=fonte, fill='black')
        # Texto principal amarelo
        canvas.create_text(x, y, text=texto, font=fonte, fill=cor_texto)

        # Botões para ações
        btn_frame = tk.Frame(self, bg='#ADD8E6')
        btn_frame.pack(pady=20)

        btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar Produto", command=self.abrir_cadastro)
        btn_cadastrar.grid(row=0, column=0, padx=20)

        btn_consultar = ttk.Button(btn_frame, text="Consultar Produtos", command=self.abrir_consulta)
        btn_consultar.grid(row=0, column=1, padx=20)

    def abrir_cadastro(self):
        CadastroProduto(self)

    def abrir_consulta(self):
        ConsultaProdutos(self)

# Janela de cadastro de produtos
class CadastroProduto(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Cadastrar Produto")
        self.geometry("400x350")
        self.configure(bg='#ADD8E6')

        self.create_widgets()

    def create_widgets(self):
        labels = ["Nome", "Quantidade", "Preço (R$)", "Validade (dd/mm/aaaa)", "Fornecedor"]
        self.entries = {}

        for i, texto in enumerate(labels):
            label = tk.Label(self, text=texto, bg='#ADD8E6', fg='black', font=('Arial', 11))
            label.grid(row=i, column=0, sticky='w', padx=10, pady=8)

            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1, padx=10, pady=8)
            self.entries[texto] = entry

        btn_salvar = ttk.Button(self, text="Salvar Produto", command=self.salvar_produto)
        btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def salvar_produto(self):
        nome = self.entries["Nome"].get().strip()
        quantidade = self.entries["Quantidade"].get().strip()
        preco = self.entries["Preço (R$)"].get().strip()
        validade = self.entries["Validade (dd/mm/aaaa)"].get().strip()
        fornecedor = self.entries["Fornecedor"].get().strip()

        if not nome or not quantidade or not preco or not validade or not fornecedor:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            quantidade = int(quantidade)
            preco = float(preco)
            datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos. Verifique quantidade, preço e validade.")
            return

        produtos = carregar_produtos()
        if any(prod['nome'].lower() == nome.lower() for prod in produtos):
            messagebox.showwarning("Aviso", "Produto já cadastrado.")
            return

        novo_produto = {
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco,
            "validade": validade,
            "fornecedor": fornecedor
        }

        produtos.append(novo_produto)
        salvar_produtos(produtos)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        self.destroy()

# Janela de consulta de produtos
class ConsultaProdutos(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Consultar Produtos")
        self.geometry("600x400")
        self.configure(bg='#ADD8E6')

        self.create_widgets()
        self.carregar_lista()

    def create_widgets(self):
        colunas = ("Nome", "Quantidade", "Preço", "Validade", "Fornecedor")
        self.tree = ttk.Treeview(self, columns=colunas, show='headings')
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_atualizar = ttk.Button(self, text="Atualizar Lista", command=self.carregar_lista)
        btn_atualizar.pack(pady=5)

    def carregar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        produtos = carregar_produtos()
        for prod in produtos:
            self.tree.insert("", "end", values=(
                prod['nome'],
                prod['quantidade'],
                f"R$ {prod['preco']:.2f}",
                prod['validade'],
                prod['fornecedor']
            ))

if __name__ == "__main__":
    app = EstoqueApp()
    app.mainloop()
