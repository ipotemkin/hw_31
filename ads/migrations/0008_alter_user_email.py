# Generated by Django 4.0.2 on 2022-03-07 19:42

import ads.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_remove_user_age_alter_user_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, validators=[ads.models.check_domain], verbose_name='Email'),
        ),
    ]