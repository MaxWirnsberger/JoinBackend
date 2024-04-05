from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from kanban.models import MyUser, Task, Category, Contact

######################################################
#Login & Logout Test!!!!!
class UserLoginTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@example.com', first_name='test', last_name='user', password='12345')
        self.client = APIClient()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_user_login(self):
        url = reverse('login') 
        data = {
            'username': 'testuser@example.com',
            'password': '12345',
        }
        response = self.client.post(url, data)      
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        
        
    def test_user_logout(self):
        login_response = self.client.post(self.login_url, {'username': 'testuser@example.com', 'password': '12345'})
        token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, 200)

        self.client.credentials()
        protected_url = reverse('logout')
        protected_response = self.client.get(protected_url)
        self.assertNotEqual(protected_response.status_code, 200)
        

######################################################
#Create, Change and Delete Task - Test!!!!!
class TasksTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@example.com', first_name='test', last_name='user', password='12345')
        self.client = APIClient()
        
    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-list')
        data = {
            "title": "Test",
            "description": "Create reusable HTML base templates...!!!",
            "due_date": "2024-04-25",
            "status": "done",
            "priority": "medium",
            "category": {
                "name": "technical_task",
                "color": "#1FD7C1"
            },
            "subtasks": []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], "Test")
        
    def test_get_task(self):
        category = Category.objects.create(name="technical_task", color="#1FD7C1")
        task = Task.objects.create(
            title="Test", 
            description="Create reusable HTML base templates...!!!",
            due_date="2024-04-25",
            status="done",
            priority="medium",
            category=category,
            author=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Test")
        
        
    def test_update_task(self):
        category = Category.objects.create(name="technical_task", color="#1FD7C1")
        task = Task.objects.create(
            title="Test", 
            description="Create reusable HTML base templates...!!!",
            due_date="2024-04-25",
            status="done",
            priority="medium",
            category=category,
            author=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[task.id])
        update_data = {
            "title": "Update_Test",
            "description": "Create reusable HTML base templates...!!!",
            "due_date": "2024-04-25",
            "status": "done",
            "priority": "medium",
            "category": {
                "name": "technical_task",
                "color": "#1FD7C1"
            },
            "subtasks": []
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Update_Test")
    
    def test_delete_task(self):
        category = Category.objects.create(name="technical_task", color="#1FD7C1")
        task = Task.objects.create(
            title="Test", 
            description="Create reusable HTML base templates...!!!",
            due_date="2024-04-25",
            status="done",
            priority="medium",
            category=category,
            author=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

######################################################
#Create, Change and Delete Contact - Test!!!!!
class ContactTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(email='testuser@example.com', first_name='test', last_name='user', password='12345')
        self.client = APIClient()
        
    def test_create_get_contact(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('contact-list')
        data = {
            "name": "Neuer Kontakt",
            "email": "neuer.kontakt@example.com",
            "phone": "123456789",
            "color": "abcdef"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "Neuer Kontakt")
    
    def test_update_contact(self):
        contact = Contact.objects.create(
            name="Max Mustermann",
            email="max@example.com",
            phone="1234567890",
            color="123456",
            author=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('contact-detail', args=[contact.id]) 
        updated_data = {
            "name": "Maxine Musterfrau",
            "email": "maxine@example.com",
            "phone": "0987654321",
            "color": "654321"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Maxine Musterfrau")
        self.assertEqual(response.data['email'], "maxine@example.com")
        self.assertEqual(response.data['phone'], "0987654321")
        self.assertEqual(response.data['color'], "654321")

    
    def test_delete_contact(self):
        contact = Contact.objects.create(
            name="Löschbarer Kontakt",
            email="loeschbar@example.com",
            phone="987654321",
            color="123456",
            author=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('contact-detail', args=[contact.id]) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Contact.objects.filter(id=contact.id).exists())