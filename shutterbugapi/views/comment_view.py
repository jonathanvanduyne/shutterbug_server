from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shutterbugapi.models import Post, ShutterbugUser, Comment

class CommentView(ViewSet):
    """Handle requests to comments resource"""

    def list(self, request):
        """Handle GET requests to comments resource"""
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations """
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)

            # Get the post using the provided post ID
            post = Post.objects.get(pk=request.data["post"])

            # Create a new Comment instance with the provided data
            comment = Comment.objects.create(
                shutterbug_user=user,
                post=post,
                content=request.data["content"],
            )

            # Serialize the newly created comment and return it with a 201 status
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a comment"""
        try:
            comment = Comment.objects.get(pk=pk)

            # Use get to keep the existing value if not provided
            comment.content = request.data.get("content", comment.content)
            comment.approved = request.data.get("approved", comment.approved)
            comment.flagged = request.data.get("flagged", comment.flagged)
            comment.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentAuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for comment author"""
    class Meta:
        model = ShutterbugUser
        fields = ('id', 'full_name')


class CommentPostSerializer(serializers.ModelSerializer):
    """JSON serializer for comment post"""
    class Meta:
        model = Post
        fields = ('id', 'title')


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""

    shutterbug_user = CommentAuthorSerializer(many=False)
    post = CommentPostSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'shutterbug_user', 'post', 'content',
                  'published_on', 'approved', 'flagged')
        depth = 1
