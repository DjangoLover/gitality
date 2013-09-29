from django.contrib.webdesign import lorem_ipsum

import factory

from core.factories import UserFactory

from .models import Project


class ProjectFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = Project

    name = factory.Sequence(
        lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0).title(), n)
    )
    user = factory.SubFactory(UserFactory)
    repo_url = factory.LazyAttribute(
        lambda a: u'https://github.com/{0}/{1}'.format(
            a.user.username,
            a.name.lower()
        )
    )
