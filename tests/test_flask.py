from asyncio import as_completed
from cgitb import html
from unittest import TestCase

from app import app
from models import db, User, default_img

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UserViewsTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        user = User(first_name='John', last_name='Smith', image_url=default_img)
        db.session.add(user)
        db.session.commit()
        self.user_id=user.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertIn('John', html)
            self.assertIn('Smith', html)

    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<input type="text" name="first_name" placeholder="Enter first name" />', html)
            self.assertIn('<input type="text" name="last_name" placeholder="Enter last name" />', html)
            self.assertIn('<input type="text" name="image_url" placeholder="Enter image url" />', html)

    def test_submit_new_user_form(self):
        with app.test_client() as client:
            d = {"first_name": "Jane", "last_name": "Doe", "image_url": default_img}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)
            self.assertIn('Doe', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>John Smith</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get('/users/1/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit John Smith</h1>', html)

    def test_update_user(self):
        with app.test_client() as client:
            d = {"first_name": "John", "last_name": "Doe", "image_url": default_img}
            resp = client.post(f'users/{self.user_id}/edit', data = d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)
            self.assertIn('Doe', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            print(resp.status_code)
            print('user is', self.user_id)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John', html)
            self.assertNotIn('Smith', html)