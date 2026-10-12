from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView
from django.db.models import FilteredRelation, Q, F
from .models import Problem, ProblemStatus

level_conversion = {
    'new': 0,   
    'beginner': 1,
    'intermediate': 2
}

EASY_XP = 20
MEDIUM_XP = 35
HARD_XP = 50

@method_decorator(never_cache, name='dispatch')
class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = 'problems/problem_detail.html'
    context_object_name = 'problem'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        status = request.POST.get('status', 'NOT_COMPLETED').strip()
        update_xp = status == 'COMPLETED'
        difficulty = self.object.category_difficulty
        starred = request.POST.get('star', 'NO').strip() == 'YES'
        
        problem_status, created = ProblemStatus.objects.update_or_create(
            user=request.user,
            problem=self.object,
            defaults={'status': status, 'starred': starred}
        )

        problem_status.refresh_from_db()

        if update_xp and (not problem_status.earned_xp or created):
            problem_status.earned_xp = True
            problem_status.save(update_fields=['earned_xp'])

            xp_map = {
                'EASY': EASY_XP,
                'MEDIUM': MEDIUM_XP,
                'HARD': HARD_XP
            }

            request.user.profile.add_xp(xp_map[difficulty])

        return redirect(self.object.get_absolute_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        problem = Problem.objects.filter(title=self.object.title).first()
        problem = str(problem).split('-')[-1]

        context['title'] = problem
        context['calendar'] = False
        
        return context

@never_cache
@login_required
def problem_list(request, topic='Sign in to Save Data'):
    level = level_conversion[request.user.user_level.lower()]
    mini_level = request.user.profile.mini_level

    if request.user.is_authenticated:
        problems = Problem.objects.annotate(
            user_data=FilteredRelation(
                'problemstatus',
                condition=Q(problemstatus__user=request.user)
            )
        ).annotate(
            user_status=F('user_data__status'),
            user_starred=F('user_data__starred')
        ).select_related()


        if topic == 'all':
            problems = problems.all()
            topic = 'All Problems'

        else:
            problems = problems.filter(topic=topic)
            topic = problems.first().get_topic_display()

    else:
        problems = Problem.objects.all()
    
    context = {
        'title': topic,
        'problems': problems,
        'topic': topic,
        'user_level': level,
        'unlocked_problems': problems.filter(Q(user_level_access__lt=level) | Q(user_level_access=level, mini_level_access__lte=mini_level)),
        'locked_problems': problems.filter(Q(user_level_access__gt=level) | Q(user_level_access=level, mini_level_access__gt=mini_level)),
        # 'calendar': True
    }

    return render(request, 'problems/problem_list.html', context)