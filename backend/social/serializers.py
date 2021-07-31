from django.contrib.auth import get_user_model
from rest_framework import serializers

USER = get_user_model()


class SubscriberSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, USER):
        return True

    class Meta:
        model = USER
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
