from article.forms import CommentForm, SortFiltForm
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView, DeleteView, View
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    """
        Shows last RECENT_NUM articles
    """
    RECENT_NUM = 5
    recent_arts_queryset = Article.objects.order_by('-created_at')[:RECENT_NUM]
    return render(request,'article/home.html', {'articles': recent_arts_queryset})

def about_us(request):
    return render(request, 'about_us.html')

class ArtList(View):
    """
    Lists articles with sort and filter ability.
    """
    def get(self, request):
       articles = Article.objects.filter(is_active=True, drafted=False).order_by('created_at')
       template_name = 'article/list.html'
       sort_filt_form = SortFiltForm(initial={"sort_by":"dates", "category_filt": None})
       context = {'articles':articles, 'sort_filt_form': sort_filt_form}
       return render(request, template_name, context)
    
    def post(self, request):
        template_name = 'article/list.html'
        sort_by = request.POST["sort_by"]
        category_filt = request.POST["category_filt"]

        if sort_by == 'dates':
            if category_filt:
                articles = Article.objects.filter(is_active = True, drafted=False, category = category_filt).order_by("-created_at")
            else: 
                articles = Article.objects.filter(is_active = True, drafted=False).order_by("-created_at")

        elif sort_by == 'comments':
            if category_filt:
                articles = Article.objects.filter(is_active = True, drafted=False, category = category_filt).order_by("-comments_count")
            else: 
                articles = Article.objects.filter(is_active = True, drafted=False).order_by("comments__count")


        elif sort_by == 'views':
            if category_filt:
                articles = Article.objects.filter(is_active = True, drafted=False, category = category_filt).order_by("-views")
            else: 
                articles = Article.objects.filter(is_active = True, drafted=False).order_by("-views")
        
        
        sort_filt_form = SortFiltForm(data = request.POST)
        context = {'articles': articles, 'sort_filt_form': sort_filt_form}
        return render(request, template_name, context)


class ArtDetail(View):
    template_name = 'article/about.html'
    def increment_view(self, article):
        article.views = F('views') + 1
        article.save()
        article.refresh_from_db()

    def post(self, request, pk):
        article = get_object_or_404(Article, id = pk)
        comments = article.comments.filter(is_active = True)
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            comment_form = CommentForm()
        else:
            comment_form = CommentForm()
        context = {'article': article, 'comments': comments, "comment_form":comment_form}
        self.increment_view(article)
        return render(request, template_name = self.template_name, context = context)
    
    def get(self, request, pk):
        article = get_object_or_404(Article, id = pk)
        comments = article.comments.filter(is_active = True)
        comment_form = CommentForm()
        context = {'article': article, 'comments': comments, "comment_form":comment_form}
        self.increment_view(article)
        return render(request, template_name = self.template_name, context = context)



class ArtCreate(LoginRequiredMixin,CreateView):
    model = Article
    fields = ['category', 'title', 'content', 'photo', 'drafted']
    template_name = 'article/new_art.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    context_object_name = 'form'


class ArtUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Article
    fields = ['category', 'title', 'content', 'photo', 'drafted']
    template_name = 'article/new_art.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    context_object_name = 'form'    

    def test_func(self):    # test for UserPassesTestMixin
        article = self.get_object()
        return self.request.user == article.author


class ArtDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article/art_confirm_delete.html'
    success_url = '/'

    def test_func(self):    # test for UserPassesTestMixin
        article = self.get_object()
        return self.request.user == article.author
