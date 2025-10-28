from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group  # <-- Import the Group model
from .forms import LoginForm, SignUpForm

# import the decorators
from django.contrib.auth.decorators import login_required
from .decorators import buyer_required, supplier_required


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Role based redirect
                if user.is_superuser:
                    return redirect("/admin/")

                if user.groups.filter(name="Supplier").exists():
                    return redirect("/supplier-dashboard/")
                elif user.groups.filter(name="Buyer").exists():
                    return redirect("/buyer-dashboard/")

                # Fallback homepage
                return redirect("/")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


# Registration View
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # --- Add user to default 'Buyer' group ---
            try:
                buyer_group = Group.objects.get(name="Buyer")
                user.groups.add(buyer_group)
            except Group.DoesNotExist:
                msg = 'Warning: "Buyer" group not found. User created without role.'

            if not msg:
                msg = 'User created - please <a href="/login">login</a>.'

            success = True
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form, "msg": msg, "success": success},
    )


# Managing views using decorators
@login_required  # Ensures user is logged in for this basic homepage
def home_view(request):
    return render(request, "home/index.html")


# Only the supplier's view
@login_required
@supplier_required
def supplier_dashboard_view(request):
    return render(request, "supplier/dashboard.html")


# Only the buyers view
@login_required
@buyer_required
def buyer_dashboard_view(request):
    return render(request, "buyer/dashboard.html")
