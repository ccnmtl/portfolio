from datetime import datetime

from django.contrib.auth.models import User, Group
import factory

from portfolio.main.models import Entry, Partner, AwardType, ProjectType, \
    Discipline


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')
    email = factory.LazyAttribute(lambda u: '%s@example.com' % u.username)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group


class AwardTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AwardType

    name = factory.Sequence(lambda n: 'Award%d' % n)


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discipline

    name = factory.Sequence(lambda n: 'Discipline %d' % n)


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    name = factory.Sequence(lambda n: 'Project Type %d' % n)


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry
    title = factory.Sequence(lambda n: 'entry{}'.format(n))
    depth = 1
    release_date = factory.LazyFunction(datetime.now)
    revision_date = factory.LazyFunction(datetime.now)

    @factory.post_generation
    def project_type(obj, create, extracted, **kwargs):
        if extracted:
            obj.project_type.add(extracted)

    @factory.post_generation
    def award_type(obj, create, extracted, **kwargs):
        if extracted:
            obj.award_type.add(extracted)


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partner

    name = 'James Moriarty'
    affiliation = 'Mathematics'
    short_title = 'Professor of Mathematics'
    full_title = 'Professor and Mathematical Chair'
