from rest_framework import serializers

from users.models import CustomUser, Payments


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payments
        fields = "__all__"
