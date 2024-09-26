# Generated by Django 4.1.13 on 2024-09-26 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app_senauthenticator', '0004_alter_usuario_groups_alter_usuario_user_permissions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_when', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(db_column='usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
