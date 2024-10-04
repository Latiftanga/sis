from django import forms
from core.models import (
    Teacher, Address
)

class TeacherForm(forms.ModelForm):
    """Staff Creation form"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field] \
                .widget.attrs['class'] = 'form-control'

    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ('user', )


class TeacherContactInfoForm(forms.ModelForm):
    create_account = forms.ChoiceField(
        choices = (
            (True, 'Yes'), (False, 'No')
        ),
        widget=forms.RadioSelect,
        label='Add User Acccount?'
    )
    class Meta:
        model = Address
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        create_account = cleaned_data.get("create_account")
        email = cleaned_data.get('email')

        # If user chooses to create an account, email must be provided
        if create_account and not email:
            self.add_error('email', "Email is required when creating an account.")
