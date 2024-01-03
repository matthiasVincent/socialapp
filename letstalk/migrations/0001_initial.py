# Generated by Django 4.2.2 on 2023-12-31 21:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatInbox',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=50)),
                ('following', models.CharField(max_length=50)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('poster', models.CharField(max_length=50)),
                ('words', models.TextField(max_length=1000000)),
                ('post_image', models.ImageField(blank=True, upload_to='')),
                ('no_of_likes', models.IntegerField(default=0)),
                ('no_of_comments', models.IntegerField(default=0)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('Phone_number', models.CharField(max_length=30)),
                ('bio', models.TextField(blank=True)),
                ('favorite_quote', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('profile_img', models.ImageField(default='blank-profile-picture.png', upload_to='profile_pictures')),
                ('cover_img', models.FileField(default='blank-profile-picture.png', upload_to='cover_pictures')),
                ('dob', models.DateField(blank=True)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userprofile', models.CharField(max_length=50)),
                ('comments', models.TextField(max_length=1000000)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='letstalk.post')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='letstalk.postcomment')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text_message', models.TextField()),
                ('image_message', models.ImageField(blank=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('room_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_room', to='letstalk.chatinbox')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userprofile', models.CharField(max_length=50)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('post', models.ForeignKey(default='d735e027-33b6-48f7-841e-55102046037e', on_delete=django.db.models.deletion.CASCADE, to='letstalk.post')),
            ],
        ),
        migrations.CreateModel(
            name='Coversation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=100)),
                ('online_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
