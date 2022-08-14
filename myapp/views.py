from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, HashtagForm
from django.utils import timezone
from .models import Post, Comment, Hashtag
from django.http import request



# Create your views here.

def main(request):
    return render(request, 'main.html')

def write(request, blog = None):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
            form.save_m2m()
            return redirect('read')
    else:
        form = PostForm (instance = blog)
        return render(request, 'write.html', {'form':form})

def read(request):
    blogs = Post.objects
    return render(request, 'read.html', {'blogs':blogs})

def detail(request, id):
    blog = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(request.POST)
            comment.blog_id = blog
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('detail', id)
    else:
        form = CommentForm()
        return render(request, 'detail.html', {'blog':blog, 'form':form})

def edit(request, id):
    blog = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm (request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save(commit=False)
            form.pub_date = timezone.now()
            form.save()
            return redirect('read')

    else:
        form = PostForm(instance=blog)
        return render(request, 'edit.html', {'form': form})

def delete(request, id):
    blog = get_object_or_404(Post, id=id)
    blog.delete()
    return redirect('read')

def hashtag(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance = hashtag)
        if form.is_valid():
            hashtag = form.save(commit =False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message="이미 존재하는 해시태그 입니다"
                return render(request, 'hashtag.html', {'form':form, "error_message": error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('read')

    else:
        form = HashtagForm (instance = hashtag)
        return render(request, 'hashtag.html', {'form':form})
            

