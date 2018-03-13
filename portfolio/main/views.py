from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from wagtail.documents.models import Document


class IndexView(TemplateView):
    template_name = "main/home_page.html"


class S3DocumentServe(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        document_id = kwargs['document_id']
        document = get_object_or_404(Document, id=document_id)
        return document.file.url
