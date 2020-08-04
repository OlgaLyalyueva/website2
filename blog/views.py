from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .models import Post, Category, Comment, User, Avatar
from .forms import PostForm, CommentForm, ProfileForm, RegistrationForm, AvatarForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

# Create your views here.


def category(request, id=None):
    c = get_object_or_404(Category, pk=id)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    print(len(posts))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def author(request, id=None):
    u = get_object_or_404(User, pk=id)
    posts = Post.objects.filter(user_id=u).order_by('-published_date')
    print(len(posts))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def get_categories():
    categories = Category.objects.all()
    count = categories.count()
    half = int(count / 2) + 1
    first_half = categories[:half]
    second_half = categories[half:]
    return {'cat1': first_half, 'cat2': second_half}


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    comments = Comment.objects.all().order_by('-published_date')
    context = {'posts': posts, 'comments': comments}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def post(request, id=None):
    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(fk_post = id).order_by('-published_date')
    url = request.path
    context = {'post': post, 'comments': comments, 'url': url}
    context.update(get_categories())
    return render(request, 'blog/post.html', context)


def search(request):
    # print(request.method)
    # print(request.POST)
    if request.method == 'POST':
        query = request.POST['query']
        posts = Post.objects.filter(content__icontains = query).order_by('-published_date')
    else:
        posts = []
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return redirect('index')

    form = PostForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'blog/add_post.html', context)


def add_comment(request, id=None):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.published_date = now()
            comment.fk_post = post
            comment.save()
            return redirect('post', id=post.pk)

    form = CommentForm()
    context = {'form': form, 'post': post}
    context.update(get_categories())
    return render(request, 'blog/add_comment.html', context)


def profile(request, id=None):
    post = Post.objects.filter(user_id=id)
    user = User.objects.get(pk=id)
    try:
        avatar = Avatar.objects.get(fk_user_id=id)
    except:
        avatar = 'Null'
    count_posts = Post.objects.filter(user_id=id).count()
    today = now()
    count_days = (today - user.date_joined).days
    context = {'post': post, 'user': user, 'avatar': avatar, 'count_posts': count_posts, 'count_days': count_days}
    context.update(get_categories())
    return render(request, 'blog/profile.html', context)


def update_profile(request, id=None):
    post = Post.objects.filter(user_id=id)
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        avatar = Avatar.objects.get(fk_user=id)
        form = ProfileForm(request.POST, instance=user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            if avatar_form.is_valid():
                avatar_form.fk_user = user.id
                avatar_form.save()
                form.save()
                return redirect('profile', id=user.pk)
    user = User.objects.get(pk=id)
    form = ProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    try:
        avatar = Avatar.objects.get(fk_user=id)
    except:
        a = Avatar()
        a.fk_user_id = id
        a.save()
        avatar = Avatar.objects.get(fk_user=id)
    avatar_form = AvatarForm(initial={'avatar': avatar.avatar})
    context = {'post': post, 'user': user, 'form': form, 'avatar_form': avatar_form}
    context.update(get_categories())
    return render(request, 'blog/update_profile.html', context)




def users_posts(request, id=None):
    user = get_object_or_404(User, pk=id)
    posts = Post.objects.filter(user_id=user).order_by('-published_date')
    print(len(posts))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def delete_post(request, id=None):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context = {'post': post}
    context.update(get_categories())
    return render(request, 'blog/delete_post.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.date_joined = now()
            form.save()
            mes = 'Successful registration. Please sign in!'
            context = {'mes': mes}
            context.update(get_categories())
            return render(request, 'registration/register.html', context)
        else:
            context = {'form': form}
            context.update(get_categories())
            return render(request, 'registration/register.html', context)
    form = RegistrationForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'registration/register.html', context)
