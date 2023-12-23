import django.db.utils
from django.test import TestCase
from category.tests.factories import CategoryFactory


class CategoryModelTest(TestCase):
    """
    Category Model Test
    """

    def test_unique_together(self):
        """
        Test unique together
        """
        category = CategoryFactory()
        with self.assertRaises(django.db.utils.IntegrityError):
            CategoryFactory(category=category.category, user=category.user)
