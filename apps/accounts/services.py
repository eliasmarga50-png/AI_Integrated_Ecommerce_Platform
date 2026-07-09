


from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class UserService:
    """
    Service layer for user-related business logic.
    """

    @staticmethod
    @transaction.atomic
    def create_user(
        *,
        username,
        email,
        password,
        first_name="",
        last_name="",
        role=None,
    ):
        """
        Create a new user.

        All user creation should go through this service
        instead of calling User.objects.create_user()
        directly from views.
        """

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role or User.Role.CUSTOMER,
        )

        return user