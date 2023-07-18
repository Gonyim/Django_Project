from django.contrib import admin
from django.urls import path
from blog.views import PostListView, PostDetailView, MainView, WritePostView, EditPostView, DeletePostView, SearchPostView, RegisterView, LoginView, MyLoginView, ProfileView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='signup'),  # 회원가입 URL
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('blog/write/', WritePostView.as_view(), name='write_post'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('blog/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('blog/search/<str:tag>/', SearchPostView.as_view(), name='search_post'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
]

