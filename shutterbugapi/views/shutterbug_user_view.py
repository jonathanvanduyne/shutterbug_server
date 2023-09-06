from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from shutterbugapi.models import ShutterbugUser

class ShutterbugUserView(ViewSet):

    def list(self, request):
        """Handle GET requests to shutterbug users resource"""
        try:
            users = ShutterbugUser.objects.all()
            serializer = ShutterbugUserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk):
        """Handle GET requests for a single shutterbug user"""
        try:
            user = ShutterbugUser.objects.get(pk=pk)
            serializer = ShutterbugUserSerializer(user)
            return Response(serializer.data)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk):
        """Handle PUT requests for a shutterbug user"""
        try:
            user = ShutterbugUser.objects.get(pk=pk)
            user.bio = request.data.get("bio", user.bio)  # Use get to keep the existing value if not provided
            user.profile_image_url = request.data.get("profile_image_url", user.profile_image_url)  # Use get to keep the existing value if not provided
            user.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active', 'date_joined')

class ShutterbugUserSerializer(serializers.ModelSerializer):
    """JSON serializer for shutterbug users"""
    user = UserSerializer(many=False)

    class Meta:
        model = ShutterbugUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'full_name')
        depth = 1
