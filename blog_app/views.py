from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Posts
from .forms import PostsForm


def post_list(request):
    template_name = 'post_list.html'
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request, template_name, context)


def post_create(request):
    if request.method == 'POST':
        form = PostsForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            messages.success(request, 'O post foi criado com sucesso')
            return HttpResponseRedirect(reverse('post_list'))

    form = PostsForm()
    return render(request, 'post_form.html', {"form": form})


def post_detail(request, id):
    template_name = 'post_detail.html'
    post = Posts.objects.get(id=id)
    context = {
        'post': post
    }
    return render(request, template_name, context)


def post_update(request, id):
    post = get_object_or_404(Posts, id=id)
    form = PostsForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()

        messages.warning(request, 'O post foi atualizado com sucesso')
        return HttpResponseRedirect(reverse('post_detail', args=[post.id]))

    return render(request, 'post_form.html', {"form": form})


def post_delete(request, id):
    post = Posts.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        messages.error(request, 'O post foi deletado com sucesso')
    return render(request, 'post_delete.html')
