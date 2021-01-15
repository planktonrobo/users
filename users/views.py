from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Archive, Article
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import DeleteView


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html') 

@login_required
def new_archive(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            o = form.save(commit=False)
            o.publisher = request.user
            o.save()
            archive_name = form.cleaned_data.get('archive_name')
            messages.success(request, f'{archive_name}! Created')
            return redirect('profile')
    else:
        form = ProfileUpdateForm()
    return render(request, 'newarchive.html', {'form': form})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Archive
    success_url = '/profile'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.publisher:
            return True
        return False




@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated!')
            return redirect('settings')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'settings.html', {'form': form})