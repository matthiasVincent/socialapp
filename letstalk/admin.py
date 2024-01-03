from django.contrib import admin
from .models import Profile,Post,LikePost,PostComment,Followers, Messages, Coversation, ChatInbox

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','id_user', 'first_name', 'last_name','Phone_number','gender']

class PostAdmin(admin.ModelAdmin):
    list_display =['post_id', 'poster', 'no_of_likes', 'no_of_comments', 'created']

class LikePostAdmin(admin.ModelAdmin):
    llist_display =['post_id', 'userprofile', 'created']

class PostCommentAdmin(admin.ModelAdmin):
    list_display =['post_id', 'userprofile', 'created', 'comments']

class ChatRoomsAdmin(admin.ModelAdmin ):
    list_display =['follower', 'following', 'created']

class MessageAdmin(admin.ModelAdmin):
    list_display =['chat_room', 'sender', 'created']

class FollowerAdmin(admin.ModelAdmin):
    list_display =['follower', 'following', 'created']
    list_display_links = None

class MessageAdmin(admin.ModelAdmin):
    list_display=['sender', 'receiver', 'text_message', 'created']
    list_display_links=None


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(Followers, FollowerAdmin)
admin.site.register(Messages, MessageAdmin)
admin.site.register(Coversation)
admin.site.register(ChatInbox)
""" admin.site.register(ChatRooms, ChatRoomsAdmin)
admin.site.register(Messages, MessageAdmin)
admin.site.register(Followers, FollowerAdmin) """