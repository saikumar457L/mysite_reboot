from django.shortcuts import render,get_object_or_404


from .models import Post
from .forms import EmailPost,CommentForm

from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic.edit import CreateView
from django.views.generic import ListView

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    paginate_by = 2

    """ rember must use page_obj for getting pages """



def post_detail (request,object_id):
    post = get_object_or_404(Post,id=object_id)

    # getting all comments
    comments = post.comments.filter(active=True)[:3] # Here the comments from the related_name defined in Comment model in First line

    new_comment = None

    if request.method == "POST":
        # Comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post # Assigning the current post to comment
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render (request,"blog/detail.html",{"post":post,"comments":comments,"new_comment":new_comment,"comment_form":comment_form})


class CreatePost(CreateView):
    model = Post
    template_name = "blog/new_post.html"
    fields = ["title","author","body"]


def share_post(request,object_id):
    post = get_object_or_404(Post,id=object_id)
    sent = False

    if request.method == "POST":
        form = EmailPost(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            get_post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = "{} ({}) recommends you reding {}".format(cd['name'],cd['email'],post.title)
            message = "Read {} at {} \n\n{}\'s comments: {}".format(post.title,get_post_url,cd['name'],cd['comments'])

            send_mail(subject,message,"saikumarveeranki1@gmail.com",[cd['to']])
            sent = True

    else:
        form = EmailPost()

    return render(request,"blog/share.html",{"form":form,"post":post,"sent":sent})
