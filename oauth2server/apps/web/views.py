from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from apps.web.decorators import validate_query_string
from apps.web.forms import AuthorizeForm
from apps.web import SCOPES


class AuthorizeView(View):
    form_class = AuthorizeForm
    initial = {}
    template_name = 'web/authorize.html'

    @method_decorator(validate_query_string)
    def dispatch(self, *args, **kwargs):
        return super(AuthorizeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return self._render(request=request, form=form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return self._render(request=request, form=form)

        return request.response_type.process(
            client=request.client,
            authorized=form.cleaned_data['authorize'],
            scopes=form.cleaned_data['scopes'],
            redirect_uri=request.GET['redirect_uri'],
            state=request.GET['state'],
        )

    def _render(self, request, form):
        return HttpResponse(render(request, self.template_name, {
            'title': 'Authorize', 'client': request.client,
            'form': form, 'scopes': SCOPES,}))