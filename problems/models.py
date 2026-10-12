from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from learning.models import CPTopic

User = get_user_model()

class Problem(models.Model):

    class Topic(models.TextChoices):
        ARRAYS_HASHING  = 'arrays-hashing'  ,  'Arrays & Hashing'
        TWO_POINTERS    = 'two-pointers'    ,  'Two Pointers'
        STACK           = 'stack'           ,  'Stack'
        BINARY_SEARCH   = 'binary-search'   ,  'Binary Search'
        SLIDING_WINDOW  = 'sliding-window'  ,  'Sliding Window'
        COMPLETE_SEARCH = 'complete-search' ,  'Complete Search'
        SIMULATION      = 'simulation'      ,  'Simulation'
        GRAPHS          = 'graphs'          ,  'Graphs'
        GREEDY          = 'greedy'          ,  'Greedy'
        MATH            = 'math'            ,  'Math'
        RECURSION       = 'recursion'       ,  'Recursion'

    class Difficulties(models.TextChoices):
        EASY =   'EASY'   , 'Easy'
        MEDIUM = 'MEDIUM' , 'Medium',
        HARD =   'HARD'   , 'Hard'

    class UserLevelAccess(models.IntegerChoices):
        NEW          = 0, _('New')
        BEGINNER     = 1, _('Beginner')
        INTERMEDIATE = 2, _('Intermediate')

    class DifficultyColor(models.TextChoices):
        EASY =      'text-green-500'  , 'Easy'
        MEDIUM =    'text-yellow-500' , 'Medium'
        HARD =      'text-red-600'    , 'Hard'
        OTHER =     'text-purple-700' , 'Other'
    
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=150)
    url = models.URLField()
    slug = models.SlugField(max_length=200, unique=True)

    external_id = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)

    category_difficulty = models.CharField(
        max_length=50,
        choices=Difficulties.choices,
        default=Difficulties.EASY
    )

    description = models.TextField(default='')
    topic = models.CharField(
        max_length=150,
        choices=Topic.choices,
        default=Topic.ARRAYS_HASHING
    )

    topic_relation = models.ForeignKey(
        CPTopic, 
        on_delete=models.PROTECT, 
        related_name='problems'
    )

    user_level_access = models.IntegerField(
        choices=UserLevelAccess.choices,
        default=UserLevelAccess.NEW
    )

    mini_level_access = models.PositiveIntegerField(default=1)

    user_tracking = models.ManyToManyField(
        User,
        through='ProblemStatus',
        related_name='problem_track'
    )

    difficulty_color = models.CharField(
        max_length=150,
        choices=DifficultyColor.choices,
        default=DifficultyColor.OTHER
    )

    class Meta:
        unique_together = ('platform', 'external_id')

    def get_absolute_url(self):
        return reverse('problem-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.platform} - Rated {self.difficulty} - {self.title}"


class ProblemStatus(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Completed'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        NOT_STARTED = 'NOT_STARTED', 'Not Started'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.NOT_STARTED
    )

    starred = models.BooleanField(default=False)
    earned_xp = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'problem')
        
        verbose_name = 'Problem Status'
        verbose_name_plural = 'Problem Statuses'

    def __str__(self):
        starred = '(Starred)' if self.starred else ''

        return f"{self.user.username} - {str(self.problem).split('-')[-1]} - {self.get_status_display()} {starred}"

class Hint(models.Model):
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.CASCADE,
        related_name="hints"
    )

    order = models.IntegerField(default=1)
    text = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Hint {self.order} - {self.problem}"

class Editorial(models.Model):
    problem = models.OneToOneField(
        Problem,
        on_delete=models.CASCADE,
        related_name='editorial'
    )

    explanation = models.TextField(blank=True)
    py_solution = models.TextField()
    cpp_solution = models.TextField()

    def __str__(self):
        return f"Editorial for {self.problem}"