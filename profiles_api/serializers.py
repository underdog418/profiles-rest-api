from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """
    Serializes a name field for testing our APIView:
    whenver sending a post request the serializer would validate the input with
    a maximum length of 10.
    """
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
        'password': {
            'write_only': True,
            'style': {'input_type': 'password'}
            }
        }

    def create(self, vadata):
        """create and return a new user"""
        user = models.UserProfile.objects.create_user(
        email = vadata['email'],
        name = vadata['name'],
        password = vadata['password']
        )
        return user
