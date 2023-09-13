from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shutterbugapi.models import Post, Category, ShutterbugUser, PostTag, Tag, Comment, PostReaction, Reaction


class PostView(ViewSet):

    def list(self, request):
        """Handle GET requests to posts resource"""
        posts = Post.objects.all()

        category = self.request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category__id=category)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            posts = posts.filter(tags__id=tag)

        user = self.request.query_params.get('user', None)
        if user is not None:
            posts = posts.filter(shutterbug_user__id=user)

        flagged = self.request.query_params.get('flagged', None)
        if flagged is not None:
            posts = posts.filter(flagged=True)

        unaaproved = self.request.query_params.get('unapproved', None)
        if unaaproved is not None:
            posts = posts.filter(approved=False)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


    def retrieve(self, request, pk):
        """Handle GET requests for single post"""
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations """
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)
            # Get the category using the provided category ID
            category = Category.objects.get(pk=request.data["category"])
            # Get the tags using the provided tag IDs
            tags = Tag.objects.filter(pk__in=request.data["tags"])
            # Get the published_on date

            # Create a new Post instance with the provided data
            post = Post.objects.create(
                shutterbug_user=user,
                title=request.data["title"],
                image_url=request.data["image_url"],
                content=request.data["content"],
                category=category
            )

            post.tags.set(tags)

            # Serialize the newly created post and return it with a 201 status
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single post"""
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Handle PUT requests for a post"""
        try:
            user = ShutterbugUser.objects.get(pk=request.data["shutterbug_user"])
            category = Category.objects.get(pk=request.data["category"])

            post = Post.objects.get(pk=pk)
            post.shutterbug_user = user
            post.title = request.data["title"]
            post.image_url = request.data["image_url"]
            post.content = request.data["content"]
            post.published_on = request.data["published_on"]
            post.category = category
            post.approved = request.data["approved"]
            post.flagged = request.data["flagged"]
            post.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        fields = ('id', 'label')


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""

    class Meta:
        model = Tag
        fields = ('id', 'label')


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions"""

    class Meta:
        model = Reaction
        fields = ('label', 'image_url')


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""

    # Define fields for User model properties
    user_first_name = serializers.CharField(
        source='shutterbug_user.user.first_name', read_only=True)
    user_last_name = serializers.CharField(
        source='shutterbug_user.user.last_name', read_only=True)
    user_full_name = serializers.CharField(
        source='shutterbug_user.full_name', read_only=True)
    user_email = serializers.EmailField(
        source='shutterbug_user.user.email', read_only=True)
    user_is_active = serializers.BooleanField(
        source='shutterbug_user.user.is_active', read_only=True)

    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    reactions = ReactionSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'shutterbug_user', 'user_first_name', 'user_last_name', 'user_full_name', 'user_email', 'user_is_active',
                  'title', 'image_url', 'content', 'published_on', 'category', 'tags', 'reactions', 'approved', 'flagged')
        depth = 1
