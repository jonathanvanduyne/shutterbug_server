from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from shutterbugapi.models import ShutterbugUser

""" I DO NOT KNOW IF YOU NEED THESE IMPORTS! ALSO HONEYRARE WITH ADMIN AUTH IS PASTED BELOW THE GAMER """
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data.get('username', None)
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)
    bio = request.data.get('bio',None)
    profile_image_url = request.data.get('profile_image_url',None)

    

    if username is not None \
        and email is not None\
        and first_name is not None \
        and last_name is not None \
        and password is not None:
        if email is None:
            return Response(
                {'message': 'You must provide an email'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if first_name is None:
            return Response(
                {'message': 'You have a first name. Where is it?'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if last_name is None:
                return Response(
                    {'message': 'No last name, moron.'},
                    status=status.HTTP_400_BAD_REQUEST
                )            
        if password is None:
            return Response(
                {'message': 'You must provide a password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if bio is None: 
            return Response(
                {'message': 'You must include a bio about yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if profile_image_url is None: 
            return Response(
                {'message': 'You must include a profile image.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email = request.data['email']
            )
            

        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_user is not None:
            new_shutterbug_user = ShutterbugUser.objects.create(
                user=new_user,
                bio=request.data['bio'],
                profile_image_url=request.data['profile_image_url']
            )
            new_shutterbug_user.save()
            


        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        # Return the token to the client
        data = { 'token': token.key, 'staff': new_user.is_staff }
        return Response(data)

    return Response({'message': 'You must provide email, password, first_name, last_name and account_type'}, status=status.HTTP_400_BAD_REQUEST)
