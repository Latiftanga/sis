from typing import Any
from django.shortcuts import render, redirect
from core.forms import TokenVerificationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.forms import (
    UserRegistrationForm, SigninForm,AddressForm
)

from core.models import SignupToken, Teacher
from portal.forms.teacher_forms import TeacherForm



def verify_token(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        form = TokenVerificationForm(request.POST)
        if form.is_valid():
            token=form.cleaned_data['token']
            request.session['token'] = token
            return redirect('core:signup')
    else:
        form = TokenVerificationForm()
    context = {'form': form, 'page_title': 'Verify token'}
    return render(request, 'auth/verify_token.html', context=context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    token = request.session.get('token', None)
    if not token:
        return redirect('core:veriy-token')
    try:
        signup_token = SignupToken.objects.get(token=token, is_used=False)
    except SignupToken.DoesNotExist:
        messages.error(request, "Invalid or already used token.")
        return redirect('core:verify-token')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, initial_email=signup_token.email)
        if form.is_valid():
            user = form.save()
            if signup_token.token_type == 'teacher':
                user.is_teacher = True
            if signup_token.token_type == 'student':
                user.is_student = True
            if signup_token.token_type == 'guardian':
                user.is_guardian = True
            user.token = signup_token
            user.save()
            signup_token.is_used = True
            signup_token.save()

            login(request, user)

            # Redirect to the start of the profile wizard
            return redirect('core:add-profile')
    else:
        form = UserRegistrationForm(initial={'email': signup_token.email})
    context = {'form': form, 'page_title': 'Create Account'}
    return render(request, 'auth/signup.html', context)


@login_required
def add_profile(request):
    if not request.user.token:
        return redirect('core:veriy-token')

    if request.user.is_teacher:
        if request.method == 'POST':
            form = TeacherForm(request.POST)
            if form.is_valid():
                teacher = form.save(commit=False)
                teacher.user = request.user
                teacher.save()
                print('teacher save')
                return redirect('core:add-contact')
        else:
            form = TeacherForm()
            return render(request, 'teachers/teacher_form.html', {'form': form})
    else:
        return redirect('core:verify-token')  # Replace with your error URL

    return redirect('core:verify-token')


@login_required
def add_contact(request):
    """Create contact for teacher or student"""
    user = request.user
    profile = None
    if not user.token:
        return redirect('core:veriy-token')

    if user.is_teacher:
        profile = user.teacher_profile
    if user.is_student:
        profile = user.student_profile
    if user.is_guardian:
        profile = user.guardian_profile

    if profile is None:
        redirect('core:add-profile')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            profile.address = address
            profile.save()
            return redirect('core:teacher-dashboard')
        return render(request, 'address_form.html', {'form': form})
    else:
        form = AddressForm()
        return render(request, 'address_form.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    form = SigninForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect("/")
            else:
                messages.error(request, 'Invalid Email or Password')
                msg = 'Invalid Email or password!'
        else:
            messages.error(request, 'An error occurred!.')
    
    context = {"form": form, "msg": msg, 'page_title': 'Signin'}
    return render(request, 'auth/signin.html', context=context)


class Index(LoginRequiredMixin, TemplateView):
    template_name = None  # Set dynamically based on user role

    def get(self, request, *args, **kwargs):
        # Check the user's role and assign the appropriate template
        if request.user.is_admin or request.user.is_superuser:
            self.template_name = 'dashboards/admin_dashboard.html'
        elif request.user.is_teacher:
            self.template_name = 'dashboards/teacher_dashboard.html'
        elif request.user.is_student:
            self.template_name = 'dashboards/student_dashboard.html'
        else:
            # Return a 403 Forbidden response with a custom template if no valid role
            return render(request, 'errors/403.html', status=403)

        # Render the appropriate template
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check user role and customize context accordingly
        if self.request.user.is_authenticated:
            if self.request.user.is_admin or self.request.user.is_superuser:
                # Admin-specific data
                context['teacher_count'] = Teacher.objects.count()
                # Add more admin-specific context if needed
            elif self.request.user.is_teacher:
                # Teacher-specific data
                context['teacher_info'] = "This is a teacher's view."
                # Add more teacher-specific context if needed
            elif self.request.user.is_student:
                # Student-specific data
                context['student_info'] = "This is a student's view."
                # Add more student-specific context if needed
        else:
            # Not authenticated
            context['error_message'] = "You need to log in to view this page."
        
        return context
        