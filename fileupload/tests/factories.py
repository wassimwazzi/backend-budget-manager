import factory
from user_factory import UserFactory
from ..models import FileUpload, Status


class FileUploadFactory(factory.django.DjangoModelFactory):
    """
    File Upload factory
    """

    class Meta:
        model = FileUpload

    user = factory.SubFactory(UserFactory)
    file = factory.django.FileField(filename="test.csv")
    date = factory.Faker("date")
    status = Status.PENDING
    message = None
