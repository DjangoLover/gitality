from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum

from django.contrib.auth.hashers import make_password

import factory


class UserFactory(factory.django.DjangoModelFactory):

    FACTORY_FOR = User

    username = factory.Sequence(
        lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n)
    )
    email = factory.LazyAttribute(
        lambda a: u'{0}@localhost.local'.format(a.username)
    )
    # Using the simplest hasher to make it faster
    password = make_password('qwerty', hasher='crypt')
