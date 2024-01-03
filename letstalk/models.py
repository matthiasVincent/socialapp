from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from uuid import uuid4
from datetime import datetime

# Create your models here.
User = get_user_model()
GENDER = (('MALE', 'MALE'), ('FEMALE', 'FEMALE'))

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    Phone_number = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    favorite_quote = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=30)
    profile_img = models.ImageField(upload_to="profile_pictures", default="blank-profile-picture.png")
    cover_img = models.FileField(upload_to="cover_pictures", default="blank-profile-picture.png")
    dob = models.DateField(blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)



class Followers(models.Model):
    follower = models.CharField(max_length=50)
    following = models.CharField(max_length=50)
    created = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return "{} following {}".format(self.follower, self.following)

class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid4)
    poster = models.CharField(max_length=50)
    words = models.TextField(max_length=1000000)
    post_image = models.ImageField(blank=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.poster
    
    @property
    def full_name(self):
        user = User.objects.get(username=self.poster)
        user_profile = Profile.objects.get(user=user)
        return "{} {}".format(user_profile.first_name, user_profile.last_name)
    
    @property
    def poster_image(self):
        user = User.objects.get(username=self.poster)
        user_profile = Profile.objects.get(user=user)
        return user_profile
    @property
    def followers(self):
        user = User.objects.get(username=self.poster)
        user_profile = Profile.objects.get(user=user)
        followers = Followers.objects.filter(following=user_profile.user.username).count()
        return followers

        

class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='d735e027-33b6-48f7-841e-55102046037e')
    userprofile = models.CharField(max_length=50)
    created = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.userprofile 

class PostComment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    userprofile = models.CharField(max_length=50)
    comments = models.TextField(max_length=1000000)
    reply = models.ForeignKey("self",on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(default=datetime.now)

    @property
    def commenter(self):
        user = User.objects.get(username=self.userprofile)
        user_profile = Profile.objects.get(user=user)
        return user_profile
    
    @property
    def replies(self):
        all_reply = PostComment.objects.filter(reply=self).all()
        return all_reply
    @property
    def rep_count(self):
        all_rep = PostComment.objects.filter(reply=self).all().count()
        return all_rep




    def __str__(self):
        return self.userprofile
    
class Coversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room_name = models.CharField(max_length=100)
    online_users = models.ManyToManyField(to=User, blank=True)

    def get_online_users(self):
        return self.online_users.count()
    
    def join(self, user):
        self.online_users.add(user)
        self.save()
    
    def leave(self, user):
        self.online_users.remove(user)
        self.save()

    def __str__(self):
        return "{} ({})".format(self.room_name, self.get_online_users())

class ChatInbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Messages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room_name = models.ForeignKey(ChatInbox, on_delete=models.CASCADE, related_name="chat_room")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    text_message = models.TextField()
    image_message = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return "from {} to {}".format(self.sender.username, self.receiver.username)

    
"""class Messages(models.Model):
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    text_message = models.TextField(max_length=100000, blank=True)
    image_message = models.ImageField(blank=True)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "{}".format(self.sender)

    
class ChatRooms(models.Model):
    follower= models.CharField(max_length=50)
    following = models.CharField(max_length=50)
    created = models.DateTimeField(default=datetime.now)

    def __st__(self):
        return "{} following {}".format(self.follower, self.following)

 class BuddyMessage(models.Model):
    buddy = models.CharField(max_length=50)
    message = models.TextField(max_length=100000, blank=True)
    img_msg = models.ImageField(blank=True)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.buddy
    
class UserMessage(models.Model):
    user = models.CharField(max_length=50)
    message = models.TextField(max_length=100000, blank=True)
    img_msg = models.ImageField(blank=True)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user 
        NB: Any message sent will first check whether the chat channel 
        already exists and forward the message according otherwise it creat the chat channel
        before message is created
        
class Messages(models.Model):
    chat_room = models.ForeignKey(ChatRooms, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    text_message = models.TextField(max_length=100000, blank=True)
    image_message = models.ImageField(blank=True)
    created = models.DateTimeField(default=datetime.now)

    def __st__(self):
        return self.sender
 """



    

