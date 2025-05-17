from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import User, Admin
import json

# 📧 Reusable email sending function
def send_verification_email(recipient_email, full_name, verification_link, is_admin=False):
    subject = 'Verify Your Admin Account' if is_admin else 'Verify Your Email Address'
    template = 'emails/admin_verify_email.html' if is_admin else 'emails/verify_email.html'

    html_content = render_to_string(template, {
        'full_name': full_name,
        'verification_link': verification_link
    })

    email_from = settings.EMAIL_HOST_USER
    email_msg = EmailMultiAlternatives(subject, '', email_from, [recipient_email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

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

        verification_link = f"http://192.168.1.59:8000/api/verify-email/{user.verification_token}/"
        send_verification_email(email, full_name, verification_link)

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

@csrf_exempt
def admin_register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        full_name = data.get('full_name')
        gender = data.get('gender')
        age = data.get('age')
        email = data.get('email')
        password = data.get('password')

        if not (full_name and gender and age and email and password):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if Admin.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        hashed_password = make_password(password)

        admin = Admin.objects.create(
            full_name=full_name,
            gender=gender,
            age=age,
            email=email,
            password=hashed_password
        )

        verification_link = f"http://192.168.1.59:8000/api/admin-verify-email/{admin.verification_token}/"
        send_verification_email(email, full_name, verification_link, is_admin=True)

        return JsonResponse({'message': 'Admin registered successfully. Please check your email to verify your account.'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def admin_verify_email(request, token):
    try:
        admin = Admin.objects.get(verification_token=token)
        if admin.is_active:
            return JsonResponse({'message': 'Admin account already verified.'}, status=200)
        admin.is_active = True
        admin.save()
        return JsonResponse({'message': 'Admin email verified successfully! You can now log in.'}, status=200)
    except Admin.DoesNotExist:
        return JsonResponse({'error': 'Invalid or expired token.'}, status=400)

@csrf_exempt
def admin_login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not (email and password):
            return JsonResponse({'error': 'Missing email or password'}, status=400)

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Admin does not exist'}, status=400)

        if check_password(password, admin.password):
            return JsonResponse({'message': 'Admin login successful', 'admin_name': admin.full_name}, status=200)
        else:
            return JsonResponse({'error': 'Invalid password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def verified_users_view(request):
    verified_users = User.objects.filter(is_active=True).values('full_name', 'email', 'age', 'gender', 'phone')
    return JsonResponse({'verified_users': list(verified_users)}, safe=False)

@csrf_exempt
def forgot_password_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not (email and old_password and new_password):
            return JsonResponse({'error': 'Missing fields'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if not check_password(old_password, user.password):
            return JsonResponse({'error': 'Old password is incorrect'}, status=400)

        user.password = make_password(new_password)
        user.save()

        email_subject = 'Your Password Has Been Changed'
        email_from = settings.EMAIL_HOST_USER
        html_content = render_to_string('emails/password_changed.html', {
            'full_name': user.full_name,
        })
        email_msg = EmailMultiAlternatives(email_subject, '', email_from, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return JsonResponse({'message': 'Password changed successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
