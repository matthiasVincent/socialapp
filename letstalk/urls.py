from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('setting/', views.setting, name="setting"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('post/', views.post, name="post"),
    path('dologout/', views.dologout, name="dologout"),
    path('likepost/', views.likepost, name="likepost"),
    path('editprofile/', views.editprofile, name="editprofile"),
    path('buddy/', views.buddy, name="buddy"),
    path('search/', views.search, name="search"),
    path('inbox/<str:profile>/', views.inbox, name="inbox"),
    path('getmessage/<str:profile_id>/', views.getmessage, name="getmessage"), 
    path('post_comment/<str:post_id>/', views.post_comment, name="post_comment"),
    path('replies/<str:comment_id>/', views.replies, name="replies"),
    #path('profile/<str:username>', views.profile_page, name="profile_page"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
Some random accounts
Abah Gina, 09076728687
Ogirah Blessing, 07080025104
Labidi Tony Akwaba, 09029611290
Onoja Austine, 08139449669
Attah Ayoh Afemikhe, 08188985677
Matthias Blessing, 09034786178
Blessed Dan, 08084631861
Okpe Ken, 08072554695
Daniel Onoja, 0810478656
Udenyi Joseph Owoche, 08167066876
Ochogwu Ekondu Lucy, 09024299532
Ella Mary, 09052923979

"""