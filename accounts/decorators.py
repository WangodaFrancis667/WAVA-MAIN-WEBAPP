from django.contrib.auth.decorators import user_passes_test


def group_required(group_name):
    """
    Decorator for views that checks if a user is in a given group.
    Redirects to login page or a 'not-authorized' page if not.
    """

    def check_group(user):
        if not user.is_authenticated:
            return False

        # by passes the group check
        if user.is_superuser:
            return True

        # check if the user is is in the required group
        return user.groups.filter(name=group_name).exists()

    # user_passes_test handles the redirect to LOGIN_URL if check fails
    return user_passes_test(check_group)


# Buyer decorator
def buyer_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated
        and (u.groups.filter(name="Buyer").exists() or u.is_superuser),
        login_url="/login/",
        redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


# Supplier decorator
def supplier_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated
        and (u.groups.filter(name="Supplier").exists() or u.is_superuser),
        login_url="/login/",
        redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
