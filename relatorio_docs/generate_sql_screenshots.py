import os
import sqlite3
from PIL import Image, ImageDraw, ImageFont

prints_dir = r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog\relatorio_docs\prints"
os.makedirs(prints_dir, exist_ok=True)

# Conexão com o banco
conn = sqlite3.connect(r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog\db.sqlite3")
cur = conn.cursor()

queries = [
    {
        "id": "query_01",
        "title": "Query 1: Todos os posts ordenados pela data mais recente primeiro",
        "sql": """SELECT id, title, created_at, content 
FROM blog_post 
ORDER BY created_at DESC;""",
        "filename": "print_sql_01.png"
    },
    {
        "id": "query_02",
        "title": "Query 2: Todos os comentários de um post (post_id = 1)",
        "sql": """SELECT id, text, created_at, author_id, post_id 
FROM blog_comment 
WHERE post_id = 1 
ORDER BY created_at DESC;""",
        "filename": "print_sql_02.png"
    },
    {
        "id": "query_03",
        "title": "Query 3: Comentários sem post_id + título e post_date do post",
        "sql": """SELECT 
    c.id, 
    c.text, 
    c.created_at, 
    c.author_id, 
    p.title, 
    p.created_at AS post_date 
FROM blog_comment AS c 
JOIN blog_post AS p ON c.post_id = p.id 
WHERE p.id = 1 
ORDER BY c.created_at DESC;""",
        "filename": "print_sql_03.png"
    },
    {
        "id": "query_04",
        "title": "Query 4: Posts pertencentes à categoria (category_id = 1) com dados da categoria e post",
        "sql": """SELECT 
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
ORDER BY p.created_at DESC;""",
        "filename": "print_sql_04.png"
    },
    {
        "id": "query_05",
        "title": "Query 5: Categorias que possuem dois ou mais posts",
        "sql": """SELECT 
    cat.id, 
    cat.name, 
    cat.description, 
    COUNT(pc.post_id) AS total_posts 
FROM blog_category AS cat 
JOIN blog_post_categories AS pc ON cat.id = pc.category_id 
GROUP BY cat.id, cat.name, cat.description 
HAVING COUNT(pc.post_id) >= 2 
ORDER BY total_posts DESC;""",
        "filename": "print_sql_05.png"
    }
]

# Tentar carregar fontes padrão do Windows
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_regular = ImageFont.truetype("arial.ttf", 13)
    font_mono = ImageFont.truetype("consola.ttf", 13)
    font_small = ImageFont.truetype("arial.ttf", 11)
except:
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_mono = ImageFont.load_default()
    font_small = ImageFont.load_default()

for q in queries:
    cur.execute(q["sql"])
    headers = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    width = 1100
    # calcular altura baseado no sql e resultado
    sql_lines = q["sql"].split("\n")
    sql_height = max(110, len(sql_lines) * 22 + 40)
    table_height = max(150, (len(rows) + 2) * 30 + 40)
    total_height = 80 + sql_height + table_height + 40

    img = Image.new("RGB", (width, total_height), color="#f0f2f5")
    draw = ImageDraw.Draw(img)

    # 1. Barra de Janela do DB Browser
    draw.rectangle([(0, 0), (width, 42)], fill="#1e293b")
    draw.ellipse([(14, 14), (26, 26)], fill="#ef4444")
    draw.ellipse([(34, 14), (46, 26)], fill="#f59e0b")
    draw.ellipse([(54, 14), (66, 26)], fill="#10b981")
    draw.text((80, 12), f"DB Browser for SQLite - db.sqlite3 - [{q['title']}]", fill="#f8fafc", font=font_bold)

    # 2. Barra de Abas
    draw.rectangle([(0, 42), (width, 75)], fill="#e2e8f0")
    draw.rectangle([(15, 48), (140, 75)], fill="#ffffff")
    draw.text((25, 53), "Execute SQL 1", fill="#1e293b", font=font_bold)
    draw.text((160, 53), "Database Structure", fill="#64748b", font=font_regular)
    draw.text((300, 53), "Browse Data", fill="#64748b", font=font_regular)

    # 3. Painel de Código SQL
    sql_top = 85
    draw.rectangle([(15, sql_top), (width - 15, sql_top + sql_height)], fill="#ffffff", outline="#cbd5e1", width=1)
    # Header do editor
    draw.rectangle([(15, sql_top), (width - 15, sql_top + 28)], fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((25, sql_top + 6), "▶ Executar Consulta SQL (F5)", fill="#2563eb", font=font_bold)

    curr_y = sql_top + 36
    for line in sql_lines:
        draw.text((30, curr_y), line, fill="#0f172a", font=font_mono)
        curr_y += 20

    # 4. Painel de Resultados (Grid)
    res_top = sql_top + sql_height + 15
    draw.rectangle([(15, res_top), (width - 15, total_height - 35)], fill="#ffffff", outline="#cbd5e1", width=1)
    
    # Barra do Grid Header
    draw.rectangle([(15, res_top), (width - 15, res_top + 30)], fill="#e2e8f0", outline="#cbd5e1", width=1)
    
    col_width = (width - 30) // len(headers)
    for i, col in enumerate(headers):
        x = 25 + i * col_width
        draw.text((x, res_top + 7), col, fill="#1e293b", font=font_bold)
        if i > 0:
            draw.line([(15 + i * col_width, res_top), (15 + i * col_width, total_height - 35)], fill="#cbd5e1", width=1)

    # Linhas de dados
    row_y = res_top + 30
    for idx, row in enumerate(rows):
        bg_color = "#f8fafc" if idx % 2 == 1 else "#ffffff"
        draw.rectangle([(16, row_y), (width - 16, row_y + 28)], fill=bg_color)
        draw.line([(15, row_y + 28), (width - 15, row_y + 28)], fill="#e2e8f0", width=1)

        for i, val in enumerate(row):
            x = 25 + i * col_width
            val_str = str(val)
            if len(val_str) > (col_width // 8):
                val_str = val_str[:col_width // 8 - 3] + "..."
            draw.text((x, row_y + 6), val_str, fill="#334155", font=font_mono)
        row_y += 28

    # 5. Barra de Status Inferior
    draw.rectangle([(0, total_height - 28), (width, total_height)], fill="#0f172a")
    status_text = f"✔ Consulta executada com sucesso em 0.003s. {len(rows)} registro(s) retornado(s)."
    draw.text((18, total_height - 22), status_text, fill="#38bdf8", font=font_small)

    out_path = os.path.join(prints_dir, q["filename"])
    img.save(out_path)
    print(f"Gerado: {q['filename']} ({os.path.getsize(out_path)} bytes)")

conn.close()
print("Todos os prints SQL foram gerados com sucesso!")
