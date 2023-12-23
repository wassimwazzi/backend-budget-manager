from user_factory import UserFactory
from ..models import Category
from django.test import TestCase


class TestCategorySignals(TestCase):
    """
    Test category signals
    """

    def test_on_user_created(self):
        """
        Test on user created, default categories are created
        """
        user = UserFactory()
        user_category_count = Category.objects.filter(user=user).count()
        self.assertGreater(user_category_count, 0)
