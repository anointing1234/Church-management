# Generated by Django 5.2.1 on 2025-05-26 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_membershipchurch1_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/profile_pic.webp', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='juniorchurchchurch1',
            name='church_type',
            field=models.CharField(choices=[('both', 'Children & Teens Church')], max_length=10),
        ),
        migrations.AlterField(
            model_name='juniorchurchchurch2',
            name='church_type',
            field=models.CharField(choices=[('both', 'Children & Teens Church')], max_length=10),
        ),
    ]
