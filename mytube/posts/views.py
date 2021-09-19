from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.http.response import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Comments, Post, Group, User, Follow
from .forms import ContactForm, AddPostForm, AddCommentForm
from django.views.decorators.cache import cache_page
# Create your views here.


# @login_required
# Декоратор бэкэнда кэширования. Указываем время в секундах сколько хранить в Каше
# @cache_page(20)
def index(request):
    page_number = request.GET.get('page', None)
    search_keyword = request.GET.get("q", None)
    if search_keyword:
        posts = Post.objects.select_related('author', 'groups').filter(text__contains=search_keyword)
    else:
        posts = Post.objects.select_related().all().order_by('-pub_date')
    paginator = Paginator(posts, 5)
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'posts':page , 'keyword':search_keyword, 'paginator':paginator} )


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # form.clean_subject()

        if form.is_valid():
            return redirect('/thank-you/')
        return render(request, 'contact.html', {'form': form})

    elif request.method == 'GET':
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

@login_required
def add_new_post(request):
    event_title = 'Отправить новый пост на стену:'

    if request.method == 'GET':
        form = AddPostForm(author=request.user, files=request.FILES or None)
        return render(request, 'new_post.html', {'form': form, 'event_title': event_title, 
                                                    'button_title':'Отправить'})
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, author=request.user,files=request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('/')        
        return render(request, 'new_post.html', {'form': form, 'event_title': event_title, 
                                                    'button_title':'Отправить'})



def group_posts(request, slug):
    community = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group = community).order_by("-pub_date")[:12]

    return render(request, 'group.html', {"community": community, "posts": posts}) 

def profile(request, username):
    page = request.GET.get('page', None)
    posts = Post.objects.filter(author__username = username).order_by("-pub_date")
    username_ = get_object_or_404(User, username = username)
    posts_paginator = Paginator(posts, 5)
    posts = posts_paginator.get_page(page)
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user = request.user, author__username = username):
            following = True
    return render(request, 'profile.html', {'posts': posts,
                                             'posts_paginator': posts_paginator, 
                                             'username': username_,
                                             'following': following, })


def post_view(request, username, post_id):
        post = get_object_or_404(Post, id = post_id)
        username_ = get_object_or_404(User, username = username)
        comments = post.post_comments.all()

        return render(request, 'post.html', {'post': post, 'username': username_, 'comments':comments})

@login_required
def post_edit(request, username, post_id):
        event_title = 'Отредактируйте пост:'
        # if request.user.get_username() != username:
        #     raise Http404('Вы не создатель этой записи!')
        
        post = Post.objects.get(id=post_id)

        if request.method == 'GET':
            form = AddPostForm(instance=post, author=username, files=request.FILES or None)
            return render(request, 'new_post.html', {'form': form, 'event_title': event_title, 
                                                    'button_title':'Сохранить', 'post_id':post_id})
        if request.method == 'POST':
            form = AddPostForm(request.POST, author=request.user , files=request.FILES or None)
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.groups = form.cleaned_data['groups']
                post.image = form.cleaned_data['image']
                post.save()
                return redirect(f'/{request.user}/')        
            return render(request, 'new_post.html', {'form': form, 'event_title': event_title, 
                                                    'button_title':'Отправить', 'post_id':post_id})


def page_not_found(request,exception):
    # exception - отладочная информация
    return render(request, 'misc/404.html', {'path': request.path}, status=404)

def server_error(request):
    return render(request, 'misc/500.html', status=500)

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id = post_id)
    username_ = get_object_or_404(User, username = username)

    if request.method == 'GET':
        form = AddCommentForm()
        comments = post.post_comments.all()
        return render(request, 'post.html', {'post': post, 
                                            'username': username_, 
                                            'form': form, 
                                            'comments':comments})
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(text = form.cleaned_data['text'],
                                              author = request.user,
                                              post = post)
        
        return HttpResponseRedirect(reverse('post', kwargs={'username':username, 'post_id':post_id}))
    

@login_required
def follow_index(request):
    page_number = request.GET.get('page', None)
    authors = request.user.follower.all().values('author')
    print(authors)
    posts = Post.objects.filter(author__in=authors).order_by('-pub_date')
    paginator = Paginator(posts, 5)
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'posts':page , 'paginator':paginator})

@login_required
def profile_follow(request, username):
    Follow.objects.create(user=request.user, author=User.objects.filter(username=username)[0])
    return HttpResponseRedirect(reverse('profile',kwargs={'username':username}))

@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(user=request.user, author=User.objects.filter(username=username)[0]).delete()
    return HttpResponseRedirect(reverse('profile', kwargs={'username':username}))
