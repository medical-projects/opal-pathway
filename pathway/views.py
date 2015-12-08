"""
Views for the pathway OPAL Plugin
"""
from django.views.generic import TemplateView, View
from rest_framework import viewsets, mixins, routers
from rest_framework.response import Response
from opal.core.views import (
    LoginRequiredMixin, _get_request_data, _build_json_response,
)
from pathways import Pathway

from elcid.pathways import BloodCulturePathway


class PathwayIndexView(LoginRequiredMixin, TemplateView):
    """
    Main entrypoint into the pathway portal service.

    Lists our pathway routes.
    """
    template_name = 'pathway/index.html'


class PathwayDetailView(LoginRequiredMixin, View):
    """
    Return a JSON serialised pathway
    """
    def get(self, *args, **kwargs):
        pathway = Pathway.get(kwargs['name'])()
        serialised = _build_json_response(
            pathway.get_steps_info()
        )
        return serialised


class PathwayTemplateView(TemplateView):
    def dispatch(self, *args, **kwargs):
        self.name = kwargs.get('name', 'pathway')
        return super(PathwayTemplateView, self).dispatch(*args, **kwargs)

    def get_template_names(self, *args, **kwargs):
        return ['pathway/'+self.name, 'pathway/pathway_detail.html']


class SavePathway(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request):
        pathway = BloodCulturePathway()
        data = _get_request_data(request)
        episode = pathway.save(data, request.user)
        return Response({"episode": episode.id})


router = routers.SimpleRouter()
router.register(r'pathway/{}'.format(BloodCulturePathway().slug), SavePathway, base_name="pathway_create")
