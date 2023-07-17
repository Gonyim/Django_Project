# tech_blog_project/urls.py
from django.contrib import admin
from django.urls import path
from blog.views import PostListView, PostDetailView, MainView, WritePostView, EditPostView, DeletePostView, SearchPostView, RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', PostListView.as_view(), name='post_list'),  # 이 부분을 주석 처리하거나 삭제하세요.
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('', MainView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='signup'),  # SignUpView -> RegisterView로 변경
    path('login/', LoginView.as_view(), name='login'),
    path('blog/write/', WritePostView.as_view(), name='write_post'),
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),
    path('blog/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    path('blog/search/<str:tag>/', SearchPostView.as_view(), name='search_post'),
]
