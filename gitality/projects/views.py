from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    ListView,
    DeleteView
)

from core.mixins import (
    ExcludeFormMixin,
    LoginRequiredMixin,
    UserFormMixin,
    UserOwnerMixin
)
from .models import Project


class ProjectListView(ListView):

    model = Project

project_list = ProjectListView.as_view()


class ProjectDetailView(DetailView):

    model = Project

project_detail = ProjectDetailView.as_view()


class ProjectCreateView(LoginRequiredMixin, ExcludeFormMixin, UserFormMixin, CreateView):

    model = Project
    exclude_form_fields = ('user',)

project_create = ProjectCreateView.as_view()


class ProjectUpdateView(LoginRequiredMixin, ExcludeFormMixin, UserFormMixin, UpdateView):

    model = Project
    exclude_form_fields = ProjectCreateView.exclude_form_fields

project_update = ProjectUpdateView.as_view()
