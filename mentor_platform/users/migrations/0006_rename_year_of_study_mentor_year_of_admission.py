# Generated by Django 5.1.1 on 2024-10-14 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_mentee_budget_alter_mentee_college_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentor',
            old_name='year_of_study',
            new_name='year_of_admission',
        ),
    ]