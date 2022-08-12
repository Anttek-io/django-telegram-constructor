import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.utils.translation import gettext_lazy as _

from administration.forms import DepartmentCreationForm, DepartmentForm, PositionCreationForm, PositionForm
from administration.models import Department, Position
from logger.utils import log_addition, log_deletion

log = logging.getLogger(__name__)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'administration/index.html'


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        context['departments'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super(DepartmentListView, self).get_queryset().order_by('-id')
        return qs


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentCreationForm

    def __init__(self, **kwargs):
        super(DepartmentCreateView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        form = DepartmentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            log_addition(request, form.instance)
            kwargs.update({'pk': form.instance.pk})
            x = redirect(reverse('administration:department_detail', kwargs=kwargs))
        else:
            log.warning(form.errors)
            x = redirect(reverse('administration:departments_list'))
        return x

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    extra_context = {"title": _('Department details')}

    def __init__(self, **kwargs):
        super(DepartmentDetailView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DepartmentForm(request.POST, instance=self.object)
        if form.is_valid() and form.changed_data:
            form.save()
        elif form.errors:
            log.warning(form.errors)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child_ids = [child.pk for child in self.object.child_departments.all()]
        available_parents = Department.objects.filter(
            Q(is_active=True, is_deleted=False)
            & ~Q(Q(pk=self.object.pk) | Q(pk__in=child_ids))
        )
        context['available_parents'] = available_parents
        return context


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department

    def __init__(self, *args, **kwargs):
        super(DepartmentDeleteView, self).__init__(*args, **kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.deleted_at = timezone.now()
        self.object.save()
        log_deletion(self.request, self.object)
        return redirect('/departments/')


class PositionListView(LoginRequiredMixin, ListView):
    model = Position

    def __init__(self, **kwargs):
        super(PositionListView, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        context['positions'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super(PositionListView, self).get_queryset().order_by('-id')
        return qs


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    form_class = DepartmentCreationForm

    def __init__(self, **kwargs):
        super(PositionCreateView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        form = PositionCreationForm(request.POST)
        if form.is_valid():
            form.save()
            log_addition(request, form.instance)
            kwargs.update({'pk': form.instance.pk})
            x = redirect(reverse('administration:position_detail', kwargs=kwargs))
        else:
            log.warning(form.errors)
            x = redirect(reverse('administration:positions_list'))
        return x

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position
    extra_context = {"title": _('Position details')}

    def __init__(self, **kwargs):
        super(PositionDetailView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PositionForm(request.POST, instance=self.object)
        if form.is_valid() and form.changed_data:
            form.save()
        elif form.errors:
            log.warning(form.errors)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child_ids = [child.pk for child in self.object.child_positions.all()]
        available_parents = Position.objects.filter(
            Q(is_active=True, is_deleted=False)
            & ~Q(Q(pk=self.object.pk) | Q(pk__in=child_ids))
        )
        context['available_parents'] = available_parents
        return context


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position

    def __init__(self, *args, **kwargs):
        super(PositionDeleteView, self).__init__(*args, **kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.is_active = False
        self.object.deleted_at = timezone.now()
        self.object.save()
        log_deletion(self.request, self.object)
        return redirect('/positions/')
