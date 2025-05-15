from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password  # For hashing and checking passwords
from .models import User
import json

# Create User
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

        if not (full_name and gender and age and phone and email and password):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Hash the password before saving it
        hashed_password = make_password(password)

        user = User.objects.create(
            full_name=full_name,
            gender=gender,
            age=age,
            phone=phone,
            email=email,
            password=hashed_password  # Store the hashed password
        )

        return JsonResponse({'message': 'User created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


# Login User
@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            return JsonResponse({'error': 'Missing email or password'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        # Check the password
        if check_password(password, user.password):
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
