from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import ModelFormMixin


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class UserOwnerMixin(object):
    """
    Filters queryset per request user as an owner
    """

    user_field = 'user'

    def get_queryset(self):
        qs = super(UserOwnerMixin, self).get_queryset()
        payload = {self.user_field: self.request.user}
        return qs.filter(**payload)


class UserFormMixin(ModelFormMixin):
    """
    Sets request user as an object attribute before save
    """

    user_field = 'user'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        setattr(self.object, self.user_field, self.request.user)
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class ExcludeFormMixin(object):
    """
    Excludes fields from model form
    """

    exclude_form_fields = ()

    def exclude_form_factory(self, form, exclude=()):
        """
        Dynamically add exclude constraint to model form meta
        """
        Meta = type('Meta', (form.Meta,), {'exclude': exclude})
        return type(form.__name__, (form,), {'Meta': Meta})

    def get_form_class(self):

        form = super(ExcludeFormMixin, self).get_form_class()

        if isinstance(self.exclude_form_fields, (list, tuple)):
            form = self.exclude_form_factory(form, self.exclude_form_fields)

        return form
