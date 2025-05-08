from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Home(View):
    def get(self, request):
        return render(request, "index.html")

@method_decorator(login_required, name="dispatch")    
class ProfildList(View):
    def get(self, request):
        profiles = request.user.profiles.all()
        print(profiles)
        return render(request, "profileList.html", {
            "profiles": profiles
        })