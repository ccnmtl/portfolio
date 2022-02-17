from django.contrib.auth.models import User, Group
from datetime import datetime
import factory
from portfolio.main.models import Entry, Partner


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry
    title = factory.Sequence(lambda n: 'entry{}'.format(n))
    depth = 1
    release_date = factory.LazyFunction(datetime.now)
    revision_date = factory.LazyFunction(datetime.now)


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partner

    name = 'James Moriarty'
    affiliation = 'Mathematics'
    short_title = 'Professor of Mathematics'
    full_title = 'Professor and Mathematical Chair'
