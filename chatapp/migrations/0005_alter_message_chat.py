# Generated by Django 5.2.1 on 2025-07-09 09:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(db_column='fromchat', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatapp.chat'),
        ),
    ]
