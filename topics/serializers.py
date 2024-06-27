from rest_framework import serializers
from .models import Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'topic_title', 'topic_body', 'topic_hashtag', 'topic_category', 'topic_pub_date']
