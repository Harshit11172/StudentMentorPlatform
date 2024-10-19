# Generated by Django 5.1.1 on 2024-10-14 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_is_verified_customuser_verification_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='college_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='degree',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='desired_expertise',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='major',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='university',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mentee',
            name='year_of_study',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='college_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='degree',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='entrance_exam_given',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='expertise',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='major',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='session_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='university',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='year_of_study',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
