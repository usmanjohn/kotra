# Generated by Django 5.0.6 on 2024-06-25 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userprofile_facebook_url_userprofile_instagram_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='link_image',
            field=models.ImageField(default='links/personal_profile.png', upload_to='links'),
        ),
    ]