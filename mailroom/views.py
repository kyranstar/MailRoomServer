from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.views import View

from .forms import ProfileForm
from .models import Profile

class SaveProfileView(View):
    form_class = ProfileForm
    template_name = 'saved.html'


    def get(self, request):
        MyProfileForm = self.form_class()
        return render(request, self.template_name, locals())


    def post(self, request):
        saved = False
        print(request.POST)
        print()
        print(request.FILES)
        #Get the posted form
        MyProfileForm = self.form_class(request.POST, request.FILES)

        if MyProfileForm.is_valid():
            profile = Profile()
            profile.name = MyProfileForm.cleaned_data["name"]
            #profile.save()
            saved = True
        print(MyProfileForm.errors)
        print()
        print(locals())
        print(saved)

        return render(request, self.template_name, locals())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
