from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import DeleteView
from article.models import Article


def register(request,*args, **kwargs):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accound created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form':u_form, 'p_form':p_form}
    return render(request, 'user/update_profile.html', context )



class UserDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = '/'

    def test_func(self):      # test for UserPassesTestMixin
        user = self.get_object()
        return self.request.user.id == user.id

@login_required
def profile(request):
    user = request.user
    user_articles_queryset = Article.objects.filter(author__id=user.id).order_by('-created_at')
    paginator = Paginator(user_articles_queryset, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"user_arts": user_articles_queryset,
               'is_paginated': True, 'page_obj': page_obj}
    return render(request, 'user/profile.html', context)

def profile(request, username):
    # NUM_TOP_ARTS = 10
    user = get_object_or_404(User, username = username)
    user_articles_queryset = Article.objects.filter( author__id = user.id, drafted=False).order_by('-created_at')

    paginator = Paginator(user_articles_queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.username == username:
        owner = True
    else:
        owner = False
    context = {'s_user': user, 'is_owner': owner, "articles":user_articles_queryset,
               'is_paginated':True, 'page_obj':page_obj}
    return render(request, 'user/profile.html',context)
