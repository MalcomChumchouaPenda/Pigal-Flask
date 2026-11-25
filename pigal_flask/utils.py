import os
import re
import sys
import pytest
from pathlib import Path
from flask import Flask
from flask_restx import Namespace
from sqlalchemy.orm import declared_attr


class TestUI:
    pass


def __find_key(cls):
    name_parts = cls.__module__.split(".")
    i = name_parts.index("models")
    return name_parts[i - 1]


@declared_attr
def bind_key(cls):
    return __find_key(cls)


@declared_attr
def tablename(cls):
    key = __find_key(cls)
    name = cls.__name__.lower()
    return f"{key}_{name}"


class AccessProviderContract:

    @pytest.fixture
    def app(self):
        return Flask(__name__)

    @pytest.fixture
    def provider(self):
        """
        Doit être redéfini par chaque implémentation.
        """
        raise NotImplementedError

    @pytest.fixture
    def provider_factory(self):
        """
        Fournit une factory permettant de créer un provider isolé.
        """
        raise NotImplementedError

    @pytest.fixture
    def user_credentials(self):
        raise NotImplementedError

    def test_initial_state_is_not_authenticated(self, provider):
        assert provider.identity() is None
        assert provider.is_authenticated() is False

    def test_authentication_sets_identity(self, provider, user_credentials):
        result = provider.authenticate(user_credentials)

        assert result is True
        assert provider.identity() is not None
        assert provider.is_authenticated() is True

    def test_logout_removes_identity(self, provider, user_credentials):
        provider.authenticate(user_credentials)
        provider.logout()

        assert provider.identity() is None
        assert provider.is_authenticated() is False

    def test_existing_role(self, provider, authenticated_identity):
        assert provider.has_role("admin") is True

    def test_missing_role(self, provider, authenticated_identity):
        assert provider.has_role("unknown") is False

    def test_existing_permission(self, provider, authenticated_identity):
        assert provider.has_permission("users.read") is True

    def test_missing_permission(self, provider, authenticated_identity):
        assert provider.has_permission("users.delete") is False

    def test_identity_is_stable_after_authentication(self, provider, user_credentials):
        provider.authenticate(user_credentials)

        identity_1 = provider.identity()
        identity_2 = provider.identity()

        assert identity_1 is identity_2

    def test_identity_is_isolated_between_contexts(self, app, provider_factory):
        with app.test_request_context("/"):
            provider = provider_factory()

            provider.authenticate({"username": "alice"})

            alice = provider.identity()

        with app.test_request_context("/"):
            provider = provider_factory()

            provider.authenticate({"username": "bob"})

            bob = provider.identity()

        print(alice, bob)
        assert alice != bob
        assert alice["id"] != bob["id"]

    def test_provider_requires_flask_context(self, provider):
        """
        Optionnel :
        uniquement si le provider dépend réellement
        du contexte Flask.
        """

        with pytest.raises(RuntimeError):
            provider.identity()

    def test_provider_works_inside_flask_context(self, app, provider, user_credentials):
        with app.test_request_context("/"):

            provider.authenticate(user_credentials)

            assert provider.identity() is not None
