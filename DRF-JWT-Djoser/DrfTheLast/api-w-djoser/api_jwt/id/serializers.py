from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import User, UserProfile

class UserCreateWithTokenSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 're_password')
        extra_kwargs = {'password': {'write_only': True}}

# Nestes user
class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='user.username')
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        # fallback Cloudinary default
        return "https://res.cloudinary.com/dcxbs1lon/image/upload/v1762843193/placeholder_profile.jpg"
            
    class Meta:
        model = UserProfile
        fields = ['user', 'owner', 'bio', 'phone', 'image']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'image']

