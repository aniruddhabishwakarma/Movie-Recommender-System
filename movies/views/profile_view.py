from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from movies.models.movie_model import Favorite, Review  # Import models
from django.contrib import messages
from movies.models.auth_model import *
from django.contrib.auth import update_session_auth_hash,authenticate

@login_required
def profile_view(request):
    """User Profile Page"""
    user = request.user  # ✅ Get logged-in user

    # ✅ Get favorite movies of the user
    favorite_movies = Favorite.objects.filter(user=user).select_related("movie")

    # ✅ Get recently reviewed movies
    recent_reviews = Review.objects.filter(user=user).select_related("movie").order_by("-created_at")[:5]

    context = {
        "user": user,
        "favorite_movies": favorite_movies,
        "recent_reviews": recent_reviews,
    }
    return render(request, "movies/profile.html", context)

@login_required
def settings_view(request):
    """User Settings Page"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        contact = request.POST.get("contact", "").strip()
        profile_photo = request.FILES.get("profile_photo")

        # ✅ Ensure None values are replaced with empty strings
        user_profile.full_name = full_name if full_name else ""
        user_profile.contact = contact if contact else ""

        # ✅ Update Profile Picture
        if profile_photo:
            user_profile.profile_photo = profile_photo

        user_profile.save()

        messages.success(request, "Your profile has been updated!")
        return redirect("settings")

    return render(request, "movies/settings.html", {
        "user_profile": user_profile
    })



@login_required
def change_password_view(request):
    """Change Password"""
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")

        # Authenticate the current password
        user = authenticate(username=request.user.username, password=current_password)

        if user:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # ✅ Keep user logged in
            messages.success(request, "Your password has been changed!")
        else:
            messages.error(request, "Current password is incorrect.")

        return redirect("settings")

    return redirect("settings")