import subprocess
import os
import time

prints_dir = r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog\relatorio_docs\prints"
os.makedirs(prints_dir, exist_ok=True)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

targets = [
    ("print_01_post_list.png", "http://127.0.0.1:8000/", "1200,850"),
    ("print_02_post_detail.png", "http://127.0.0.1:8000/post/1/", "1200,900"),
    ("print_03_post_create.png", "http://127.0.0.1:8000/post/new/", "1200,800"),
    ("print_04_post_update.png", "http://127.0.0.1:8000/post/1/edit/", "1200,800"),
    ("print_05_post_confirm_delete.png", "http://127.0.0.1:8000/post/1/delete/", "1200,700"),
    ("print_06_comment_create.png", "http://127.0.0.1:8000/post/1/comment/", "1200,750"),
    ("print_06b_post_comments.png", "http://127.0.0.1:8000/post/1/", "1200,1400"),
    ("print_07_category_list.png", "http://127.0.0.1:8000/categories/", "1200,750"),
    ("print_08_category_detail.png", "http://127.0.0.1:8000/categories/1/", "1200,850"),
]

for filename, url, size in targets:
    out_file = os.path.join(prints_dir, filename)
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={size}",
        f"--screenshot={out_file}",
        url
    ]
    print(f"Capturando {url} (size {size}) -> {filename}...")
    try:
        subprocess.run(cmd, timeout=15, check=True)
        print(f"Sucesso: {filename} ({os.path.getsize(out_file)} bytes)")
    except Exception as e:
        print(f"Erro capturando {url}: {e}")

print("Captura de páginas web finalizada!")
