from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.base import TemplateView

from portfolio.main.models import Entry
from portfolio.main.utils import (
    featured_entries_by_slot, published_entries_by_date)


class FeaturedView(TemplateView):
    template_name = 'featured/index.html'

    def initialize_slots(self):
        slots = [None] * 3
        for entry in featured_entries_by_slot():
            slots[entry.feature_slot] = entry
        return slots

    def get_context_data(self, **kwargs):
        context = super(FeaturedView, self).get_context_data(**kwargs)
        context['slots'] = self.initialize_slots()
        context['entries'] = published_entries_by_date()
        return context

    def set_featured(self, key):
        try:
            entry = Entry.objects.get(id=self.request.POST[key])
            entry.feature_on_homepage = True

            ordinal = entry.featured_slot = key.split('-')[-1]
            entry.feature_slot = int(ordinal) - 1

            blurb = self.request.POST['feature-blurb-{}'.format(ordinal)]
            entry.feature_blurb = blurb

            entry.save()
        except (ValueError, Entry.DoesNotExist):
            pass

    def post(self, *args, **kwargs):
        # reset all featured attributes
        Entry.objects.all().update(
            feature_on_homepage=False, feature_slot=None, feature_blurb=None)

        # set newly featured entries
        for key in self.request.POST:
            if key.startswith('feature-entry'):
                self.set_featured(key)

        return HttpResponseRedirect(reverse('featured'))
