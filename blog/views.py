from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Post, Category, Comment, User
from .forms import PostForm, CommentForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

# Create your views here.


# check addition !!!!!!!
def category(request, id=None):
    c = get_object_or_404(Category, pk=id)
    posts = Post.objects.filter(category=c).order_by('-published_date')
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
    user = User.objects.get(pk=id)
    return render(request, 'blog/profile.html', {'user': user})