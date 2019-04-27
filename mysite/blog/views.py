from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    # 通过标签来过滤文章
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="publish", publish_time__year=year, publish_time__month=month,
                             publish_time__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 显示相近tag的文章列表
    post_tags_ids = post.tags.values_list('id', flat=True)
    print("ids:", post.tags.values_list('id', flat=True))
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # count;按照相同标签的数量计数
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish_time')[:4]
    print("相似文章：", similar_posts)

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='publish')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{}({})推荐你阅读{}".format(data['name'], data['email_from'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url,
                                                                    data['name'], data['comments'])
            send_mail(subject, message, 'guofeng_1997@163.com', [data['email_to']])
            sent = True
            print("邮件发送成功")

    form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})


class PostListView(ListView):
    # django内置的ListView返回的变量名称叫做page_obj;
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
