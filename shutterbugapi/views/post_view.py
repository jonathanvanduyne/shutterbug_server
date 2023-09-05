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
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single post"""
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations """
        user = ShutterbugUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.create(
            user=user,
            title=request.data["title"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            published_on=request.data["published_on"],
            category=category,
            approved=request.data["approved"],
            flagged=request.data["flagged"]
        )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
        user = ShutterbugUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.get(pk=pk)
        post.user = user
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.published_on = request.data["published_on"]
        post.category = category
        post.approved = request.data["approved"]
        post.flagged = request.data["flagged"]
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    


class ShutterbugUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = ShutterbugUser
        fields = ('id', 'user', 'bio', 'profile_image_url')

        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('label')

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = PostTag
        fields = ('label')

        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('shutterbug_user', 'content', 'created_on')

        depth = 1

class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions"""
    class Meta:
        model = PostReaction
        fields = ('shutterbug_user', 'reaction_type')

        depth = 1

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""

    shutterbug_user = ShutterbugUserSerializer(many=False)
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)
    reactions = ReactionSerializer(many=True)


    class Meta:
        model = Post
        fields = ('id', 'shutterbug_user', 'title', 'image_url', 'content', 'published_on', 'category', 'tags', 'comments', 'reactions', 'approved', 'flagged')

        depth = 1