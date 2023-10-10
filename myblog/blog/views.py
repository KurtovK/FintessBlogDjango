from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView

from .forms import UserRegisterForm, PostForm, UserProfileForm, CommentsForm, CategoryForm, FitnessServiceForm
from .models import Post, Comment, UserProfile, FavoritePost, FitnessService, Category


@method_decorator(login_required, name='dispatch')
class PostView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/blog.html', {'posts': posts})

    def blog(request):
        posts = Post.objects.all()
        comments = Comment.objects.select_related('post')
        return render(request, 'blog.html', {'posts': posts, 'comments': comments})


class PostDetailView(View):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        print(comments)
        return render(request, 'blog/posts/post.html', {'post': post, 'comments': comments})


@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    form_class = PostForm
    template_name = 'blog/posts/post_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


class AddCommentView(View):
    def post(self, request, pk):
        form = CommentsForm(request.POST)
        if form.is_valid():
            parent_comment_id = form.cleaned_data.get('parent_comment_id')
            form = form.save(commit=False)
            form.post_id = pk
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                form.parent_comment = parent_comment
            form.save()
        return redirect(f'/posts/{pk}')


class SignUpView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('blog')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/posts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class AddCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'admin/add_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        return render(request, 'admin/add_category.html', {'form': form})


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/posts/post_edit.html'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied()
        return obj

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.id)])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/posts/post_delete.html'
    success_url = reverse_lazy('user_posts')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.filter(author=self.request.user)


class AllPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'admin/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            return Post.objects.none()

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = UserProfile.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect('view_profile')

class ServicesView(View):
    def get(self, request):
        services = FitnessService.objects.all()
        return render(request, 'service/services.html', {'services': services})


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('view_profile')

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class AboutView(View):
    def get(self, request):
        return render(request, 'blog/about_us.html')


@login_required
def favorites_list(request):
    favorite_posts = FavoritePost.objects.filter(user=request.user)
    return render(request, 'blog/favorites/favorites_list.html', {'favorite_posts': favorite_posts})


@require_POST
def favorite_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favorite_post, created = FavoritePost.objects.get_or_create(user=request.user, post=post)
    if not created:
        favorite_post.delete()
    return HttpResponse(status=204)


@login_required
def unfavorite_post(request, pk):
    favorite = get_object_or_404(FavoritePost, pk=pk, user=request.user)
    favorite.delete()
    return redirect('favorites_list')


def search(request):
    query = request.GET.get('q')
    order = request.GET.get('order_by')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)

    if order == 'date':
        posts = posts.order_by('-created_at')
    elif order == 'popularity':
        posts = posts.annotate(popularity=Count('comments')).order_by('-popularity')

    return render(request, 'blog/blog.html', {'posts': posts, 'query': query})


@login_required
def comment_create(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        parent_comment_id = request.POST.get('parent_comment_id')
        email = request.POST.get('email')
        name = request.user.username if request.user.username else 'Anonymous'
        content = request.POST.get('content')

        post = get_object_or_404(Post, id=post_id)
        parent_comment = None
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)

        Comment.objects.create(
            post=post,
            email=email,
            name=name,
            content=content,
            parent_comment=parent_comment
        )

        return redirect(post.get_absolute_url())


@user_passes_test(lambda u: u.is_staff)
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    return redirect(post.get_absolute_url())


class CategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, 'admin/categories.html', {'categories': categories, 'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
        return render(request, 'admin/add_category.html', {'form': form})


class CategoryEditView(LoginRequiredMixin, View):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        form = CategoryForm(instance=category)
        return render(request, 'admin/edit_category.html', {'form': form})

    def post(self, request, id):
        category = get_object_or_404(Category, id=id)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
        return render(request, 'admin/edit_category.html', {'form': form})


class DeleteCategoryView(LoginRequiredMixin, View):
    def post(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return redirect('categories')


class AddFitnessServiceView(View):
    def get(self, request):
        form = FitnessServiceForm(initial={'author': request.user})
        return render(request, 'service/add_service.html', {'form': form})

    def post(self, request):
        form = FitnessServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('services')
        return render(request, 'service/add_service.html', {'form': form})


class EditFitnessServiceView(View):
    def get(self, request, id):
        service = get_object_or_404(FitnessService, id=id)
        form = FitnessServiceForm(instance=service)
        return render(request, 'service/edit_service.html', {'form': form})

    def post(self, request, id):
        service = get_object_or_404(FitnessService, id=id)
        form = FitnessServiceForm(request.POST, instance=service, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('services')
        return render(request, 'service/edit_service.html', {'form': form})


class DeleteFitnessServiceView(View):
    def get(self, request, id):
        service = get_object_or_404(FitnessService, id=id)
        service.delete()
        return redirect('services')

    def post(self, request, id):
        service = get_object_or_404(FitnessService, id=id)
        service.delete()
        return redirect('services')
