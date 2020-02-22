from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """
    Serializes a name field for testing our APIView:
    whenver sending a post request the serializer would validate the input with
    a maximum length of 10.
    """
    name = serializers.CharField(max_length=10)
