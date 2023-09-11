from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User


class DjangoUserView(ViewSet):

    def list(self, request):
        """Handle GET requests to Django users resource"""
        users = User.objects.all()

        serializer = DjangoUserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single Django user"""
        user = User.objects.get(pk=pk)
        serializer = DjangoUserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        try:
            user = User.objects.get(pk=pk)

            # Fields to exclude from updating
            excluded_fields = ["password", "last_login", "is_superuser"]

            # Update other fields
            for field in request.data:
                if field not in excluded_fields:
                    setattr(user, field, request.data[field])

            user.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DjangoUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Django users"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active', 'date_joined')