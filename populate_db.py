import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment, Category
from django.utils import timezone
import datetime

print("Iniciando população da base de dados do blog ArenaBot...")

# 0. Limpeza total e reset de autoincrement
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM blog_comment;")
    cursor.execute("DELETE FROM blog_post_categories;")
    cursor.execute("DELETE FROM blog_post;")
    cursor.execute("DELETE FROM blog_category;")
    cursor.execute("DELETE FROM auth_user;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('blog_post', 'blog_comment', 'blog_category', 'auth_user');")

# 1. Usuários
admin_user = User.objects.create_superuser('admin', 'admin@arenabot.com.br', 'admin123')
marcos = User.objects.create_user('marcos_mec', 'marcos@poli.usp.br', 'senha123')
pedro = User.objects.create_user('pedro_elec', 'pedro@poli.usp.br', 'senha123')
lucas = User.objects.create_user('lucas_poli', 'lucas@poli.usp.br', 'senha123')

print("Usuários criados: admin, marcos_mec, pedro_elec, lucas_poli")

# 2. Categorias
cat_mec = Category.objects.create(
    name='Projeto e Mecânica',
    description='Armações, materiais como Titânio e Hardox, dentes de impacto, tambores e cálculos de inércia.'
)

cat_elec = Category.objects.create(
    name='Eletrônica e Motores',
    description='Baterias LiPo, controladores brushless (ESCs), rádios 2.4GHz e dimensionamento elétrico.'
)

cat_rules = Category.objects.create(
    name='Categorias de Peso e Regras',
    description='Normas de segurança, limites de peso (Beetleweight, Featherweight) e inspeção de arena.'
)

print("Categorias criadas: Projeto e Mecânica, Eletrônica e Motores, Categorias de Peso e Regras")

# Post 1 (comentado, múltiplas categorias: Projeto e Mecânica + Eletrônica e Motores)
p1 = Post.objects.create(
    title='Dimensionamento de Reduções Planetárias e Motores Brushless para Armas de Tambor',
    content='''<p>Um dos erros mais comuns em robôs da classe <em>Beetleweight (1,36 kg)</em> com armas rotativas de tambor (drum spinners) é focar apenas na rotação máxima (RPM) e esquecer o <strong>tempo de aceleração (spin-up)</strong> e a taxa de avanço (bite).</p>
<h3>1. Cálculo de Rotação e Bite</h3>
<p>Se o seu tambor gira rápido demais sem ter dentes com altura suficiente, ele simplesmente raspa na blindagem do oponente em vez de transferir energia cinética. O dente precisa de tempo mecânico para engatar por baixo do adversário antes de desferir o golpe.</p>
<ul>
    <li><strong>Momento de Inércia:</strong> Concentre a massa nas extremidades do diâmetro do tambor.</li>
    <li><strong>Redução por Polias:</strong> Polias sincronizadoras HTD 3M com correias de poliuretano com alma de aço evitam que o motor trave em impactos diretos.</li>
    <li><strong>Controlador (ESC):</strong> Sempre utilize controladores com limite de corrente ativo para não queimar enrolamentos durante travamentos na arena.</li>
</ul>
<p>Um tempo de spin-up entre 1,5s e 2,5s é ideal para manter a manobrabilidade e estar sempre pronto para o contra-ataque.</p>''',
)
p1.categories.set([cat_mec, cat_elec])
p1.created_at = timezone.now() - datetime.timedelta(days=2)
p1.save()

# Comentários do Post 1 (3 comentários)
c1_1 = Comment.objects.create(
    post=p1,
    author=marcos,
    text='Excelente post! Para o dente de impacto você recomenda fixar com parafusos de grau 12.9 ou usinar inteiriço em aço ferramenta S7?',
)
c1_1.created_at = timezone.now() - datetime.timedelta(days=2, hours=-1)
c1_1.save()

c1_2 = Comment.objects.create(
    post=p1,
    author=pedro,
    text='Sobre os ESCs, tivemos muito problema de desync em acelerações bruscas. O que resolveu pra gente foi migrar para controladores com firmware AM32.',
)
c1_2.created_at = timezone.now() - datetime.timedelta(days=2, hours=-2)
c1_2.save()

c1_3 = Comment.objects.create(
    post=p1,
    author=lucas,
    text='Muito didático! Estamos projetando um Beetleweight aqui na faculdade e essa relação de inércia e bite ajudou demais a fechar as polias.',
)
c1_3.created_at = timezone.now() - datetime.timedelta(days=2, hours=-3)
c1_3.save()


# Post 2 (comentado, múltiplas categorias: Projeto e Mecânica + Categorias de Peso e Regras)
p2 = Post.objects.create(
    title='Guia de Blindagem: Quando Usar UHMW, Alumínio 7075 ou Titânio Grau 5',
    content='''<p>Escolher o material certo para o chassi e as placas de proteção é o que define se o seu robô vai sobreviver aos três minutos de combate ou sair em pedaços da caixa de acrílico.</p>
<h3>Comparativo Rápido de Materiais:</h3>
<ul>
    <li><strong>UHMW (Polietileno de Ultra Alto Peso Molecular):</strong> Excelente absorvedor de choques. Ele deforma plasticamente sem trincar contra impactos de discos horizontais de alta energia.</li>
    <li><strong>Titânio Grau 5 (Ti-6Al-4V):</strong> A melhor relação resistência/peso para cunhas frontais e apoios de chão. É leve, difícil de perfurar e produz faíscas que impressionam os juízes.</li>
    <li><strong>Alumínio 7075-T6:</strong> Ideal para painéis estruturais internos usinados, pois é muito mais rígido que o alumínio comum 6061.</li>
</ul>
<p>Dica prática: monte as placas de titânio sobre coxins de borracha ou suportes de TPU flexível para que a estrutura interna de eletrônica não sofra com as ondas de choque.</p>''',
)
p2.categories.set([cat_mec, cat_rules])
p2.created_at = timezone.now() - datetime.timedelta(days=1)
p2.save()

# Comentários do Post 2 (2 comentários)
c2_1 = Comment.objects.create(
    post=p2,
    author=marcos,
    text='UHMW nas laterais salvou meu robô ano passado. Mesmo amassado ele não travou as rodas e conseguimos vencer na decisão dos juízes.',
)
c2_1.created_at = timezone.now() - datetime.timedelta(days=1, hours=-1)
c2_1.save()

c2_2 = Comment.objects.create(
    post=p2,
    author=pedro,
    text='Chanfrar as arestas externas do chassi também ajuda bastante o disco do adversário a escorregar em vez de travar o golpe em 90 graus.',
)
c2_2.created_at = timezone.now() - datetime.timedelta(days=1, hours=-2)
c2_2.save()


# Post 3 (sem comentários, 1 categoria: Categorias de Peso e Regras)
p3 = Post.objects.create(
    title='Checklist de Segurança e Fail-Safe para Inspeção Técnica na Arena',
    content='''<p>Antes de qualquer combate, todos os robôs devem passar obrigatoriamente pela <strong>inspeção técnica de segurança</strong> dos juízes. A reprovação impede a entrada na arena.</p>
<h3>Itens Obrigatórios de Verificação:</h3>
<ul>
    <li><strong>Chave Geral (Removable Link ou Switch de Potência):</strong> Deve estar localizada em local acessível externamente, sem que os dedos fiquem no raio de ação da arma ativa.</li>
    <li><strong>Trava Mecânica de Arma (Weapon Lock):</strong> Pino ou haste rígida que impede o movimento involuntário do tambor ou lâmina nos boxes e durante o transporte.</li>
    <li><strong>Fail-Safe de Rádio:</strong> Se o transmissor for desligado ou perder o sinal com a arena, tanto a tração quanto a arma devem cortar a potência imediatamente para neutro (zero).</li>
</ul>
<p>Faça esse teste no pit antes de levar o robô para a pesagem oficial!</p>''',
)
p3.categories.set([cat_rules])
p3.created_at = timezone.now()
p3.save()

print(f"Banco populado com sucesso:")
print(f"- {Post.objects.count()} posts")
print(f"- {Comment.objects.count()} comentários")
print(f"- {Category.objects.count()} categorias")
print(f"- {User.objects.count()} usuários")
