from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm, PostEditForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


def post_list(request):
    post_list = Post.objects.all().order_by('-id')
    query = request.GET.get('query')
    if query:
        post_list = Post.objects.filter(
        Q(title__contains=query)|
        Q(body__contains=query) |
        Q(author__username = query)
        )

    paginator = Paginator(post_list,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'post_list.html',{'posts':posts})

def post_detail(request,id,slug):
    post = Post.objects.get(id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    return render(request,'post_detail.html',{'post':post,'is_liked':is_liked,'total_likes':post.total_likes()})

def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            messages.success(request, "Post was created Successfully")
            return redirect('post_list')

        else:
            form = PostCreateForm()
            context = {'form':form}
            return render(request, 'post_create.html',context)
    form = PostCreateForm()
    context = {'form':form}
    return render(request,'post_create.html',context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse('User is Not Active')
            else:
                form = UserLoginForm()
                messages.warning(request, "Username or Password Incorrect")
                return render(request, 'login_file.html', {'form': form})
    else:
        form = UserLoginForm()
        return render(request, 'login_file.html',{'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, "You LoggedOut Successfully")
    return redirect('post_list')


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user =form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('user_login')
        else:
            return HttpResponse("Invalid Details")
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form':form})

def like_post(request):
    id=request.POST.get('post_id')
    post = get_object_or_404(Post, id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == "POST":
        form = PostEditForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            messages.warning(request, "Your post was Updated Successfully")
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
        return render(request, 'post_edit.html',{'form':form})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return Http404
    post.delete()
    messages.success(request, "Your Post was deleted Succesfully..")
    return redirect('post_list')



