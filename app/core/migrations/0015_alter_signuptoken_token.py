# Generated by Django 5.0.8 on 2024-09-20 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_signuptoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signuptoken',
            name='token',
            field=models.CharField(default='GPZVDXUUEY', editable=False, unique=True),
        ),
    ]
