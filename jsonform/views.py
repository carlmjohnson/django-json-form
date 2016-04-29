import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.template import loader
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, View


class JsonFormBase(ContextMixin, View):
    # To use, set these in subclass:
    template_name = None
    form_class = lambda data: None

    def dispatch(self, request, *args, **kwargs):
        self.post_data = request.POST if request.method == 'POST' else None
        return super(JsonFormBase, self).dispatch(request, *args, **kwargs)

    @cached_property
    def form(self):
        return self.form_class(data=self.post_data)

    def post(self, request):
        if self.form.is_valid():
            return self.success()

        return self.get(request)

    def get(self, request, *args, **kwargs):
        data = self.get_json_data()
        return JsonResponse(data=data)

    def get_json_data(self):
        return {
            'changed_data': self.form.changed_data,
            'cleaned_data': getattr(self.form, 'cleaned_data', {}),
            'html': loader.render_to_string(
                self.template_name,
                context=self.get_context_data(),
                request=self.request,
            ),
            'is_valid': self.form.is_valid(),
            'raw_data': self.form.data,
        }

    def get_context_data(self, **kwargs):
        context = super(JsonFormBase, self).get_context_data(**kwargs)
        context.update({
            'form': self.form,
        })
        return context

    def success(self):
        """
        Implement in subclass
        """
        raise NotImplementedError

    @cached_property
    def serialized_form_data(self):
        return json.dumps(self.form.cleaned_data, cls=DjangoJSONEncoder)
