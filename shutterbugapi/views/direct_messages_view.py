from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shutterbugapi.models import ShutterbugUser, DirectMessage


class DirectMessageView(ViewSet):

    def list(self, request):
        """Handle GET requests to posts resource"""
        direct_messages = DirectMessage.objects.order_by('-created_on')
        serializer = DirectMessageSerializer(
            direct_messages, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single post"""
        direct_message = DirectMessage.objects.get(pk=pk)
        serializer = DirectMessageSerializer(direct_message)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations """
        try:
            # Get the user from the request's authentication
            sender = ShutterbugUser.objects.get(user=request.auth.user)

            recipient = ShutterbugUser.objects.get(pk=request.data["recipient_id"])

            # Create a new Post instance with the provided data
            direct_message = DirectMessage.objects.create(
                sender=sender,
                recipient=recipient,
                content=request.data["content"],
            )

            # Serialize the newly created post and return it with a 201 status
            serializer = DirectMessageSerializer(direct_message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a post
        Returns:
            Response -- Empty body with 204 status code
        """
        direct_message = DirectMessage.objects.get(pk=pk)
        direct_message.content = request.data["content"]
        direct_message.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single post"""
        try:
            direct_message = DirectMessage.objects.get(pk=pk)
            direct_message.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except direct_message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    Arguments:
        serializer type
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')


class ShutterbugUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    Arguments:
        serializer type
    """

    user = UserSerializer(many=False)

    class Meta:
        model = ShutterbugUser
        fields = ('id', 'user', 'profile_image_url')


class DirectMessageSerializer(serializers.ModelSerializer):
    """JSON serializer for direct messages"""

    sender = ShutterbugUserSerializer(many=False)
    recipient = ShutterbugUserSerializer(many=False)

    class Meta:
        model = DirectMessage
        fields = ('id', 'sender', 'recipient', 'content',
                  'created_on', 'is_read', 'is_deleted')
        depth = 1
