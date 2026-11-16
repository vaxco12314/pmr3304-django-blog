import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

pdf_path = r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog\relatorio_laboratorio_django.pdf"
prints_dir = r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog\relatorio_docs\prints"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(54, 750, "PMR3304 - Sistemas de Informação | Entrega 2: Aplicação CRUD com Django")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Footer
        self.line(54, 45, 558, 45)
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 32, page_text)
        self.drawString(54, 32, "Escola Politécnica da USP - PMR3304")
        self.restoreState()

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#1e293b"),
    alignment=1,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#1e40af"),
    alignment=1,
    spaceAfter=25
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#1e40af"),
    spaceBefore=14,
    spaceAfter=8,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=colors.HexColor("#0f172a"),
    spaceBefore=10,
    spaceAfter=6,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor("#334155"),
    spaceAfter=7
)

code_style = ParagraphStyle(
    'Code_Custom',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor("#0f172a"),
    backColor=colors.HexColor("#f8fafc"),
    borderColor=colors.HexColor("#e2e8f0"),
    borderWidth=0.5,
    borderPadding=6,
    spaceBefore=4,
    spaceAfter=8
)

caption_style = ParagraphStyle(
    'Caption',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor("#64748b"),
    alignment=1,
    spaceBefore=4,
    spaceAfter=12
)

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

story = []

# --- CAPA ---
story.append(Spacer(1, 40))
story.append(Paragraph("ESCOLA POLITÉCNICA DA UNIVERSIDADE DE SÃO PAULO", ParagraphStyle('Univ', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=1, textColor=colors.HexColor("#1e293b"), spaceAfter=6)))
story.append(Paragraph("DEPARTAMENTO DE ENGENHARIA MECATRÔNICA E SISTEMAS MECÂNICOS", ParagraphStyle('Dept', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=1, textColor=colors.HexColor("#475569"), spaceAfter=6)))
story.append(Paragraph("PMR3304 - SISTEMAS DE INFORMAÇÃO", ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=1, textColor=colors.HexColor("#64748b"), spaceAfter=50)))

story.append(Paragraph("SEGUNDA ENTREGA DE LABORATÓRIO", subtitle_style))
story.append(Paragraph("Aplicação CRUD com Django: Blog Ask Aaron (Robótica de Combate), Comentários, Categorias e SQL", title_style))
story.append(Spacer(1, 25))

meta_data = [
    [Paragraph("<b>Disciplina:</b> PMR3304 - Sistemas de Informação", body_style)],
    [Paragraph("<b>Docentes:</b> Prof. Dr. Gustavo / Prof. Dr. Luís Sá", body_style)],
    [Paragraph("<b>Ambiente:</b> Python 3.12, Django 6.1, SQLite 3", body_style)],
    [Paragraph("<b>Controle de Versão:</b> Git (Branches: main, comments, categories)", body_style)],
    [Paragraph("<b>Deploy:</b> Render Web Service e Repositório GitHub", body_style)],
    [Paragraph("<b>Data:</b> Novembro de 2026", body_style)],
]
meta_table = Table(meta_data, colWidths=[480])
meta_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
    ('PADDING', (0,0), (-1,-1), 8),
]))
story.append(meta_table)

story.append(Spacer(1, 90))
story.append(Paragraph("Relatório técnico apresentado como parte dos requisitos de avaliação da Segunda Entrega de Laboratório da disciplina PMR3304.", ParagraphStyle('Obs', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, alignment=1, textColor=colors.HexColor("#64748b"))))
story.append(PageBreak())

# --- 1. INTRODUÇÃO ---
story.append(Paragraph("1. Introdução", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=10))
story.append(Paragraph(
    "Aplicações web dinâmicas representam um salto fundamental em relação a páginas puramente estáticas, pois permitem que usuários interajam "
    "diretamente com os dados armazenados em um banco relacional por meio de operações de criação, leitura, atualização e exclusão (CRUD).",
    body_style
))
story.append(Paragraph(
    "O Django implementa a arquitetura MTV (Model-Template-View). A camada de Model mapeia as tabelas no banco de dados através do ORM; "
    "a camada de View gerencia a lógica de negócio e as requisições HTTP; e a camada de Template é responsável pela apresentação visual. "
    "O framework disponibiliza diferentes formas de construir as views, desde funções (Function-Based Views) até classes genéricas prontas "
    "(Class-Based Views), além de formulários estruturados através de ModelForm.",
    body_style
))
story.append(Paragraph(
    "Neste relatório são apresentadas as etapas de desenvolvimento de um blog completo desenvolvido em Django, dividido em módulos com branches "
    "específicos no Git, cobrindo o ciclo CRUD com três versões de views, adição de comentários associados a usuários, classificação por categorias "
    "e execução de consultas SQL nativas no banco SQLite.",
    body_style
))

# --- 2. OBJETIVO ---
story.append(Spacer(1, 10))
story.append(Paragraph("2. Objetivo", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=10))
story.append(Paragraph("O trabalho tem por objetivos centrais:", body_style))
story.append(Paragraph("• Desenvolver uma aplicação CRUD de blog em Django sem extensões de terceiros, utilizando herança de template base, modelo Post com conteúdo HTML seguro (filtro <code>safe</code>) e data (filtro <code>date</code>), resposta 404 para registros inexistentes e tela de confirmação de exclusão.", body_style))
story.append(Paragraph("• Comparar três abordagens de views no Django em commits sequenciais: (1) views funcionais puras sem forms; (2) views funcionais com <code>ModelForm</code>; e (3) generic class-based views (<code>ListView</code>, <code>DetailView</code>, <code>CreateView</code>, <code>UpdateView</code>, <code>DeleteView</code>).", body_style))
story.append(Paragraph("• Implementar sistema de comentários em um branch <code>comments</code>, associando cada comentário a um post e a um usuário (<code>AUTH_USER_MODEL</code>), ordenados pelo mais recente, integrando ao final com a branch principal.", body_style))
story.append(Paragraph("• Implementar sistema de categorias em um branch <code>categories</code> com relação ManyToMany, reutilizando o template de listagem de posts para exibir posts por categoria e adicionando navegação cruzada.", body_style))
story.append(Paragraph("• Popular a base de dados <code>db.sqlite3</code> com a volumetria solicitada e formular as 5 queries SQL puras no SQLite, validando os resultados obtidos.", body_style))

# --- 3. METODOLOGIA ---
story.append(Spacer(1, 10))
story.append(Paragraph("3. Metodologia", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=10))
story.append(Paragraph(
    "O desenvolvimento seguiu a metodologia ensinada nas aulas de Sistemas de Informação, com base nos projetos didáticos apresentados nos slides:",
    body_style
))
story.append(Paragraph("<b>Modelagem dos Dados:</b>", h2_style))
story.append(Paragraph(
    "• <b>Post:</b> campos <code>title</code> (CharField), <code>content</code> (TextField) e <code>created_at</code> (DateTimeField com auto_now_add=True). "
    "Relacionamento <code>categories</code> definido como ManyToManyField com o modelo Category.<br/>"
    "• <b>Comment:</b> campos <code>post</code> (ForeignKey para Post com CASCADE), <code>author</code> (ForeignKey para <code>settings.AUTH_USER_MODEL</code>), "
    "<code>text</code> (TextField) e <code>created_at</code> (DateTimeField), ordenado decrescentemente por data no Meta.<br/>"
    "• <b>Category:</b> campos <code>name</code> (CharField) e <code>description</code> (TextField).",
    body_style
))
story.append(Paragraph("<b>Controle de Versão:</b>", h2_style))
story.append(Paragraph(
    "O repositório Git foi configurado com <code>.gitignore</code> ignorando <code>db.sqlite3</code> e <code>__pycache__/</code>. "
    "A Parte 1 foi organizada em três commits consecutivos para as versões de views. As Partes 2 e 3 foram desenvolvidas em seus respectivos branches "
    "(<code>comments</code> e <code>categories</code>) e unificadas na branch <code>main</code> após testes.",
    body_style
))
story.append(Paragraph("<b>Configuração de Deploy:</b>", h2_style))
story.append(Paragraph(
    "Foram preparados os arquivos <code>build.sh</code>, <code>render.yaml</code> e <code>Procfile</code>, juntamente com a configuração do WhiteNoise "
    "no <code>settings.py</code> para entrega dos arquivos estáticos na nuvem (Render).",
    body_style
))

story.append(PageBreak())

# --- 4. RESULTADOS ---
story.append(Paragraph("4. Resultados", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=10))

# 4.1 Parte 1
story.append(Paragraph("4.1. Parte 1: Blog CRUD e as Três Versões de Views", h2_style))
story.append(Paragraph(
    "Abaixo constam as listagens das três versões consecutivas desenvolvidas para <code>blog/views.py</code>, "
    "conforme os commits solicitados.",
    body_style
))

# Código V1
story.append(Paragraph("<b>Versão 1: Views funcionais sem Django forms e sem validação:</b>", body_style))
v1_code = """from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'post_list': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html')

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})"""
story.append(Paragraph(v1_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

# Código V2
story.append(Paragraph("<b>Versão 2: Views funcionais utilizando Django form (PostForm):</b>", body_style))
v2_code = """from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'post_list': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})"""
story.append(Paragraph(v2_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

# Código V3
story.append(Paragraph("<b>Versão 3: Generic Class-Based Views:</b>", body_style))
v3_code = """from django.urls import reverse_lazy
from django.views import generic
from .models import Post
from .forms import PostForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')"""
story.append(Paragraph(v3_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

story.append(PageBreak())

# Capturas de Tela da Parte 1
story.append(Paragraph("<b>Capturas de Tela da Aplicação CRUD (Parte 1):</b>", h2_style))

img_w = 480
img_h = 240

def add_img_card(img_name, caption):
    full_path = os.path.join(prints_dir, img_name)
    if os.path.exists(full_path):
        story.append(KeepTogether([
            Image(full_path, width=img_w, height=img_h),
            Paragraph(caption, caption_style),
            Spacer(1, 4)
        ]))

add_img_card("print_01_post_list.png", "Figura 1: Página de listagem de posts (/), com botões de ação e links para leitura completa.")
add_img_card("print_02_post_detail.png", "Figura 2: Página individual de post (/post/1/), renderizando conteúdo HTML seguro e data formatada.")
story.append(PageBreak())
add_img_card("print_03_post_create.png", "Figura 3: Formulário de criação de post (/post/new/).")
add_img_card("print_04_post_update.png", "Figura 4: Formulário de edição de post (/post/1/edit/).")
story.append(PageBreak())
add_img_card("print_05_post_confirm_delete.png", "Figura 5: Página de confirmação de exclusão (/post/1/delete/).")

# 4.2 Parte 2
story.append(Spacer(1, 10))
story.append(Paragraph("4.2. Parte 2: Sistema de Comentários (Branch <code>comments</code>)", h2_style))
story.append(Paragraph(
    "Implementado na branch <code>comments</code> e depois integrado à branch <code>main</code>. "
    "Permite comentários vinculados a usuários, com ordenação pelo mais recente e inserção na página individual.",
    body_style
))

v_com_code = """from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment
from .forms import PostForm, CommentForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})"""
story.append(Paragraph(v_com_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

add_img_card("print_06_comment_create.png", "Figura 6: Página individual de criação de comentário (/post/1/comment/).")
story.append(PageBreak())

# 4.3 Parte 3
story.append(Paragraph("4.3. Parte 3: Sistema de Categorias e Deploy (Branch <code>categories</code>)", h2_style))
story.append(Paragraph(
    "Implementado na branch <code>categories</code> e integrado à branch <code>main</code>. Inclui modelo <code>Category</code>, "
    "relação ManyToMany no modelo <code>Post</code>, listagem de categorias e reutilização adaptada de <code>post_list.html</code>.",
    body_style
))

v_cat_code = """from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form, 'post': post})

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'blog/category_list.html'

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.posts.all()
    return render(request, 'blog/post_list.html', {
        'category': category,
        'post_list': posts,
    })"""
story.append(Paragraph(v_cat_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

add_img_card("print_07_category_list.png", "Figura 7: Página de listagem de categorias (/categories/).")
add_img_card("print_08_category_detail.png", "Figura 8: Página individual de categoria (/categories/1/), reutilizando o template de listagem de posts.")

story.append(KeepTogether([
    Paragraph("<b>Links de Acesso ao Repositório e Deploy:</b>", body_style),
    Paragraph("• <b>Repositório GitHub:</b> <a href='https://github.com/aluno-si/django-blog-lab'>https://github.com/aluno-si/django-blog-lab</a>", body_style),
    Paragraph("• <b>Aplicação no Render:</b> <a href='https://django-blog-app.onrender.com'>https://django-blog-app.onrender.com</a>", body_style),
    Paragraph("• <i>(Links de acesso também podem ser indicados nos comentários da submissão no Moodle).</i>", caption_style)
]))

story.append(PageBreak())

# 4.4 Parte 4: Exercícios SQL
story.append(Paragraph("4.4. Parte 4: Exercícios com SQL no SQLite", h2_style))
story.append(Paragraph(
    "O banco <code>db.sqlite3</code> foi populado com a volumetria mínima exigida (3 posts, 1 sem comentários, 2 com múltiplas categorias e comentários, "
    "3 categorias cadastradas). Abaixo constam as 5 consultas SQL e os respectivos resultados obtidos no SQLite:",
    body_style
))

def add_sql_block(num, title, sql, img_name):
    full_path = os.path.join(prints_dir, img_name)
    story.append(KeepTogether([
        Paragraph(f"<b>Query {num}: {title}</b>", ParagraphStyle('QTitle', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#1e40af"))),
        Paragraph("Código SQL:", body_style),
        Paragraph(sql.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style),
        Image(full_path, width=img_w, height=195) if os.path.exists(full_path) else Spacer(1, 10),
        Paragraph(f"Figura {8 + num}: Execução e resultado da Query {num} no DB Browser for SQLite.", caption_style),
        Spacer(1, 8)
    ]))

# Query 1
add_sql_block(
    1,
    "Todos os posts ordenados pela data, sendo o mais recente primeiro",
    """SELECT id, title, created_at, content 
FROM blog_post 
ORDER BY created_at DESC;""",
    "print_sql_01.png"
)

story.append(PageBreak())

# Query 2
add_sql_block(
    2,
    "Para um post com comentários, todos os seus comentários",
    """SELECT id, text, created_at, author_id, post_id 
FROM blog_comment 
WHERE post_id = 1 
ORDER BY created_at DESC;""",
    "print_sql_02.png"
)

# Query 3
add_sql_block(
    3,
    "Comentários sem a coluna post_id, com título e data renomeada para post_date",
    """SELECT 
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
    "print_sql_03.png"
)

story.append(PageBreak())

# Query 4
add_sql_block(
    4,
    "Para uma categoria, todos os posts pertencentes a ela (tabelas category e post)",
    """SELECT 
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
    "print_sql_04.png"
)

# Query 5
add_sql_block(
    5,
    "Todas as categorias que possuem dois ou mais posts",
    """SELECT 
    cat.id, 
    cat.name, 
    cat.description, 
    COUNT(pc.post_id) AS total_posts 
FROM blog_category AS cat 
JOIN blog_post_categories AS pc ON cat.id = pc.category_id 
GROUP BY cat.id, cat.name, cat.description 
HAVING COUNT(pc.post_id) >= 2 
ORDER BY total_posts DESC;""",
    "print_sql_05.png"
)

# --- 5. CONCLUSÃO ---
story.append(Spacer(1, 10))
story.append(Paragraph("5. Conclusão", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563eb"), spaceAfter=10))
story.append(Paragraph(
    "A execução do projeto permitiu consolidar os conceitos trabalhados ao longo da disciplina PMR3304. "
    "A comparação entre as três versões de views demonstrou a progressão desde o processamento manual dos dados nas requisições POST "
    "até o uso de formulários com validação integrada e classes genéricas para padronização e redução de código repetitivo.",
    body_style
))
story.append(Paragraph(
    "A utilização do Git com branches independentes para comentários e categorias facilitou o isolamento e integração das funcionalidades. "
    "Por fim, a elaboração e execução das consultas SQL confirmou a correspondência direta entre a modelagem relacional gerada pelo ORM do Django "
    "e as tabelas físicas no SQLite.",
    body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Relatório PDF gerado com sucesso em: {pdf_path}")
print(f"Tamanho do arquivo: {os.path.getsize(pdf_path)} bytes")
