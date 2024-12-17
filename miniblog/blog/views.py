from django.shortcuts import render, HttpResponseRedirect,redirect,get_object_or_404
from .forms import SignUpForm, LoginForm, PostForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post,Comment
from django.contrib.auth.models import User, Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def home(request):
    #posts = Post.objects.all()
    posts = Post.objects.all().prefetch_related('comments')
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': groups})
    else:
        return HttpResponseRedirect('/login/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! You have become an author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                user_password =  form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'LoggedIn successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                post = Post(title=title, description=description)
                post.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                "posts",
                {
                    "type": "handle_new_post",
                    "title": post.title,
                    "description": post.description,
                    "id":post.id
                }
                )
                # channel_layer = get_channel_layer()
                # async_to_sync(channel_layer.group_send)(
                # 'post_updates',
                # {
                #     'type': 'post_update',
                #     'data':
                #             {'action': 'create',
                #                 'post_id': post.id,
                #                 'post_title': post.title,
                #                 'post_description': post.description
                                
                #             }
                                
                # }
                #)
                # form = PostForm()
                return HttpResponseRedirect('/')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                # messages.success(request, 'Data updated')
                return HttpResponseRedirect('/dashboard/')
        else:
            post = Post.objects.get(pk=id)
            form = PostForm(instance=post)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Post.objects.get(pk=id)
            post.delete()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')
    


from django.http import JsonResponse


def add_comments(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Assuming the user is logged in
            comment.save()
            if request.is_ajax():
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment added successfully'
                })
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')



    
    # return render(request, 'blog/home.html', {
    #     'post': post,
    #     'form': form,
    # })

# def add_comments(request,id):
#     print('hi')
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             # Fetch the post and user
#             post = Post.objects.get(id=id)

#             user = User.objects.get(username=request.user.username)

#             # Create and save the comment
#             comment = Comment.objects.create(
#                 post=post,
#                 author=user,
#                 text=request.data['comment_text']
#             )
#             # channel_layer = get_channel_layer()
#             # async_to_sync(channel_layer.group_send)(
#             #         "posts",
#             #         {
#             #             'type': 'handle_comment_message',
#             #             'post_id': post_id,
#             #             'author': request.user.username,
#             #             'text': comment_text,
#             #             'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
#             #         }
#             #         )
#             return HttpResponseRedirect('/')
#         # else:
#         #     form = PostForm()
#         # return render(request, 'blog/addpost.html', {'form': form})
#     else:
#         return HttpResponseRedirect('/login/')