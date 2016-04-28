from django.http import JsonResponse
from django.views.generic.base import TemplateView

from jsonform.views import JsonFormBase

from .forms import ExampleForm


class ContainerView(TemplateView):

    template_name = "jsonform_example/container.html"


class SubClass(JsonFormBase):

    template_name = "jsonform_example/form.html"
    form_class = ExampleForm

    def success(self):
        # Log to console as an example (use DB in real life, probably)...
        print(self.serialized_form_data)

        # Change template before calling get_json_data to get updated html
        self.template_name = "jsonform_example/success.html"
        data = self.get_json_data()
        return JsonResponse(data=data)
