from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

level_2_num = {
    'NEW': 0,
    'BEGINNER': 1,
    'INTERMEDIATE': 2
}

num_2_level = {
    0: 'NEW',
    1: 'BEGINNER',
    2: 'INTERMEDIATE'
}

class AlgoUser(AbstractUser):

    class UserLevel(models.TextChoices):
        new = 'NEW', 'New'
        beginner = 'BEGINNER', 'Beginner'
        intermediate = 'INTERMEDIATE', 'Intermediate'

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    github_username = models.CharField(max_length=39, blank=True, default='Not Added Yet')
    codeforces_username = models.CharField(max_length=100, blank=True, default='Not Added Yet')
    leetcode_username = models.CharField(max_length=100, blank=True, default='Not Added Yet')

    user_level = models.CharField(
        max_length=20,
        choices=UserLevel.choices,
        default=UserLevel.new
    )

    unlocked_topics = models.ManyToManyField(
        'learning.CPTopic',
        through='learning.UserTopic',
        related_name='user_progress'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        new_user = self.pk is None
        super().save(*args, **kwargs)

        if new_user:
            from learning.models import CPTopic, UserTopic

            unlocked = CPTopic.objects.filter(user_level_req__lte=level_2_num[self.user_level], mini_level_req__lte=self.profile.mini_level)

            for topic in unlocked:
                UserTopic.objects.get_or_create(
                    user=self,
                    topic=topic,
                    defaults={'status': 'UNLOCKED'}
                )

    def __str__(self):
        return f"{self.username} - {self.get_user_level_display()}"

class Profile(models.Model):
    user = models.OneToOneField(AlgoUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics/')

    xp = models.PositiveIntegerField(default=0)
    mini_level = models.PositiveIntegerField(default=1)

    MAX_LEVELS = 3

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def add_xp(self, points):
        if points > 0:
            Profile.objects.filter(pk=self.pk).update(xp=F('xp') + points)
            self.refresh_from_db()
            self.check_level_up()

    def check_level_up(self):
        core_user = self.user

        while self.xp >= self.xp_required:
            from learning.models import CPTopic, UserTopic

            self.xp -= self.xp_required
            self.mini_level += 1

            if self.mini_level > self.MAX_LEVELS:
                self.mini_level = 1

                curr_level = core_user.user_level
                next_lvl = (level_2_num[curr_level] + 1) % 3
                core_user.user_level = num_2_level[next_lvl]
                
                core_user.save(update_fields=['user_level'])
                core_user.refresh_from_db()

            topics_unlocked = CPTopic.objects.filter(
                mini_level_req=self.mini_level, 
                user_level_req=level_2_num[core_user.user_level]
            )

            for topic in topics_unlocked:
                UserTopic.objects.get_or_create(
                    user=core_user,
                    topic=topic,
                    defaults={'status': 'UNLOCKED'}
                )

        self.save(update_fields=['xp', 'mini_level'])

    @property
    def xp_required(self) -> int:
        core_user = self.user
        curr_level = core_user.user_level

        if curr_level == 'NEW':             return 100
        elif curr_level == 'BEGINNER':      return 120
        elif curr_level == 'INTERMEDIATE':  return 150
        else:                               return -1

    @property
    def total_xp(self) -> int:
        return self.xp + (self.mini_level - 1) * 100

    @property
    def user_xp_required(self) -> int:
        return self.xp_required * 3