# -*- encoding: utf-8 -*-
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_user_groups(sender, **kwargs):
    """
    Creates the 'Buyer' and 'Supplier' groups when the app is migrated.
    """
    # We import models here to avoid AppRegistryNotReady error
    from django.contrib.auth.models import Group

    # get_or_create returns a tuple (object, created_boolean)
    Group.objects.get_or_create(name="Buyer")
    Group.objects.get_or_create(name="Supplier")
    # We don't need an 'Admin' group because is_superuser handles this.


class AccountsConfig(AppConfig):
    # The app package is named `auth` in this project, so AppConfig.name
    # AppConfig.name must be the full import path to this app's package.
    # Set it to the actual package name 'accounts' so Django can import it.
    name = "accounts"
    # Use a distinct label to avoid colliding with the built-in
    # 'auth' label from django.contrib.auth.
    label = "accounts"
    verbose_name = "Accounts"

    def ready(self):
        # Connect the signal handler
        post_migrate.connect(create_user_groups, sender=self)
