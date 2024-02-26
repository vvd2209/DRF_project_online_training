from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from education.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        """
        Создание тестового пользователя
        """
        self.user = User(email='test@test.ru', phone='111111111', city='test', is_superuser=False, is_staff=True,
                         is_active=True)
        self.user.set_password('1234')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user.save()

        response = self.client.post(
            '/token/',
            {"email": "test@test.ru", "password": "1234"}
        )

        self.access_token = response.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

        self.course = Course.objects.create(
            name="test_course",
        )

        self.lesson = Lesson.objects.create(
            name="test_lesson",
            description="test lesson description",
            owner=self.user
        )

    def test_create_lesson(self):
        """
        Тест создания урока
        """
        data = {
            "name": "test",
            "course": 1,
            "video": "https://www.youtube.com/",
            "description": "test lesson description"
        }
        create_lesson = reverse('education:lesson_create')
        response = self.client.post(create_lesson, data, format='json', **self.headers)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], data['name'])

    def test_retrieve_lesson(self):
        """
        Тест просмотра урока
        """
        retrieve_url = reverse('education:lesson_view', args=[self.lesson.id])
        response = self.client.get(retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """
        Тест редактирования урока
        """
        update_url = reverse('education:lesson_update', args=[self.lesson.id])
        updated_data = {
            "name": "Updated Lesson",
            "description": "This is an updated lesson",
        }
        response = self.client.patch(update_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, updated_data['name'])
        self.assertEqual(self.lesson.description, updated_data['description'])

    def test_destroy_lesson(self):
        """
        Тест удаления урока
        """
        delete_url = reverse('education:lesson_delete', args=[self.lesson.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_list_lessons(self):
        """
        Тест просмотра списка всех уроков
        """
        list_url = reverse('education:lesson_list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.lesson.name)
