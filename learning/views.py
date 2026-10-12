from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CPTopic

level_2_num= {
    'new': 0,   
    'beginner': 1,
    'intermediate': 2
}

num_2_level = {
    0: 'New',
    1: 'Beginner',
    2: 'Intermediate'
}

@login_required
def skill_tree(request):
    level = level_2_num[request.user.user_level.lower()]
    mini_level = request.user.profile.mini_level

    topics = CPTopic.objects.filter(topic_level__in=[1, 2, 3, 4]).order_by('mini_level_req')

    unlocked_topic_id = set(
        request.user.unlocked_topics.filter(
            usertopic__status='UNLOCKED'

        ).values_list('id', flat=True)
    )

    for topic in topics:
        user_level_met = topic.user_level_req <= level
        mini_level_met = topic.mini_level_req <= mini_level
        unlocked_all_topics = all(req.id in unlocked_topic_id for req in topic.requirements.all())

        if level > topic.user_level_req:
            topic.locked = not unlocked_all_topics

        elif level == topic.user_level_req:
            topic.locked = (not mini_level_met) or (not unlocked_all_topics)

        else:
            topic.locked = True

        topic.mini_level_met = mini_level_met
        topic.user_level_met = user_level_met

        topic.user_level_requirement = num_2_level[topic.user_level_req]

    context = {
        'level': level,
        'mini_level': mini_level,
        'level1': [t for t in topics if t.topic_level == 1],
        'level2': [t for t in topics if t.topic_level == 2],
        'level3': [t for t in topics if t.topic_level == 3],
        'level4': [t for t in topics if t.topic_level == 4],
        'unlocked_topics': unlocked_topic_id
    }

    return render(request, 'learning/skill_tree.html', context)