# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Post
from .forms import PostForm


class SearchPostView(ListView):
    model = Post
    template_name = 'search_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(Q(title__contains=tag) | Q(content__contains=tag))


class DeletePostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')
    

class EditPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    

@method_decorator(login_required, name='dispatch')
class WritePostView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'write_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
        return render(request, 'write_post.html', {'form': form})
    

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class MainView(TemplateView):
    template_name = 'main.html'


class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        # 실제 회원가입 로직을 여기에 추가
        # 회원가입 폼의 입력 값을 받아서 적절한 처리를 수행해야 합니다.
        # 예를 들어, 회원 정보를 저장하고 로그인 페이지로 이동하도록 할 수 있습니다.
        return redirect('login')  # 회원가입 후 로그인 페이지로 이동


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 실제 로그인 로직을 여기에 추가
        return redirect('main')  # 로그인 완료 후 메인 페이지로 이동