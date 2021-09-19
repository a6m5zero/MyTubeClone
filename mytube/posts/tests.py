from os import stat
from django.http import response
from django.shortcuts import redirect
from django.test import TestCase
from django.test import client
from django.test.client import Client
from .models import Post, User, Follow
from time import sleep 

# После регистрации пользователя создается его персональная страница (profile)
class ProfileTest(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='TestUser', email="Test@mail.ru", password="123456"
        )
        self.user2 = User.objects.create_user(
            username='TestUser2', email="Test@mail.ru", password="123456"
        )

        self.post = Post.objects.create(text="TestingProfile", 
                                        author=self.user, 
                                        image = '../media/posts/nissan-silvia-s15-spec-r-jdm.jpg')

    def tearDown(self) -> None:
        return super().tearDown()
        pass

    def test_profile(self):
        response = self.client.get("/TestUser/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertIsInstance(response.context['username'], User)
        self.assertEqual(response.context['username'].username, 'TestUser')

    def test_send_post_login(self):
        response = self.client.post('/auth/login/', {'username': 'TestUser', 'password': '123456'}, follow=True)
        self.assertEqual(response.status_code, 200)
        text = 'Тестовое сообщение Текст № 555'
        response = self.client.post('/new/',{'groups':'', 'text':text}, follow=True)
        
        self.assertRedirects(response, '/')
        self.assertContains(response, text, status_code=200)

        response = self.client.get('/TestUser/')
        self.assertContains(response, text, status_code=200)

        post = Post.objects.get(text=text)
        response = self.client.get(f'/TestUser/{post.id}/')
        self.assertEqual(response.status_code, 200)


    def test_send_post_logout(self):
        self.client.logout()
        response = self.client.post('/new/',{'groups':'', 'text':123})
        self.assertRegex(response.url, r'/auth/login/')

    def test_edit_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(f'/{self.user.username}/{self.post.id}/edit/', follow=True)
        text = 'Тестовое сообщение Отредактированный текст'
        response = self.client.post(f'/TestUser/{self.post.id}/edit/',{'groups':'', 'text':text}, follow=True)
        self.assertContains(response, text, status_code=200)

    def test_404_template(self):
        response = self.client.get('/testpage/testpage/', follow=True)
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, 'misc/404.html')

    def test_images_on_pages(self):
        response = self.client.get('/TestUser/')
        self.assertContains(response, '<img class="card-img"')

    def test_upload_exe(self):
        # with open('1.jpg', 'rb') as image:
        with open('db.sqlite3', 'rb') as image:
            self.client.force_login(self.user, backend=None)
            post = self.client.post('/new/',{'groups':'', 'text': 'ImageUpload', 'image': image},follow=True)
            self.assertIsNotNone(post.context['form'].errors)

    # Тестируем работу кэширования
    def test_index_cache(self):
        self.client.get('/')
        new_post = Post.objects.create(text="TEST CACHE", author=self.user, image = '../media/posts/nissan-silvia-s15-spec-r-jdm.jpg')
        response = self.client.get('/')
        self.assertNotContains(response, new_post.text, status_code=200)
        sleep(20)
        response = self.client.get('/')
        self.assertContains(response, new_post.text, status_code=200)
    
    # Авторизованный пользователь может подписываться на авторов.
    def test_follow(self):
        self.client.force_login(self.user2, backend=None)
        response = self.client.get(f'/{self.user.username}/follow/', follow=True)
        self.assertRedirects(
            response, f'/{self.user.username}/',status_code=302,target_status_code=200)
        self.assertIsNotNone(Follow.objects.filter(user=self.user2, author=self.user))

    # Авторизованный пользователь может отписываться от авторов.
    def test_unfollow(self):
        self.client.force_login(self.user2, backend=None)
        Follow.objects.create(user=self.user2, author=self.user)
        response = self.client.get(f'/{self.user.username}/unfollow/', follow=True)
        self.assertRedirects(
            response, f'/{self.user.username}/',status_code=302,target_status_code=200)
        self.assertEqual(len(Follow.objects.filter(user=self.user2, author=self.user)),0)

