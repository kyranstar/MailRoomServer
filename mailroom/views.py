from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.views import View

from .forms import ProfileForm
#from .models import Profile

class UploadDataView(View):
    form_class = ProfileForm
    template_name = 'uploaded.html'


    def get(self, request):
        MyProfileForm = self.form_class()
        return render(request, self.template_name, locals())


    def post(self, request):
        saved = False
        #Get the posted form
        MyProfileForm = self.form_class(request.POST, request.FILES)

        if MyProfileForm.is_valid():
            #profile.save()
            (matched_emails, unmatched_names, unmatched_images) = MyProfileForm.extract_emails(MyProfileForm.cleaned_data["name"], request.FILES.getlist('file_field'), request.FILES.getlist('emails_file'))
            saved = True

        return render(request, self.template_name, locals())
