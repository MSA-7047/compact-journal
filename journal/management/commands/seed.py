from io import StringIO
from django.core.management.base import BaseCommand, CommandError
from django.forms import ValidationError


from journal.models import User, Group, GroupMembership

import pytz
from faker import Faker
from random import randint, random
from math import floor, log10 as log

from typing import Annotated, Any

user_fixtures = [
    [
        {
            "username": "@johndoe",
            "email": "john.doe@example.org",
            "first_name": "John",
            "last_name": "Doe",
            "location": "America",
        },
        {
            "username": "@janedoe",
            "email": "jane.doe@example.org",
            "first_name": "Jane",
            "last_name": "Doe",
            "location": "America",
        },
        {
            "username": "@charlie",
            "email": "charlie.johnson@example.org",
            "first_name": "Charlie",
            "last_name": "Johnson",
            "location": "England",
        },
    ]
]

group_fixtures = [{"name": "Default People Club"}]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    help = "Seeds database with sample data"

    # Database 'settings'
    GROUP_COUNT = 50
    USER_COUNT_PER_GROUP = 6

    DEFAULT_PASSWORD = "Password123"

    def __init__(self) -> None:
        self._faker: Faker = Faker("en_GB")

    @staticmethod
    def create_username(first_name: str, last_name: str) -> str:
        """Creates an example username using the first & last name

        :param first_name: The First name
        :param last_name: The Last name, otherwise known as the surname
        :return: The generated username"""
        return f"@{first_name.lower()}{last_name.lower()}"

    @staticmethod
    def create_email(first_name: str, last_name: str) -> str:
        """Creates an example email using the first & last name

        :param first_name: The First name
        :param last_name: The Last name, otherwise known as the surname
        :return: The generated email"""
        return f"{first_name}.{last_name}@example.org"

    def create_user(self) -> User:
        """Uses Faker to create a fake user

        :return: The generated user, which is also saved on the database"""
        first_name = self._faker.first_name()
        last_name = self._faker.last_name()
        username = Command.create_username(first_name, last_name)
        email = Command.create_email(first_name, last_name)
        location = "nowhere"

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            location=location,
            password=Command.DEFAULT_PASSWORD,
        )

    def try_to_create_user(self) -> User | None:
        """Ensures that User creation is aborted if an error occurs"""
        try:
            return self.create_user()
        except Exception:
            pass

    def create_group(self, group_number: int) -> Group:
        """Creates a Group with an assigned number

        :param group_number: Integer value to label the group
        :return: The Created group, that's also held in the database"""
        return Group.objects.create(name=f"Group {group_number}")

    def try_to_create_group(self, group_number: int) -> Group | None:
        """Ensures that Group creation is aborted if an error occurs"""
        try:
            return self.create_group(group_number)
        except Exception:
            pass

    def bind_group_to_user(
        self, user: User, group: Group, is_owner: bool
    ) -> GroupMembership:
        """Creates a GroupMembership record which ties the user to the group

        :param user:
        :param group:
        :param is_owner:

        :return:"""
        return GroupMembership.objects.create(user=user, group=group, is_owner=is_owner)

    def try_to_bind_group_to_user(
        self, user: User, group: Group, is_owner: bool
    ) -> GroupMembership:
        try:
            return self.bind_group_to_user(user, group, is_owner)
        except Exception:
            pass

    def try_and_bind_multiple_users_to_empty_group(
        self, group: Group, user_list: list[User]
    ) -> None:

        owner = self.try_to_bind_group_to_user(user_list[0], group, True)
        other_members = [
            self.try_to_bind_group_to_user(user, group, False) for user in user_list[1:]
        ]

    def create_users_for_groups(self, group: Group) -> None:
        group_users = [
            self.try_to_create_user() for _ in range(Command.USER_COUNT_PER_GROUP)
        ]

        self.try_and_bind_multiple_users_to_empty_group(group, group_users)

    def generate_groups(self) -> None:
        current_group_count = Group.objects.count()
        while current_group_count < Command.GROUP_COUNT:
            print(f"Creating group {current_group_count}/{Command.GROUP_COUNT}")
            current_group: Group = self.try_to_create_group(current_group_count)
            print("\t- Populating group")
            if current_group is not None:
                self.create_users_for_groups()
        print("Seeding complete")

    def generate_fixtures(
        self, user_fixtures: list[list[dict]], group_fixtures: list[dict]
    ) -> None:

        for user_list, group in zip(user_fixtures, group_fixtures, strict=True):
            created_group: Group = Group.objects.get_or_create(**group)
            print(f"Creating group from fixture")
            users_in_group: list[User] = [
                User.objects.get_or_create(**user_details) for user_details in user_list
            ]

            self.try_and_bind_multiple_users_to_empty_group(
                created_group, users_in_group
            )

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.generate_fixtures()
        self.generate_groups()
        return super().handle(*args, **options)
