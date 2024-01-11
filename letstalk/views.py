from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model, login, logout
from .forms import ProfileForm, LoginForm
from django.contrib import messages
from .models import Profile,Post,LikePost,PostComment,Followers,Messages
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
import time 
from itertools import chain
from random import shuffle, choices
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse, HttpResponse

User = get_user_model()

# Create your views here.
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,password)
            try:
                user = User.objects.get(username=username)
                if user.password==password:
                     login(request, user)
                     return redirect('home')
                else:
                    form = LoginForm()
                    messages.info(request, 'Incorrect Password')
                    return render(request, 'login.html', {'form':form})
            except User.DoesNotExist:
                form = LoginForm()
                messages.info(request,  "username not correct")
                return render(request, 'login.html', {'form':form})

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

def signup(request):
     if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            gender = form.cleaned_data['gender']
            dob = form.cleaned_data['dob']
            print(first_name,last_name,phone_number,password, confirm_password,gender,dob)
            if password!=confirm_password:
                form = ProfileForm()
                messages.info(request,'Password not matching')
                return render(request, 'signup.html', {'form':form})
            else:
                user = User.objects.create(username=phone_number,password=password)
                user.save()
                profile = Profile.objects.create(user=user, id_user=user.id, first_name=first_name, last_name=last_name,gender=gender,dob=dob)
                profile.save()
                return redirect('signin')
     else:
        form = ProfileForm()
     return render(request, 'signup.html', {'form':form})
     
@login_required(login_url='signin')
def home(request):
    user =request.user
    userprofile = Profile.objects.get(user=request.user)
    followers = Followers.objects.filter(following=request.user.username)
    those_i_follow =[those_i_follow.following for those_i_follow in Followers.objects.filter(follower=user.username)]
    users = []
    profiles = []
    for follower in followers:
        pro = User.objects.get(username=follower.follower)
        users.append(pro.username)
    #for user in users:
       # us = Profile.objects.get(user=user)
        #profiles.append(us)
    posts_by_followers = [filter_post for filter_post in Post.objects.all() if filter_post.poster in users or filter_post.poster==user.username]
    print(posts_by_followers)
    user_you_can_follow =[us for us in User.objects.all() if us.username not in those_i_follow and us.username!=user.username]
    profile_of_users_to_follow = [profile for profile in Profile.objects.all() if profile.user in user_you_can_follow]
    if profile_of_users_to_follow == []:
        pass
    else:
        profile_of_users_to_follow = list(set(choices(profile_of_users_to_follow, k=5)))
    likepost = LikePost.objects.filter(userprofile=user.username).all()
    all_likes = LikePost.objects.all()
    print(likepost)
    post_liked = [post.post for post in likepost]
    print(post_liked)
    post_you_like = []
    for post in posts_by_followers:
        for likes in post.likepost_set.all():
            if likes.userprofile==user.username:
                post_you_like.append(likes.post)
        
    print(userprofile)
    context =  {'user':user ,
                'all_post':posts_by_followers,
                  'userprofile':userprofile, 
                  'all_likers':post_you_like,
                  'users_you_can_follow':profile_of_users_to_follow,
                  }
    return render(request, 'home.html', context)
@login_required(login_url='signin')
def setting(request):
    userprofile = Profile.objects.get(user=request.user)
    return render(request, 'setting.html', {'userprofile':userprofile})

def editprofile(request):
     if request.method == 'POST':
        if 'profile_img_edit' in request.POST:
            profile_img = request.FILES['profile_img']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.profile_img = profile_img
            userprofile.save()
            return redirect('setting')
        elif 'cover_img_edit' in request.POST:
            cover_img = request.FILES['cover_img']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.cover_img = cover_img
            userprofile.save()
            return redirect('setting')
        elif 'name_edit' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.first_name = first_name
            userprofile.last_name = last_name
            userprofile.save()
            return redirect('setting')
        elif 'quote_edit' in request.POST:
            favorite_quote = request.POST['bio']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.favorite_quote = favorite_quote
            userprofile.save()
            return redirect('setting')
        elif 'dob_edit' in request.POST:
            dob = request.POST['dob']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.dob = dob
            userprofile.save()
            return redirect('setting')
        elif 'location_edit' in request.POST:
            location = request.POST['location']
            userprofile = Profile.objects.get(user=request.user)
            userprofile.location = location
            userprofile.save()
            return redirect('setting')
        elif 'follow' in request.POST:
            follower = request.POST['follower']
            following = request.POST['following']
            check = Followers.objects.filter(follower=follower,following=following).first()
            if check is not None:
                check.delete()
                return redirect('/profile/' + following + "/")
            else:
                check = Followers.objects.create(follower=follower, following=following)
                check.save()
                return redirect('/profile/' + following + "/")
     return redirect('home')

@login_required(login_url='signin')
def profile(request, username):
    user = User.objects.get(username=username)
    userprofile = Profile.objects.get(user=user)
    logged_in = request.user
    my_posts = Post.objects.filter(poster=user.username)
    user_posts = Post.objects.filter(poster=user.username).count()
    user_profile_follower = Followers.objects.filter(follower=logged_in.username, following=userprofile.user.username).first()
    my_followers = Followers.objects.filter(following=userprofile.user.username).count()
    following = Followers.objects.filter(follower=userprofile.user.username).count()
    print(user_profile_follower)
    # userprofiles = Profile.objects.get(user=request.user)
    followers = Followers.objects.filter(following=user.username)
    following_count = Followers.objects.filter(follower=user.username)
    following_usernames = [following.following for following in following_count]
    friends = [friend for friend in followers if friend.follower in following_usernames]
    #print(followers)
   # print(following_count)
    #print(friends)
    users = []
    profiles = []
    for friend in friends:
        pro = User.objects.get(username=friend.follower)
        users.append(pro)
    for user in users:
        us = Profile.objects.get(user=user)
        profiles.append(us)
    all_posts = Post.objects.all()
    likepost = LikePost.objects.filter(userprofile=logged_in.username).all()
    all_likes = LikePost.objects.all()
    print(likepost)
    post_liked = [post.post for post in likepost]
    print(post_liked)
    post_you_like = []
    for post in all_posts:
        for likes in post.likepost_set.all():
            if likes.userprofile==request.user.username:
                post_you_like.append(likes.post)
    if user_profile_follower is not None:
        btn_text = "unfollow"
    else: 
        btn_text = "follow"
    
    context = {
        'userprofile':userprofile,
        'logged_in':logged_in,
        'btn_text':btn_text,
        'my_posts': my_posts,
        'user_posts':user_posts,
        'my_follower':my_followers,
        'following':following,
        'friends': profiles,
        'all_likers': post_you_like,
    }
    return render(request, 'profile.html',context)
@login_required(login_url='signin')
def post(request):
    user = User.objects.get(username=request.user.username)
    if request.method =='POST':
        if "post_image" not in request.FILES:
             words = request.POST['words']
             new_post = Post.objects.create(poster=user.username, words=words)
             new_post.save()
        elif 'words' not in request.POST:
            post_image = request.FILES['post_image']
            new_post = Post.objects.create(poster=user.username, post_image=post_image)
            new_post.save()
        else:
            words = request.POST['words']
            post_image = request.FILES['post_image']
            new_post = Post.objects.create(poster=user.username, words=words, post_image=post_image)
            new_post.save()
        return redirect('home')
    return render(request, 'create_post.html')
def dologout(request):
    logout(request)
    return redirect('signin')

def likepost(request):
    post_id = request.GET['post']
    user = User.objects.get(username=request.user.username)
    post = Post.objects.get(post_id=post_id)
    likepost = LikePost.objects.filter(post=post, userprofile=user.username).first()
    if likepost is not None:
        likepost.delete()
        post = Post.objects.get(post_id=post_id)
        post.no_of_likes -= 1
        post.save()
        #return redirect('home')
        #return HttpResponse("done")
    else:
        new_like = LikePost.objects.create(post=post, userprofile=user.username)
        new_like.save()
        post = Post.objects.get(post_id=post_id)
        post.no_of_likes += 1
        post.save()
        #return redirect('home')
    post_likes = post.likepost_set.all()
    post_likes_count = post_likes.count()
    usernames_of = [names.userprofile for names in post_likes]
    logged_in_user_liked = user.username in usernames_of
    print(usernames_of)
    print(post_likes_count)
    context = {"count": post_likes_count, "I_liked": logged_in_user_liked}
    return JsonResponse(context)
@login_required(login_url='signin')    
def buddy(request):
    userprofile = Profile.objects.get(user=request.user)
    followers = Followers.objects.filter(following=request.user.username)
    following_count = Followers.objects.filter(follower=request.user.username)
    following_usernames = [following.following for following in following_count]
    friends = [friend for friend in followers if friend.follower in following_usernames]
    #print(followers)
   # print(following_count)
    #print(friends)
    users = []
    profiles = []
    for friend in friends:
        pro = User.objects.get(username=friend.follower)
        users.append(pro)
    for user in users:
        us = Profile.objects.get(user=user)
        profiles.append(us)
    return render(request, 'buddy.html', {'profiles':profiles})
@login_required(login_url='signin')
def search(request):
    query_string = request.GET.get('search')
    match_list = Profile.objects.filter(Q(first_name__icontains=query_string)|Q(last_name__icontains=query_string))
    return render(request, 'search.html', {'search_result':match_list})
@login_required(login_url='signin')
def inbox(request, profile):
    user = request.user
    user_for_profile = User.objects.get(username=profile)
    userprofile = Profile.objects.get(user=user_for_profile)
    if request.method == "POST":
        if "picture-msg" in request.POST:
            image_message = request.FILES['picture-msg']
            profile = request.POST['profile']
            user_for_profile = User.objects.get(username=profile)
            userprofile = Profile.objects.get(user=user_for_profile)
            new_message = Messages.objects.create(sender=user, receiver=user_for_profile, image_message=image_message)
            new_message.save()
            return HttpResponse("message was sent")
            #return redirect('/inbox/' + userprofile.user.username)
        elif "msg" in request.POST:
            text_message = request.POST['msg']
            profile = request.POST['profile']
            user_for_profile = User.objects.get(username=profile)
            userprofile = Profile.objects.get(user=user_for_profile)
            new_message = Messages.objects.create(sender=user, receiver=user_for_profile, text_message=text_message)
            new_message.save()
            return HttpResponse("message sent successfully")
            #return redirect('/inbox/' + userprofile.user.username)

    
    return render(request, 'chat.html', {'userprofile':userprofile})

def getmessage(request, profile_id):
    user = request.user
    user_for_profile = User.objects.get(username=profile_id)
    userprofile = Profile.objects.get(user=user_for_profile)
    if Messages.objects.filter(Q(sender=user, receiver=user_for_profile)|Q(sender=user_for_profile, receiver=user)).count()<=10:
        last_ten_messages = list(Messages.objects.filter(Q(sender=user, receiver=user_for_profile)|Q(sender=user_for_profile, receiver=user)).all().values_list())
    else:
        last_ten_messages = list(Messages.objects.order_by('-created')\
                                 .filter(Q(sender=user, receiver=user_for_profile)|Q(sender=user_for_profile, receiver=user))[:10].values_list())
        last_ten_messages.reverse()

   
    #print(last_ten_messages)

    data = last_ten_messages
    return JsonResponse({'data':data})

def post_comment(request, post_id):
    if request.method == "POST":
        post_id = request.POST['post_id']
        userprofile = request.POST['userprofile']
        comment = request.POST['comment']
        post = Post.objects.filter(post_id=post_id).first()
        comment = PostComment.objects.create(post_id=post, userprofile=userprofile, comments=comment)
        comment.save()
        return redirect('/post_comment/' + post_id + "/")

    single_post = Post.objects.filter(post_id=post_id).first()
    print(single_post)
    all_comments = single_post.post.all()
    print(all_comments)
    user =request.user
    userprofile = Profile.objects.get(user=request.user)
    followers = Followers.objects.filter(following=request.user.username)
    those_i_follow =[those_i_follow.following for those_i_follow in Followers.objects.filter(follower=user.username)]
    users = []
    profiles = []
    for follower in followers:
        pro = User.objects.get(username=follower.follower)
        users.append(pro.username)
    #for user in users:
       # us = Profile.objects.get(user=user)
        #profiles.append(us)
    posts_by_followers = [filter_post for filter_post in Post.objects.all() if filter_post.poster in users or filter_post.poster==user.username]
    print(posts_by_followers)
    likepost = LikePost.objects.filter(userprofile=user.username).all()
    all_likes = LikePost.objects.all()
    # print(likepost)
    post_liked = [post.post for post in likepost]
    # print(post_liked)
    post_you_like = []
    for post in posts_by_followers:
        for likes in post.likepost_set.all():
            if likes.userprofile==user.username:
                post_you_like.append(likes.post)
    return render(request, 'post_detail.html', {'single_post': single_post, 'all_likers': post_you_like, 'comments': all_comments})

def replies(request, comment_id):
    comment = PostComment.objects.filter(id=comment_id).first()
    post = comment.post_id
    total_rep = comment.replies.count()
    has_reply = comment.replies.count() >= 1
    if request.method == "POST":
        userprofile = request.POST['userprofile']
        reply = request.POST['reply']
        new_reply = PostComment.objects.create(post_id=post, userprofile=userprofile, comments=reply, reply=comment)
        new_reply.save()
        return redirect('/replies/' + comment_id + "/")
    return render(request, 'comment_replies.html', {'comment': comment, 'has_reply': has_reply, 'total_rep': total_rep})




















