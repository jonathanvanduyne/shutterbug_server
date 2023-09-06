from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shutterbugapi.models import Tag, PostTag, Post, ShutterbugUser, PostReaction

class TagView(ViewSet):
    """Handles requests for Tags"""

    def list(self, request):
        """Handle GET requests to tags resource"""
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for a single tag"""
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)

        except Tag.DoesNotExist:
            return Response({'message': 'Tag not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def create(self, request):
        """Handle POST operations"""
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)

            # Validate the label field
            label = request.data.get("label")
            if not label:
                return Response({'message': 'Label is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new Tag instance with the provided data
            tag = Tag.objects.create(label=label)

            # Serialize the newly created tag and return it with a 201 status
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk):
        """Handle PUT requests for a tag"""
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)

            # Get the tag using the provided tag ID
            tag = Tag.objects.get(pk=pk)

            # Update the tag's label
            tag.label = request.data["label"]
            tag.save()

            # Return a 204 response, which indicates the update operation was successful
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Tag.DoesNotExist:
            return Response({'message': 'Tag not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk):
        """Handle DELETE requests for a single tag"""
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
        depth = 1