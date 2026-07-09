


from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from .services import UserService


def register(request):
	"""
	Register a new customer account
	"""
	if request.user.is_authenticated:
		return redirect("home")
	
	if request.method=="POST":
		
		form=UserRegistrationForm(request.POST)
		
		if form.is_valid():
			user=UserService.create_user(
	username=form.cleaned_data["username"],
	email=form.cleaned_data["email"],
	password=form.cleaned_data["password"],
	first_name=form.cleaned_data["first_name"],
	last_name=form.cleaned_data["last_name"],
			)
			
			messages.success(
			request,
			"Account created successfully."
			)
			
			login(request, user)
			
			return redirect("home")
			
			
	else:
		form=UserRegistrationForm()
		
	return render(
	  request,
	  "accounts/register.html",
	  {
	     "form":form
	  },
	)


def user_login(request):
    """
    Authenticate an existing user.
    """

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            login(
                request,
                form.cleaned_data["user"],
            )

            messages.success(
                request,
                "Welcome back!"
            )

            return redirect("home")

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )

@login_required
def user_logout(request):
    """
    Logout the current user.
    """

    logout(request)

    messages.info(
        request,
        "You have been logged out."
    )

    return redirect("login")


@login_required
def profile(request):
    """
    Display the logged-in user's profile.
    """

    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user
        },
    )