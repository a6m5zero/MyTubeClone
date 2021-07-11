from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Group
from .forms import ContactForm, AddPostForm
# Create your views here.


# @login_required
def index(request):

    search_keyword = request.GET.get("q", None)
    print(search_keyword)
    if search_keyword:
        posts = Post.objects.select_related('author', 'groups').filter(text__contains=search_keyword)
    else:
        posts = Post.objects.select_related().all()

    return render(request, 'index.html', {'posts':posts , 'keyword':search_keyword})


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
    if request.method == 'GET':
        form = AddPostForm(author=request.user)
        return render(request, 'new_post.html', {'form': form})
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, author=request.user)
        if form.is_valid:
            form.save()
            return redirect('/')        
        return render(request, 'new_post.html', {'form':form})


def group_posts(request, slug):
    community = get_object_or_404(Group, slug = slug)
    posts = Post.objects.filter(group = community).order_by("-pub_date")[:12]

    return render(request, 'group.html', {"community": community, "posts": posts}) 