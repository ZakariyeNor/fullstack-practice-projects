from rest_framework import serializers
from .models import CustomUser, Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    image = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        """Return default Cloudinary URL if no image uploaded"""
        ret = super().to_representation(instance)
        if not instance.image:
            ret['image'] = "https://res.cloudinary.com/dcxbs1lon/image/upload/v1755066155/default_profile.jpg"
        else:
            request = self.context.get('request')
            if request:
                ret['image'] = request.build_absolute_uri(instance.image.url)
            else:
                ret['image'] = instance.image.url
        return ret

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'image', 'bio', 'created_at', 'updated_at']

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.user.date_joined.isoformat()

    def get_updated_at(self, obj):
        return obj.user.last_login.isoformat() if obj.user.last_login else None


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # nested profile

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'profile']
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested profile
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance