from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer1(ModelSerializer):
    class Meta:
        model = User
        exclude = ("created_on", "updated_on", "password")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    model = User

    def validate(self, value):
        if self.initial_data["old_password"] and self.initial_data["new_password"]:
            return value
        raise ValidationError(
            {
                "old_password": "This field may not be null.",
                "new_password": "This field may not be null.",
            }
        )

    def validate_old_password(self, old_password):
        print("in validate password")
        try:
            user = self.context["request"].thisUser
        except:
            raise serializers.ValidationError("User Not Found")
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        return old_password

    def save(self):
        if self.validated_data["old_password"] and self.validated_data["new_password"]:
            user = self.context["request"].thisUser
            print("user")
            user.set_password(self.validated_data["new_password"])
            user.save()
        return user


class ProfileSerializer(serializers.Serializer):
    class Meta:
        fields = "__all__"
