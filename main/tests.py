from rest_framework.test import APITestCase
from django.urls import reverse, TestCase
from .models import Course, User, Student, Product
from rest_framework import status

class CourseReviewAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.student = Student.objects.create(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="A great course.")
        self.client.login(username='testuser', password='password')

    def test_create_review(self):
        url = reverse('course-review-list')
        data = {
            'course': self.course.id,
            'student': self.student.id,
            'rating': 5,
            'comment': 'This is an excellent course!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_reviews(self):
        url = reverse('course-review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Product1", price=100)
        self.assertEqual(product.name, "Product1")
