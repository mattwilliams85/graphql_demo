# Generated by Django 2.1.4 on 2021-05-13 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210513_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
