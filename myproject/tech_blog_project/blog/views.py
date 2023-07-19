from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required  # 추가
from django.utils.decorators import method_decorator  # 추가
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Post
from .forms import PostForm


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')


class SearchPostView(ListView):
    model = Post
    template_name = 'search_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(Q(title__contains=tag) | Q(content__contains=tag))


@method_decorator(login_required, name='dispatch')
class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # 해당 게시글의 작성자와 로그인한 사용자가 일치하는지 확인
        if post.author != request.user:
            raise Http404("존재하지 않는 게시글입니다.")  # 본인의 게시글이 아니라면 404 오류 반환
        post.delete()
        return redirect('post_list')
    

@method_decorator(login_required, name='dispatch')
class EditPostView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # 해당 게시글의 작성자와 로그인한 사용자가 일치하는지 확인
        if post.author != request.user:
            return redirect('post_list')  # 본인의 게시글이 아니라면 목록 페이지로 이동
        form = PostForm(instance=post)
        return render(request, 'edit_post.html', {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # 해당 게시글의 작성자와 로그인한 사용자가 일치하는지 확인
        if post.author != request.user:
            return redirect('post_list')  # 본인의 게시글이 아니라면 목록 페이지로 이동
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    

class WritePostView(View):
    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        form = PostForm()
        return render(request, 'write_post.html', {'form': form})

    @method_decorator(login_required, name='dispatch')
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Remove commit=False
            post.author = request.user
            post.save()  # Save the post directly to the database
            return redirect('post_list')
        return render(request, 'write_post.html', {'form': form})
    

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(deleted=False)  # 삭제되지 않은 게시물만


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.deleted:
            raise Http404("존재하지 않는 게시글입니다.")
        return obj


class MainView(TemplateView):
    template_name = 'main.html'


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('post_list')
        return render(request, 'register.html', {'form': form})


class MyLoginView(LoginView):
    template_name = 'login.html'
