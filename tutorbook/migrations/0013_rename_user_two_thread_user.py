# Generated by Django 4.1.2 on 2022-10-16 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorbook', '0012_remove_thread_user_one_thread_tutor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='user_two',
            new_name='user',
        ),
    ]