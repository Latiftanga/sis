from django.db import models
from core.models import Person
from django.contrib.auth import get_user_model


class Teacher(Person):
    """Teaching staff in the system"""
    TITLES = (
        (
            ("Dr.", "Dr."), ("Dr.", "Dr."), ("Hon", "Hon"),
            ("Hon.", "Hon."), ("Lord", "Lord"), ("Md.", "Md."),
            ("Ms", "Ms"), ("Mr.", "Mr."), ("Mrs.", "Mrs."),
            ("Prof", "Prof"), ("Prof", "Prof"), ("Rev", "Rev"),
            ("Rev.", "Rev."), ("Sir", "Sir"),
        )
    )
    title = models.CharField(max_length=32, choices=TITLES)
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='teacher_profile'
    )

    def get_full_name(self):
        if len(self.other_names) > 0:
            return f'{self.first_name.capitalize} {self.last_name} {self.other_names}'
        else:
            return f'{self.first_name.capitalize} {self.last_name.capitalize}'

    def __str__(self):
        return self.get_full_name
