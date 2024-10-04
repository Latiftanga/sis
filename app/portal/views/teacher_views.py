from django.db.models.base import Model as Model
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from core.models import (
    Teacher, Address
)
from portal.forms import teacher_forms
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView
)
from core.permissions import (
    AdminRequiredMixin, TeacherOrAdminRequiredMixin
)
from core.utils import (
    generate_random_password, send_activation_email
)
from django.views.generic import FormView


class TeacherListView(ListView, AdminRequiredMixin):
    """List Teachers in the system"""
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'teachers/list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.model().__class__.__name__}s'
        context['page_action'] = 'list'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class TeacherArchiveView(ListView, AdminRequiredMixin):
    """View Archive teacher in the system"""
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'teachers/archived.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Archive {self.model().__class__.__name__}'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class TeacherCreateView(CreateView, AdminRequiredMixin):
    """Create Teachers in the system"""
    model = Teacher
    form_class = teacher_forms.TeacherForm
    template_name = 'teachers/form.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Teacher'
        context['page_action'] = 'create'
        return context

    def form_valid(self, form):
        # Save the teacher personal info instance into the session
        teacher = form.save()
        return redirect('portal:teacher-contact-create', teacher.id)


class TeacherCreateAddressView(CreateView):
    model = Address
    template_name = 'teachers/address_form.html'
    form_class = teacher_forms.TeacherContactInfoForm

    def form_valid(self, form):
        # Store contact info instance in the session
        contact = form.save()
        print("Contact ID: ", contact.id)
        teacher = Teacher.objects.filter(id=self.kwargs['pk']).first()
        if not teacher:
            return redirect('portal:teacher-create')
        teacher.address = contact
        teacher.save()
        if form.cleaned_data['create_account']:
            password = generate_random_password()
            user = get_user_model().objects.create_teacheruser(
                email=teacher.address.email,
                password=password
            )
            teacher.user = user
            teacher.save()
            # send_activation_email(email=user.email, password=password)
        return reverse_lazy('portal:teacher-detail', self.kwargs['pk'])


class TeacherDetailView(DetailView, TeacherOrAdminRequiredMixin):
    """Teacher Detail view"""
    model = Teacher
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.model().__class__.__name__}'
        return context


class TeacherUpdateView(UpdateView, TeacherOrAdminRequiredMixin):
    """Edit Teacher Details"""

    model = Teacher
    form_class = teacher_forms.TeacherForm
    template_name = 'teachers/form.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'{self.object.__class__.__name__}'
        return context

    def get_success_url(self):
        # Access the pk using self.object.pk
        return reverse_lazy('staff:teacher-detail', args=(self.object.pk,))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Teacher updated successfully!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred while updating teacher.')
        return super().form_invalid(form)
