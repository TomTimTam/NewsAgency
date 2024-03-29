# Generated by Django 2.2.4 on 2019-08-15 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='NewsStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=64)),
                ('story_datetime', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(max_length=512)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='API.Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='API.Category')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='API.Region')),
            ],
        ),
    ]
