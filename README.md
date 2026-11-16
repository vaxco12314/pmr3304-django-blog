# TechBlog - Segunda Entrega de Laboratório: Aplicação CRUD com Django

Aplicação web dinâmica desenvolvida com **Django** como requisito da **Segunda Entrega de Laboratório** da disciplina de **Sistemas de Informação**.

---

## 📋 Sumário de Funcionalidades

1. **Parte 1 - Blog CRUD de Postagens:**
   - Templates organizados com herança a partir de `/templates/base.html`.
   - Modelo `Post` com campos `title`, `content` (HTML renderizado com filtro `safe`) e `created_at` (DateTimeField renderizado com `date`).
   - Resposta HTTP 404 para posts inexistentes via `get_object_or_404`.
   - Página de confirmação prévia para exclusão de postagem.
   - Histórico Git documentando **três versões de views**:
     - *Versão 1:* Views funcionais puras sem Django forms.
     - *Versão 2:* Views funcionais com `forms.ModelForm`.
     - *Versão 3:* Class-Based Views genéricas (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).

2. **Parte 2 - Sistema de Comentários:**
   - Desenvolvido no branch `comments` e integrado à `main` via `git merge`.
   - Modelo `Comment` associado ao `Post` e referenciando o modelo de usuário do Django (`AUTH_USER_MODEL`).
   - Comentários exibidos na página individual ordenados do mais recente primeiro.
   - Permite comentar direto da página do post ou via view dedicada (`comment_create`).

3. **Parte 3 - Sistema de Categorias:**
   - Desenvolvido no branch `categories` e integrado à `main` via `git merge`.
   - Modelo `Category` com relação ManyToMany em `Post`.
   - Reutilização do template `post_list.html` na view individual de categoria.
   - Navegação cruzada no cabeçalho e badges de categorias nos posts.

4. **Parte 4 - Exercícios com SQL no SQLite (`db.sqlite3`):**
   - Base populada com volumetria exata solicitada.
   - 5 consultas analíticas formuladas em SQL puro com capturas de tela.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.10+
- Git

### 2. Passo a Passo
```bash
# 1. Ativar o ambiente virtual
venv\Scripts\activate   # No Windows

# 2. Instalar dependências (caso necessário)
pip install -r requirements.txt

# 3. Aplicar migrações
python manage.py migrate

# 4. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse no navegador: **`http://127.0.0.1:8000/`**

---

## 🔑 Usuários para Teste (Django Admin)

| Usuário | Senha | Função |
|---|---|---|
| `admin` | `admin123` | Superusuário / Acesso ao painel `/admin/` |
| `maria` | `senha123` | Usuária comum (autora de comentários) |
| `joao` | `senha123` | Usuário comum (autor de comentários) |
| `ana` | `senha123` | Usuária comum (autora de comentários) |

---

## 🗄️ Consultas SQL (Exercícios da Seção 4)

### Query 1: Todos os posts ordenados por data decrescente
```sql
SELECT id, title, created_at, content 
FROM blog_post 
ORDER BY created_at DESC;
```

### Query 2: Todos os comentários de um post (post_id = 1)
```sql
SELECT id, text, created_at, author_id, post_id 
FROM blog_comment 
WHERE post_id = 1 
ORDER BY created_at DESC;
```

### Query 3: Comentários sem post_id + título e data renomeada para post_date
```sql
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
```

### Query 4: Posts de uma categoria específica (category_id = 1)
```sql
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
```

### Query 5: Categorias com dois ou mais posts
```sql
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
```

---

## 📦 Arquivos Gerados para Entrega no Moodle

1. **`relatorio_laboratorio_django.pdf`**: Relatório acadêmico completo com seções de Introdução, Objetivo, Metodologia e Resultados (contendo as listagens das 3 versões das views e todos os 13 screenshots).
2. **`db.sqlite3`**: Banco de dados populado com os dados utilizados nas consultas SQL.
