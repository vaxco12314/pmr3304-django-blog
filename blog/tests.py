from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Category

class BlogAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Tecnologia', description='Posts de tecnologia')
        self.post = Post.objects.create(title='Post de Teste', content='<p>Conteudo HTML de teste</p>')
        self.post.categories.add(self.category)
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='Otimo post!')

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de Teste')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de Teste')
        self.assertContains(response, 'Otimo post!')

    def test_post_detail_404(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tecnologia')

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de Teste')

    def test_category_detail_404(self):
        response = self.client.get(reverse('category_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_post_create_view(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_update_view(self):
        response = self.client.get(reverse('post_update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view_get(self):
        response = self.client.get(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirmar Exclusão')

    def test_comment_create_view(self):
        response = self.client.get(reverse('comment_create', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
