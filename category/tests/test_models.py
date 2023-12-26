import django.db.utils
from django.test import TestCase
from category.tests.factories import CategoryFactory
from category.models import Category
from users.user_factory import UserFactory


class CategoryModelTest(TestCase):
    """
    Category Model Test
    """

    def setUp(self):
        self.user = UserFactory()

    def test_unique_together(self):
        """
        Test unique together
        """
        category = CategoryFactory(user=self.user)
        with self.assertRaises(django.db.utils.IntegrityError):
            CategoryFactory(category=category.category, user=self.user)

    def test_cannot_delete_default_category(self):
        """
        Test cannot delete default category
        """
        with self.assertRaises(django.db.utils.IntegrityError):
            Category.objects.filter(user=self.user, is_default=True).first().delete()

    def test_cannot_have_two_default_categories(self):
        """
        Test cannot have two default categories
        """
        with self.assertRaises(django.db.utils.IntegrityError):
            CategoryFactory(is_default=True, user=self.user)

    def test_can_update_default_category(self):
        """
        Test can update default category
        """
        category = Category.objects.filter(user=self.user, is_default=True).first()
        category.name = "New Name"
        category.save()
        self.assertEqual(category.name, "New Name")
