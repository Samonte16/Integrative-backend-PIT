from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import User
import json

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

        hashed_password = make_password(password)

        user = User.objects.create(
            full_name=full_name,
            gender=gender,
            age=age,
            phone=phone,
            email=email,
            password=hashed_password
        )

        # Prepare verification link
        verification_link = f"http://192.168.1.44:8000/api/verify-email/{user.verification_token}/"

        # Render HTML template
        html_content = render_to_string('emails/verify_email.html', {
            'full_name': full_name,
            'verification_link': verification_link
        })

        # Send email
        email_subject = 'Verify Your Email Address'
        email_from = settings.EMAIL_HOST_USER
        email_msg = EmailMultiAlternatives(email_subject, '', email_from, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return JsonResponse({'message': 'User created successfully. Please check your email to verify your account.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        if user.is_active:
            return JsonResponse({'message': 'Account already verified.'}, status=200)
        user.is_active = True
        user.save()
        return JsonResponse({'message': 'Email verified successfully! You can now log in.'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid or expired token.'}, status=400)


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

        if not user.is_active:
            return JsonResponse({'error': 'Account not verified. Please check your email.'}, status=403)

        if check_password(password, user.password):
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
