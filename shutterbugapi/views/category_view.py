from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from shutterbugapi.models import ShutterbugUser, Post, Category

class CategoryView(ViewSet):
    """Handles requests for Categories"""

    def list(self, request):
        """Handle GET requests to categories resource"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single category"""
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

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

            # Create a new Category instance with the provided data
            category = Category.objects.create(label=label)

            # Serialize the newly created category and return it with a 201 status
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a category"""
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)

            # Get the category using the provided category ID
            category = Category.objects.get(pk=pk)

            # Validate the label field
            label = request.data.get("label")
            if not label:
                return Response({'message': 'Label is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the category with the provided data
            category.label = label
            category.save()

            # Return an empty response body and a 204 status
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for a category"""
        try:
            # Get the user from the request's authentication
            user = ShutterbugUser.objects.get(user=request.auth.user)

            # Get the category using the provided category ID
            category = Category.objects.get(pk=pk)
            category.delete()

            # Return an empty response body and a 204 status
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ShutterbugUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        fields = ('id', 'label')
