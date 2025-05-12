from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Movie, Profile

class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:profile_list")
        return render(request, "index.html")

@method_decorator(login_required, name="dispatch")    
class ProfileList(View):
    def get(self, request):
        profiles = request.user.profiles.all()
        print(profiles)
        return render(request, "profileList.html", {
            "profiles": profiles
        })

@method_decorator(login_required, name="dispatch")
class ProfileCreate(View):
    def get(self, request):
        # form for creating profile
        form = ProfileForm()
        return render(request, "profileCreate.html", {
            'form': form
        })
    
    def post(self, request):
        form = ProfileForm(request.POST or None)

        if form.is_valid():
            profile = Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile)
                return redirect("core:profile_list")

        return render(request, "profileCreate.html", {
            "form": form
        })

@method_decorator(login_required, name="dispatch")
class Watch(View):
    def get(self, request, profile_id):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit=profile.age_limit)

            if profile not in request.user.profiles.all():
                return redirect(to="core:profile_list")
            return render(request, "movieList.html", {
                "movies": movies
            })
        except Profile.DoesNotExist:
            return redirect(to="core:profile_list")
