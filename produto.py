from database import conectar

def adicionar_produto(nome, quantidade, preco, validade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produto (nome, quantidade, preco, validade)
        VALUES (?, ?, ?, ?)
    """, (nome, quantidade, preco, validade))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produto")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def remover_produto(id_produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produto WHERE id = ?", (id_produto,))
    conn.commit()
    conn.close()
