# Generated by Django 5.1.1 on 2024-10-07 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_authenticated',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_mentor',
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('mentor', 'Mentor'), ('mentee', 'Mentee')], default='mentee', max_length=6),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='users_user_set', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='users_user_permissions', to='auth.permission'),
        ),
    ]
