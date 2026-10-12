from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from problems.models import ProblemStatus
from .models import AlgoUser

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully created account! You can now log in.')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'title': 'Registration', 'form': form})


def aggregate_problems(user):
    problem_counts = ProblemStatus.objects.filter(user=user).aggregate(
        total_solved=Count('id', Q(status='COMPLETED')),
        easy_solved=Count('id', Q(problem__category_difficulty='EASY', status='COMPLETED')),
        medium_solved=Count('id', Q(problem__category_difficulty='MEDIUM', status='COMPLETED')),
        hard_solved=Count('id', Q(problem__category_difficulty='HARD', status='COMPLETED')),

        in_progress=Count('id', Q(status="IN_PROGRESS")),
        easy_progress=Count('id', Q(problem__category_difficulty='EASY', status='IN_PROGRESS')),
        medium_progress=Count('id', Q(problem__category_difficulty='MEDIUM', status='IN_PROGRESS')),
        hard_progress=Count('id', Q(problem__category_difficulty='HARD', status='IN_PROGRESS')),
    )

    return problem_counts


@login_required
def profile(request, username):
    profile_user = get_object_or_404(AlgoUser, username=username)

    context = {
        'title': profile_user.username,
        'problems_in_progress': ProblemStatus.objects.filter(user=profile_user, status='IN_PROGRESS'),
        'profile_user': profile_user
    } | aggregate_problems(profile_user)

    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('profile', username=request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'accounts/edit_profile.html', context)