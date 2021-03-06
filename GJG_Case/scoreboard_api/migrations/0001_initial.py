# Generated by Django 3.0.5 on 2020-04-15 16:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=64)),
                ('points', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=None)),
                ('country', models.CharField(default='UN', max_length=2)),
            ],
        ),
    ]
