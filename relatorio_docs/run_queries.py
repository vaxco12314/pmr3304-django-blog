import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

print("=== ESQUEMA DAS TABELAS BLOG ===")
cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name LIKE 'blog_%'")
for name, sql in cur.fetchall():
    print(f"\n--- Tabela: {name} ---")
    print(sql)

print("\n" + "="*50)
print("EXECUÇÃO DAS 5 QUERIES DO EXERCÍCIO SQL")
print("="*50)

# Query 1: Todos os posts, ordenados pela data, sendo o mais recente primeiro
q1 = """
SELECT id, title, created_at, content 
FROM blog_post 
ORDER BY created_at DESC;
"""
print("\n--- QUERY 1: Todos os posts ordenados pela data decrescente ---")
print("SQL:")
print(q1.strip())
print("\nResultado:")
cur.execute(q1)
cols1 = [d[0] for d in cur.description]
rows1 = cur.fetchall()
print(f"{'ID':<4} | {'Título':<40} | {'Data':<25}")
print("-" * 75)
for r in rows1:
    print(f"{r[0]:<4} | {r[1][:38]:<40} | {r[2]:<25}")

# Query 2: Para um post com comentários, todos os seus comentários
# Usando o post de ID 1 (ou título 'Introdução ao Desenvolvimento com Django e Arquitetura MTV')
q2 = """
SELECT c.id, c.text, c.created_at, c.author_id, c.post_id 
FROM blog_comment AS c 
WHERE c.post_id = 1 
ORDER BY c.created_at DESC;
"""
print("\n--- QUERY 2: Comentários de um post específico (post_id = 1) ---")
print("SQL:")
print(q2.strip())
print("\nResultado:")
cur.execute(q2)
rows2 = cur.fetchall()
print(f"{'ID':<4} | {'Autor ID':<10} | {'Post ID':<8} | {'Comentário':<40}")
print("-" * 70)
for r in rows2:
    print(f"{r[0]:<4} | {r[3]:<10} | {r[4]:<8} | {r[1][:38]:<40}")

# Query 3: Para um post com comentários, todos os seus comentários, incluindo todas as colunas da tabela comentários (exceto o post_id), o título do post e sua data de publicação, renomeada para post_date
q3 = """
SELECT 
    c.id, 
    c.text, 
    c.created_at, 
    c.author_id, 
    p.title, 
    p.created_at AS post_date 
FROM blog_comment AS c 
JOIN blog_post AS p ON c.post_id = p.id 
WHERE p.id = 1 
ORDER BY c.created_at DESC;
"""
print("\n--- QUERY 3: Comentários sem post_id + título do post + post_date ---")
print("SQL:")
print(q3.strip())
print("\nResultado:")
cur.execute(q3)
rows3 = cur.fetchall()
print(f"{'ID':<4} | {'Autor ID':<10} | {'Título do Post':<35} | {'post_date':<22} | {'Texto':<30}")
print("-" * 110)
for r in rows3:
    print(f"{r[0]:<4} | {r[3]:<10} | {r[4][:33]:<35} | {r[5]:<22} | {r[1][:28]:<30}")

# Query 4: Para uma categoria, todos os posts pertencentes a ela, incluindo as colunas da tabela de categoria e da tabela de posts
# Usando categoria_id = 1 ('Desenvolvimento Web')
q4 = """
SELECT 
    cat.id AS category_id, 
    cat.name AS category_name, 
    cat.description AS category_description, 
    p.id AS post_id, 
    p.title AS post_title, 
    p.content AS post_content, 
    p.created_at AS post_created_at 
FROM blog_category AS cat 
JOIN blog_post_categories AS pc ON cat.id = pc.category_id 
JOIN blog_post AS p ON pc.post_id = p.id 
WHERE cat.id = 1 
ORDER BY p.created_at DESC;
"""
print("\n--- QUERY 4: Posts de uma categoria específica (incluindo colunas da categoria e do post) ---")
print("SQL:")
print(q4.strip())
print("\nResultado:")
cur.execute(q4)
rows4 = cur.fetchall()
print(f"{'Cat ID':<7} | {'Categoria':<22} | {'Post ID':<8} | {'Título do Post':<40}")
print("-" * 85)
for r in rows4:
    print(f"{r[0]:<7} | {r[1]:<22} | {r[3]:<8} | {r[4][:38]:<40}")

# Query 5: Todas as categorias que possuem dois ou mais posts
q5 = """
SELECT 
    cat.id, 
    cat.name, 
    cat.description, 
    COUNT(pc.post_id) AS total_posts 
FROM blog_category AS cat 
JOIN blog_post_categories AS pc ON cat.id = pc.category_id 
GROUP BY cat.id, cat.name, cat.description 
HAVING COUNT(pc.post_id) >= 2 
ORDER BY total_posts DESC;
"""
print("\n--- QUERY 5: Categorias que possuem dois ou mais posts ---")
print("SQL:")
print(q5.strip())
print("\nResultado:")
cur.execute(q5)
rows5 = cur.fetchall()
print(f"{'ID':<4} | {'Categoria':<25} | {'Total de Posts':<15}")
print("-" * 50)
for r in rows5:
    print(f"{r[0]:<4} | {r[1]:<25} | {r[3]:<15}")

conn.close()
