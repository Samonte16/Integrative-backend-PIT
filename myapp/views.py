from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import Profile

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        full_name = data.get('full_name')
        gender = data.get('gender')
        age = data.get('age')
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=email).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name  # optionally split full name if needed
        user.save()

        # Create profile if you use extra fields
        Profile.objects.create(user=user, gender=gender, age=age, phone=phone)

        return JsonResponse({'message': 'User created successfully'})

    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)  # optional if using sessions
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid method'}, status=405)
