# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, logout
# from customers.models import User
# from django.contrib import messages
# from landing_start.forms import UserRegistrationForm
# from customers.backends import UsernameAuthBackend
# from django.contrib.auth import login as auth_login  # Import the default login function
# from django.contrib.auth.hashers import make_password

# # Custom login function to handle session storage
# def custom_login(request, user):
#     request.session['user_pk'] = user.username  # Store the username in the session
#     auth_login(request, user)  # Use Django's default login to manage other aspects

# def landing_page(request):
#     return render(request, 'landing_start/landing.html')

# def about_us(request):
#     return render(request, 'landing_start/about_us.html')

# def contact(request):
#     return render(request, 'landing_start/contact.html')

# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_customer:
#                 custom_login(request, user)  # Use custom login here
#                 return redirect('customer_dashboard')  # Adjust the URL name as needed
#             elif user.is_operator:
#                 custom_login(request, user)  # Use custom login here
#                 return redirect('operator_dashboard')  # Redirect to operator dashboard
#             elif user.is_manager:
#                 custom_login(request, user)  # Use custom login here
#                 return redirect('manager_dashboard')  # Redirect to operator dashboard
#             else:
#                 return render(request, 'landing_start/login.html', {
#                     'error_message': "Access denied. Only customers or operators can log in here."
#                 })
#         else:
#             return render(request, 'landing_start/login.html', {
#                 'error_message': "Invalid credentials. Please try again."
#             })

#     return render(request, 'landing_start/login.html')


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         email = request.POST['email']
#         first_name = request.POST['first_name']
#         surname = request.POST['surname']

#         if password != confirm_password:
#             return render(request, 'landing_start/register.html', {
#                 'error_message': "Passwords do not match. Please try again."
#             })

#         if User.objects.filter(username=username).exists():
#             return render(request, 'landing_start/register.html', {
#                 'error_message': "Username already exists."
#             })

#         user = User.objects.create(
#             username=username,
#             password=make_password(password),  # Hash the password
#             email=email,
#             first_name=first_name,
#             surname=surname,
#             is_customer=True,
#             is_manager=False,
#             is_operator=False,
#         )
#         user.save()
#         messages.success(request, 'Account created successfully! You can now log in.')
#         return redirect('login')

#     return render(request, 'landing_start/register.html')

# def logout_user(request):
#     logout(request)
#     return redirect('landing_page')
#previous code above

# Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from customers.models import User
from django.contrib import messages
from landing_start.forms import UserRegistrationForm
from customers.backends import UsernameAuthBackend
from django.contrib.auth import login as auth_login  # Import the default login function
from django.contrib.auth.hashers import make_password

# Custom login function to handle session storage
def custom_login(request, user):
    request.session['user_pk'] = user.username  # Store the username in the session
    auth_login(request, user)  # Use Django's default login to manage other aspects

# Landing page view
def landing_page(request):
    return render(request, 'landing_start/landing.html')

# About us page view
def about_us(request):
    return render(request, 'landing_start/about_us.html')

# Contact page view
def contact(request):
    return render(request, 'landing_start/contact.html')

# Login page view
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_customer:
                custom_login(request, user)  # Use custom login here
                return redirect('customer_dashboard')  # Redirect to customer dashboard
            elif user.is_operator:
                custom_login(request, user)  # Use custom login here
                return redirect('operator_dashboard')  # Redirect to operator dashboard
            elif user.is_manager:
                custom_login(request, user)  # Use custom login here
                return redirect('manager_dashboard')  # Redirect to manager dashboard
            else:
                return render(request, 'landing_start/login.html', {
                    'error_message': "Access denied. Only customers or operators can log in here."
                })
        else:
            return render(request, 'landing_start/login.html', {
                'error_message': "Invalid credentials. Please try again."
            })

    return render(request, 'landing_start/login.html')

# Registration page view
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        surname = request.POST['surname']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'landing_start/register.html', {
                'error_message': "Passwords do not match. Please try again."
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'landing_start/register.html', {
                'error_message': "Username already exists."
            })

        # Create a new user
        user = User.objects.create(
            username=username,
            password=make_password(password),  # Hash the password
            email=email,
            first_name=first_name,
            surname=surname,
            is_customer=True,
            is_manager=False,
            is_operator=False,
        )
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'landing_start/register.html')

# Logout user view
def logout_user(request):
    logout(request)
    return redirect('landing_page')
