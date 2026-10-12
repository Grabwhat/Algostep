from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import AlgoUser

level_conversion = {
    'new': 0,   
    'beginner': 1,
    'intermediate': 2
}

class CPTopic(models.Model):

    class TopicLevels(models.IntegerChoices):
        LVL1 = 1, _('Foundational')
        LVL2 = 2, _('Beginner')
        LVL3 = 3, _('Elementary')
        LVL4 = 4, _('Intermediate')

    name = models.CharField(max_length=100)
    slug_name = models.CharField(max_length=100, default='topic')
    description = models.TextField()

    topic_level = models.IntegerField(
        choices=TopicLevels.choices,
        default=TopicLevels.LVL1
    )

    requirements = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='unlocks'
    )

    mini_level_req = models.PositiveIntegerField(default=1)
    user_level_req = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'CP Topic'
        verbose_name_plural = 'CP Topics'

    def __str__(self):
        return f"{self.name} - {self.get_topic_level_display()}"


class UserTopic(models.Model):

    class Status(models.TextChoices):
        LOCKED = 'LOCKED', 'Locked'
        UNLOCKED = 'UNLOCKED', 'Unlocked'

    user = models.ForeignKey(AlgoUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(CPTopic, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.LOCKED
    )

    class Meta:
        unique_together = ('user', 'topic')

        verbose_name = 'User Topic'
        verbose_name_plural = 'User Topics'

    def __str__(self):
        return f"{self.user} - {self.topic} ({self.get_status_display()})"