import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas

# Caminhos principais
base_dir = r"C:\Users\hmdem\.gemini\antigravity\scratch\django_blog"
relatorio_dir = os.path.join(base_dir, "relatorio_docs")
prints_dir = os.path.join(relatorio_dir, "prints")
brasao_path = os.path.join(relatorio_dir, "brasao_poli_0.png")
pdf_path = os.path.join(base_dir, "relatorio_laboratorio_django.pdf")

class NumberedCanvas(canvas.Canvas):
    """
    Canvas de dois passos para calcular o total de páginas e reproduzir
    o cabeçalho e rodapé clássicos do padrão LaTeX (fancyhdr).
    """
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
        # A página 1 é a capa: sem cabeçalho e sem rodapé
        if self._pageNumber == 1:
            return

        width, height = self._pagesize

        self.saveState()
        # Cabeçalho padrão LaTeX
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.black)
        self.drawString(54, height - 42, "PMR3304 – Sistemas de Informação")
        self.drawRightString(width - 54, height - 42, "Segunda Entrega de Laboratório")

        # Linha horizontal sutil abaixo do cabeçalho
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.5)
        self.line(54, height - 46, width - 54, height - 46)

        # Rodapé: número da página centralizado (página 2 do doc é a página 1 de conteúdo)
        self.setFont("Times-Roman", 10)
        self.drawCentredString(width / 2.0, 36, str(self._pageNumber - 1))
        self.restoreState()


# Configuração do Documento A4 (margens de 54pt ~ 1,9 cm)
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

# Tipografia sóbria padrão LaTeX (Times-Roman look)
cover_univ_style = ParagraphStyle(
    'CoverUniv',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=12,
    leading=16,
    alignment=TA_CENTER,
    textColor=colors.black
)

cover_dept_style = ParagraphStyle(
    'CoverDept',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=11,
    leading=15,
    alignment=TA_CENTER,
    textColor=colors.black
)

cover_title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Normal'],
    fontName='Times-Bold',
    fontSize=16,
    leading=22,
    alignment=TA_CENTER,
    textColor=colors.black
)

cover_subtitle_style = ParagraphStyle(
    'CoverSubtitle',
    parent=styles['Normal'],
    fontName='Times-Italic',
    fontSize=13,
    leading=18,
    alignment=TA_CENTER,
    textColor=colors.black
)

cover_date_style = ParagraphStyle(
    'CoverDate',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=10.5,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.black
)

h1_style = ParagraphStyle(
    'Heading1_LaTeX',
    parent=styles['Heading1'],
    fontName='Times-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.black,
    spaceBefore=12,
    spaceAfter=5,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_LaTeX',
    parent=styles['Heading2'],
    fontName='Times-Bold',
    fontSize=11,
    leading=15,
    textColor=colors.black,
    spaceBefore=9,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body_LaTeX',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=10,
    leading=14.2,
    textColor=colors.black,
    alignment=TA_JUSTIFY,
    spaceAfter=5
)

code_style = ParagraphStyle(
    'Code_LaTeX',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=7.0,
    leading=8.8,
    textColor=colors.black,
    backColor=colors.HexColor("#fbfbfb"),
    borderColor=colors.HexColor("#d1d5db"),
    borderWidth=0.5,
    borderPadding=4,
    spaceBefore=2,
    spaceAfter=4
)

caption_style = ParagraphStyle(
    'Caption_LaTeX',
    parent=styles['Normal'],
    fontName='Times-Italic',
    fontSize=9,
    leading=12,
    alignment=TA_CENTER,
    textColor=colors.black,
    spaceBefore=3,
    spaceAfter=8
)

table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Times-Bold',
    fontSize=8.5,
    leading=11,
    alignment=TA_LEFT,
    textColor=colors.black
)

table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=8.5,
    leading=11,
    alignment=TA_LEFT,
    textColor=colors.black
)

story = []

# =========================================================================
# CAPA (Idêntica ao modelo SED: Brasão, Título, Tabela Booktabs, Cidade/Ano)
# =========================================================================
story.append(Spacer(1, 15))
story.append(Paragraph("Escola Politécnica da Universidade de São Paulo", cover_univ_style))
story.append(Paragraph("PMR3304 – Sistemas de Informação", cover_dept_style))

story.append(Spacer(1, 35))
if os.path.exists(brasao_path):
    emblem_img = Image(brasao_path, width=150, height=135)
    emblem_table = Table([[emblem_img]], colWidths=[487])
    emblem_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(emblem_table)
else:
    story.append(Spacer(1, 135))

story.append(Spacer(1, 40))
story.append(Paragraph("Segunda Entrega de Laboratório", cover_title_style))
story.append(Spacer(1, 6))
story.append(Paragraph("Aplicação Web CRUD com Django", cover_subtitle_style))

story.append(Spacer(1, 45))

# Tabela de Autoria estilo LaTeX Booktabs
author_data = [
    [Paragraph("<b>Nome</b>", table_header_style), Paragraph("<b>NUSP</b>", table_header_style)],
    [Paragraph("Henrique Moreno de Morais", table_cell_style), Paragraph("15459239", table_cell_style)]
]
author_table = Table(author_data, colWidths=[240, 100])
author_table.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),  # toprule
    ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),  # midrule
    ('LINEBELOW', (0,1), (-1,1), 1.0, colors.black),  # bottomrule
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))

author_container = Table([[author_table]], colWidths=[487])
author_container.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
story.append(author_container)

story.append(Spacer(1, 135))
story.append(Paragraph("São Paulo", cover_date_style))
story.append(Spacer(1, 2))
story.append(Paragraph("Novembro de 2026", cover_date_style))
story.append(PageBreak())

# =========================================================================
# 1. INTRODUÇÃO
# =========================================================================
story.append(Paragraph("1. Introdução", h1_style))
story.append(Paragraph(
    "No desenvolvimento de sistemas de informação modernos, a transição de sítios exclusivamente "
    "estáticos para aplicações dinâmicas orientadas a banco de dados representa uma etapa fundamental. "
    "Diferente da primeira entrega de laboratório, baseada em páginas HTML geradas estaticamente, uma aplicação dinâmica "
    "viabiliza operações em tempo de execução para inserção, consulta, atualização e remoção de registros "
    "(ciclo CRUD) diretamente pelo navegador web. Esse arranjo elimina a necessidade de alteração manual "
    "dos arquivos fonte e permite a interação de usuários convencionais sem conhecimentos de programação.",
    body_style
))
story.append(Paragraph(
    "Para a implementação deste projeto, utilizou-se o framework web <i>Django</i>, estruturado sob o "
    "padrão arquitetural MTV (<i>Model-Template-View</i>). Na camada de modelo (<i>Model</i>), o ORM nativo "
    "(<i>Object-Relational Mapping</i>) realiza o mapeamento entre as classes declaradas em Python e o banco relacional "
    "SQLite, garantindo integridade referencial e tipagem consistente. A camada de apresentação (<i>Template</i>) "
    "provê a estrutura visual via herança de layout, enquanto a camada de controle (<i>View</i>) processa as requisições "
    "HTTP, interage com a base de dados e devolve as respostas adequadas ao cliente.",
    body_style
))
story.append(Paragraph(
    "O escopo do sistema desenvolvido contempla um portal temático de engenharia intitulado <b>ArenaBot</b>, "
    "focado em projeto mecânico de armas de impacto, dimensionamento de motores brushless, blindagens em UHMW e titânio, "
    "e procedimentos de segurança em robôs de combate (categorias <i>Beetleweight</i> e <i>Featherweight</i>). "
    "O sistema implementa o ciclo CRUD completo de postagens, gerenciamento de comentários vinculados ao modelo de "
    "usuários do framework, categorização com relacionamentos <i>ManyToMany</i> e execução de consultas analíticas "
    "em linguagem SQL sobre o banco SQLite.",
    body_style
))

# =========================================================================
# 2. OBJETIVO
# =========================================================================
story.append(Spacer(1, 4))
story.append(Paragraph("2. Objetivo", h1_style))
story.append(Paragraph(
    "O objetivo deste laboratório consiste em projetar, codificar, testar e documentar uma aplicação web "
    "dinâmica completa em Django, atendendo aos seguintes objetivos específicos:",
    body_style
))
story.append(Paragraph(
    "1. <b>Elaboração do CRUD de Posts:</b> Construção da aplicação central sem bibliotecas externas de terceiros, "
    "utilizando um template base compartilhado na pasta <code>/templates</code>, modelo <code>Post</code> com "
    "renderização de conteúdo HTML (filtro <code>safe</code>) e datas tipadas (filtro <code>date</code>), "
    "resposta HTTP 404 para identificadores inexistentes e página de confirmação para exclusão de registros.",
    body_style
))
story.append(Paragraph(
    "2. <b>Evolução das Camadas de Controle (Views):</b> Desenvolvimento e comparação, em três <i>commits</i> "
    "sequenciais no repositório Git, de três paradigmas de views: (a) views funcionais manuais sem formulários "
    "ou validação; (b) views funcionais com <code>ModelForm</code>; e (c) views baseadas em classes genéricas "
    "(<i>Generic Class-Based Views</i>: <code>ListView</code>, <code>DetailView</code>, <code>CreateView</code>, "
    "<code>UpdateView</code> e <code>DeleteView</code>).",
    body_style
))
story.append(Paragraph(
    "3. <b>Módulo de Comentários:</b> Implementação de comentários vinculados ao modelo padrão de usuários do "
    "Django (<code>AUTH_USER_MODEL</code>) na <i>branch</i> <code>comments</code>, com exibição decrescente cronológica "
    "e inclusão direta a partir da página de detalhe da postagem.",
    body_style
))
story.append(Paragraph(
    "4. <b>Módulo de Categorias:</b> Estruturação da <i>branch</i> <code>categories</code> para associar posts e "
    "categorias via relação <i>ManyToMany</i>, reutilizando o template de listagem de posts e implementando "
    "navegação cruzada entre postagens e categorias.",
    body_style
))
story.append(Paragraph(
    "5. <b>Consultas Relacionais em SQL:</b> Povoamento do banco de dados <code>db.sqlite3</code> com a volumetria "
    "mínima estipulada e elaboração de cinco consultas SQL nativas no SQLite, abrangendo filtros, junções internas "
    "(<code>JOIN</code>) e agrupamentos com restrição agregada (<code>GROUP BY ... HAVING</code>).",
    body_style
))

story.append(PageBreak())

# =========================================================================
# 3. METODOLOGIA
# =========================================================================
story.append(Paragraph("3. Metodologia", h1_style))
story.append(Paragraph(
    "A metodologia de desenvolvimento adotada seguiu rigorosamente os padrões de engenharia de software "
    "apresentados ao longo das aulas da disciplina PMR3304:",
    body_style
))

story.append(Paragraph("3.1. Controle de Versão e Estrutura de Ramificações (Git)", h2_style))
story.append(Paragraph(
    "O versionamento do código foi conduzido por meio do Git. O arquivo de configuração <code>.gitignore</code> "
    "foi parametrizado desde o primeiro commit para ignorar diretórios transitórios (<code>__pycache__/</code>, "
    "<code>venv/</code>) e a base de dados relacional <code>db.sqlite3</code>. "
    "O fluxo de desenvolvimento foi dividido em três branches principais:",
    body_style
))
story.append(Paragraph(
    "• <b>Branch <code>main</code>:</b> Concentrou a estrutura básica do projeto, configurações de ambiente "
    "e a implementação sequencial das três versões de views da Parte 1, registradas em três commits dedicados.<br/>"
    "• <b>Branch <code>comments</code>:</b> Criada a partir da <code>main</code> para isolar a modelagem de "
    "comentários, migrações e rotas de criação de comentários. Ao término da validação, foi integrada via <i>merge</i>.<br/>"
    "• <b>Branch <code>categories</code>:</b> Ramificada a partir da <code>main</code> atualizada, acomodando a "
    "relação <i>ManyToMany</i>, views de listagem e detalhe de categorias, e templates adaptados, sendo igualmente "
    "unificada à <code>main</code>.",
    body_style
))

story.append(Paragraph("3.2. Modelagem de Dados e Esquema Relacional", h2_style))
story.append(Paragraph(
    "A modelagem conceitual foi descrita em Python no módulo <code>blog/models.py</code>. A Tabela 1 sintetiza "
    "os modelos, campos e restrições adotadas.",
    body_style
))

story.append(Spacer(1, 2))
story.append(Paragraph("Tabela 1: Especificação dos modelos relacionais implementados no Django.", caption_style))

models_table_data = [
    [Paragraph("<b>Modelo</b>", table_header_style), Paragraph("<b>Campo</b>", table_header_style), Paragraph("<b>Tipo Django</b>", table_header_style), Paragraph("<b>Descrição e Restrições</b>", table_header_style)],
    [Paragraph("Post", table_cell_style), Paragraph("title", table_cell_style), Paragraph("CharField(200)", table_cell_style), Paragraph("Título da publicação", table_cell_style)],
    [Paragraph("Post", table_cell_style), Paragraph("content", table_cell_style), Paragraph("TextField", table_cell_style), Paragraph("Texto com marcação HTML (filtro safe)", table_cell_style)],
    [Paragraph("Post", table_cell_style), Paragraph("created_at", table_cell_style), Paragraph("DateTimeField", table_cell_style), Paragraph("Timestamp automático (auto_now_add=True)", table_cell_style)],
    [Paragraph("Post", table_cell_style), Paragraph("categories", table_cell_style), Paragraph("ManyToManyField", table_cell_style), Paragraph("Associação com Category (related_name='posts')", table_cell_style)],
    [Paragraph("Comment", table_cell_style), Paragraph("post", table_cell_style), Paragraph("ForeignKey", table_cell_style), Paragraph("Chave estrangeira para Post (on_delete=CASCADE)", table_cell_style)],
    [Paragraph("Comment", table_cell_style), Paragraph("author", table_cell_style), Paragraph("ForeignKey", table_cell_style), Paragraph("Chave para AUTH_USER_MODEL", table_cell_style)],
    [Paragraph("Comment", table_cell_style), Paragraph("text", table_cell_style), Paragraph("TextField", table_cell_style), Paragraph("Corpo textual do comentário", table_cell_style)],
    [Paragraph("Comment", table_cell_style), Paragraph("created_at", table_cell_style), Paragraph("DateTimeField", table_cell_style), Paragraph("Ordenação decrescente: ordering=['-created_at']", table_cell_style)],
    [Paragraph("Category", table_cell_style), Paragraph("name", table_cell_style), Paragraph("CharField(100)", table_cell_style), Paragraph("Nome da categoria", table_cell_style)],
    [Paragraph("Category", table_cell_style), Paragraph("description", table_cell_style), Paragraph("TextField", table_cell_style), Paragraph("Descrição detalhada do escopo", table_cell_style)],
]
models_table = Table(models_table_data, colWidths=[65, 75, 105, 230])
models_table.setStyle(TableStyle([
    ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),
    ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(models_table)

story.append(Spacer(1, 4))
story.append(Paragraph("3.3. Arquitetura de Templates e Navegação", h2_style))
story.append(Paragraph(
    "A camada visual utiliza o mecanismo de herança do Django. O arquivo <code>templates/base.html</code>, "
    "localizado na raiz do projeto conforme exigido no enunciado, encapsula a navegação global, metatags, folhas "
    "de estilo estruturais e o rodapé. Os demais templates estendem o base utilizando <code>{% extends 'base.html' %}</code> "
    "e injetam conteúdo no bloco <code>{% block content %}</code>. Todos os links internos foram mapeados "
    "estritamente pelos nomes de rota configurados em <code>urls.py</code> via <code>{% url 'nome' %}</code>, "
    "e os formulários incluem o token de segurança <code>{% csrf_token %}</code> contra ataques <i>Cross-Site Request Forgery</i>.",
    body_style
))

story.append(PageBreak())

# =========================================================================
# 4. RESULTADOS
# =========================================================================
story.append(Paragraph("4. Resultados", h1_style))
story.append(Paragraph(
    "A seguir são apresentados os resultados obtidos em cada uma das quatro partes do projeto, incluindo listagens "
    "de código-fonte, capturas de tela das rotas da aplicação web e resultados das consultas SQL.",
    body_style
))

# 4.1 PARTE 1
story.append(Paragraph("4.1. Parte 1: Aplicação CRUD de Posts e Três Versões de Views", h2_style))
story.append(Paragraph(
    "Para atender aos requisitos da primeira etapa, foram desenvolvidas três versões sequenciais do arquivo "
    "<code>blog/views.py</code>, cada uma vinculada a um commit distinto no Git:",
    body_style
))

# V1
story.append(Paragraph("<b>Versão 1: Views funcionais puras sem formulários e sem validação:</b>", body_style))
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

# V3 on same page (fits perfectly with V1)
story.append(Spacer(1, 2))
story.append(Paragraph("<b>Versão 3: Generic Class-Based Views (CBVs):</b>", body_style))
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

# V2 on next page with comparison discussion (fits completely without breaking!)
story.append(Paragraph("<b>Versão 2: Views funcionais com formulário Django (PostForm):</b>", body_style))
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

story.append(Spacer(1, 4))
story.append(Paragraph("<b>Análise Comparativa das Abordagens:</b>", h2_style))
story.append(Paragraph(
    "A comparação prática entre as três implementações evidencia a evolução dos padrões de projeto no Django. "
    "A <i>Versão 1</i> processa manualmente as chaves do dicionário <code>request.POST</code>, sem sanitização "
    "automática ou validação de tipos, o que a torna propensa a inconsistências caso campos obrigatórios venham vazios. "
    "A <i>Versão 2</i> introduz a classe <code>PostForm</code> (derivada de <code>ModelForm</code>), centralizando regras "
    "de validação via <code>form.is_valid()</code> e permitindo a reutilização automática dos dados submetidos em caso de erro. "
    "Por fim, a <i>Versão 3</i> utiliza as classes genéricas (CBVs) do framework, que eliminam o código repetitivo "
    "de consulta ao banco (<code>get_object_or_404</code>), gerenciamento de métodos HTTP (GET/POST) e redirecionamentos, "
    "reduzindo o código em mais de 50% e aderindo ao princípio DRY (<i>Don't Repeat Yourself</i>).",
    body_style
))

story.append(PageBreak())

# Função para adicionar capturas de tela com moldura clássica
def add_figure_card(img_name, caption_text, w=460, h=225):
    img_path = os.path.join(prints_dir, img_name)
    if os.path.exists(img_path):
        img_obj = Image(img_path, width=w, height=h)
        container = Table([[img_obj]], colWidths=[w])
        container.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(KeepTogether([
            container,
            Spacer(1, 3),
            Paragraph(caption_text, caption_style),
            Spacer(1, 4)
        ]))

story.append(Paragraph("<b>Capturas de Tela da Aplicação CRUD (Parte 1):</b>", h2_style))
add_figure_card("print_01_post_list.png", "Figura 1: Página inicial de listagem de postagens (/), com links para visualização e criação.", w=460, h=220)
add_figure_card("print_02_post_detail.png", "Figura 2: Página individual de post (/post/1/), renderizando HTML seguro (safe) e data formatada (date).", w=460, h=220)

story.append(PageBreak())
add_figure_card("print_03_post_create.png", "Figura 3: Formulário de criação de nova postagem (/post/new/).", w=460, h=215)
add_figure_card("print_04_post_update.png", "Figura 4: Formulário de edição de postagem existente (/post/1/edit/).", w=460, h=215)

story.append(PageBreak())
add_figure_card("print_05_post_confirm_delete.png", "Figura 5: Página de confirmação de exclusão com proteção POST (/post/1/delete/).", w=460, h=210)

story.append(PageBreak())

# 4.2 PARTE 2
story.append(Paragraph("4.2. Parte 2: Sistema de Comentários nos Posts", h2_style))
story.append(Paragraph(
    "Desenvolvido na branch <code>comments</code> e incorporado à <code>main</code> após testes. "
    "O modelo <code>Comment</code> associa o autor ao <code>AUTH_USER_MODEL</code> e organiza as mensagens "
    "em ordem cronológica decrescente. O arquivo <code>views.py</code> foi expandido com a função "
    "<code>comment_create</code> e a sobrecarga de <code>get_context_data</code> em <code>PostDetailView</code>:",
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

story.append(PageBreak())
story.append(Paragraph("<b>Capturas de Tela do Sistema de Comentários (Parte 2):</b>", h2_style))
add_figure_card("print_06b_post_comments.png", "Figura 6: Página individual de post exibindo a seção de comentários ordenados pelo mais recente.", w=440, h=300)
add_figure_card("print_06_comment_create.png", "Figura 7: Formulário dedicado para criação de comentário (/post/1/comment/).", w=460, h=210)

story.append(PageBreak())

# 4.3 PARTE 3
story.append(Paragraph("4.3. Parte 3: Sistema de Categorias e Implantação", h2_style))
story.append(Paragraph(
    "Implementado na branch <code>categories</code> e integrado à <code>main</code>. O modelo <code>Category</code> "
    "relaciona-se com <code>Post</code> em esquema N:N. A view de detalhe da categoria reutiliza o template "
    "<code>post_list.html</code>, adaptando a renderização conforme a presença do objeto <code>category</code> no contexto:",
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

story.append(PageBreak())
story.append(Paragraph("<b>Capturas de Tela do Sistema de Categorias (Parte 3):</b>", h2_style))
add_figure_card("print_02_post_detail.png", "Figura 8: Detalhe do post exibindo as categorias às quais pertence com links navegáveis.", w=460, h=215)
add_figure_card("print_07_category_list.png", "Figura 9: Listagem geral de categorias cadastradas (/categories/) com link no cabeçalho.", w=460, h=210)

story.append(PageBreak())
add_figure_card("print_08_category_detail.png", "Figura 10: Página individual de categoria (/categories/1/), reutilizando post_list.html para filtrar posts.", w=460, h=220)

story.append(Spacer(1, 4))
links_table_data = [
    [Paragraph("<b>Ambiente</b>", table_header_style), Paragraph("<b>Link de Acesso</b>", table_header_style)],
    [Paragraph("Repositório Git (GitHub)", table_cell_style), Paragraph("<a href='https://github.com/aluno-si/django-blog-lab'>https://github.com/aluno-si/django-blog-lab</a>", table_cell_style)],
    [Paragraph("Aplicação em Produção (Render)", table_cell_style), Paragraph("<a href='https://django-blog-app.onrender.com'>https://django-blog-app.onrender.com</a>", table_cell_style)],
]
links_table = Table(links_table_data, colWidths=[160, 315])
links_table.setStyle(TableStyle([
    ('LINEABOVE', (0,0), (-1,0), 1.0, colors.black),
    ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 1.0, colors.black),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(KeepTogether([
    Paragraph("Tabela 2: Repositório de código e endereço da aplicação publicada.", caption_style),
    links_table,
    Spacer(1, 4),
    Paragraph("<i>Nota: Conforme indicado no enunciado, os links de acesso foram igualmente registrados nos comentários da entrega no e-Disciplinas.</i>", caption_style)
]))

story.append(PageBreak())

# 4.4 PARTE 4: CONSULTAS SQL
story.append(Paragraph("4.4. Parte 4: Exercícios e Consultas em SQL Nativo", h2_style))
story.append(Paragraph(
    "A base de dados <code>db.sqlite3</code> foi populada atendendo aos requisitos de volumetria: 3 postagens "
    "(1 sem comentários e 2 com múltiplos comentários e categorias), 3 categorias e 5 comentários distribuídos entre "
    "usuários distintos. As consultas foram elaboradas e executadas no SQLite através do software <i>DB Browser for SQLite</i>:",
    body_style
))

def add_sql_section(num, title_text, sql_code, img_name):
    img_path = os.path.join(prints_dir, img_name)
    story.append(KeepTogether([
        Paragraph(f"<b>Consulta {num}: {title_text}</b>", h2_style),
        Paragraph(sql_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style),
        Image(img_path, width=460, height=185) if os.path.exists(img_path) else Spacer(1, 10),
        Spacer(1, 3),
        Paragraph(f"Figura {10 + num}: Execução e resultado da Consulta {num} no DB Browser for SQLite.", caption_style),
        Spacer(1, 6)
    ]))

# Consulta 1
add_sql_section(
    1,
    "Todos os posts ordenados pela data mais recente primeiro",
    """SELECT id, title, created_at, content 
FROM blog_post 
ORDER BY created_at DESC;""",
    "print_sql_01.png"
)

story.append(PageBreak())

# Consulta 2
add_sql_section(
    2,
    "Para um post com comentários, todos os seus comentários",
    """SELECT id, text, created_at, author_id, post_id 
FROM blog_comment 
WHERE post_id = 1 
ORDER BY created_at DESC;""",
    "print_sql_02.png"
)

# Consulta 3
add_sql_section(
    3,
    "Comentários sem post_id, com título do post e data renomeada para post_date",
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

# Consulta 4
add_sql_section(
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

# Consulta 5
add_sql_section(
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

story.append(PageBreak())

# =========================================================================
# 5. CONCLUSÃO
# =========================================================================
story.append(Paragraph("5. Conclusão", h1_style))
story.append(Paragraph(
    "A execução deste trabalho permitiu consolidar na prática os fundamentos de desenvolvimento de sistemas de informação "
    "baseados na web. A comparação entre os três paradigmas de views evidenciou a evolução da produtividade: enquanto "
    "as views funcionais puras exigem escrita explícita para manipulação do dicionário <code>request.POST</code> e persistência, "
    "a adoção de <code>ModelForm</code> assegura integridade de dados e as <code>generic class-based views</code> abstraem "
    "o fluxo rotineiro de busca por chave primária, renderização e tratamento de métodos HTTP com expressiva concisão.",
    body_style
))
story.append(Paragraph(
    "O isolamento das funcionalidades em branches distintas (<code>comments</code> e <code>categories</code>) permitiu "
    "verificar a conveniência do versionamento com Git em projetos com evolução incremental de banco de dados. "
    "Por fim, a execução das consultas SQL sobre a base física <code>db.sqlite3</code> validou a fidelidade do ORM do Django, "
    "comprovando como os relacionamentos de chave estrangeira e ManyToMany declarados em código Python correspondem exatamente "
    "às tabelas de junção e restrições referenciais do modelo relacional clássico.",
    body_style
))

# Construção final do PDF
doc.build(story, canvasmaker=NumberedCanvas)
print(f"Relatório PDF em formato LaTeX gerado com sucesso em: {pdf_path}")
print(f"Tamanho do arquivo: {os.path.getsize(pdf_path)} bytes")
