from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import PostCreateView, UserPostListView, PostUpdateView, PostDeleteView, AllPostsListView, UserProfileView, \
    EditProfileView, favorites_list, unfavorite_post, ServicesView, DeleteCategoryView, \
    CategoryListView, CategoryEditView, AddCategoryView, AddFitnessServiceView, EditFitnessServiceView, \
    DeleteFitnessServiceView

urlpatterns = [
    path('', views.PostView.as_view(), name='blog'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('user_posts/', UserPostListView.as_view(), name='user_posts'),
    path('all_posts/', AllPostsListView.as_view(), name='all_posts'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),

    path('profile/', UserProfileView.as_view(), name='view_profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),

    path('search/', views.search, name='search'),

    path('review/<int:pk>', views.AddCommentView.as_view(), name='add_comment'),
    path('comment_create/', views.comment_create, name='comment_create'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    path('favorites/', favorites_list, name='favorites_list'),
    path('favorite_post/<int:post_id>', views.favorite_post),
    path('favorites/<int:pk>/unfavorite/', unfavorite_post, name='unfavorite_post'),

    path('about/', views.AboutView.as_view(), name='about_us'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('edit_category/<int:id>/', CategoryEditView.as_view(), name='edit_category'),
    path('delete_category/<int:id>/', DeleteCategoryView.as_view(), name='delete_category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),

    path('services/', ServicesView.as_view(), name='services'),
    path('add_service/', AddFitnessServiceView.as_view(), name='add_service'),
    path('edit_service/<int:id>/', EditFitnessServiceView.as_view(), name='edit_service'),
    path('delete_service/<int:id>/', DeleteFitnessServiceView.as_view(), name='delete_service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
