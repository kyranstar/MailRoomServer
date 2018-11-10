from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.views import View

from .forms import ProfileForm, SubmitForm, CreateTemplateForm, EmailTemplate
#from .models import Profile

class UploadDataView(View):
    form_class = ProfileForm
    template_name = 'uploaded.html'


    def get(self, request):
        templates = EmailTemplate.objects.all()
        MyProfileForm = self.form_class()
        return render(request, self.template_name, locals())


    def post(self, request):
        saved = False
        #Get the posted form
        MyProfileForm = self.form_class(request.POST, request.FILES)

        if MyProfileForm.is_valid():
            (matched_emails, unmatched_names, unmatched_images) = ProfileForm.extract_emails(MyProfileForm.cleaned_data["name"], request.FILES.getlist('file_field'), request.FILES.getlist('emails_file'))
            matched_names = ", ".join(list(map(lambda email_data: email_data.name, matched_emails)))
            saved = True

        templates = EmailTemplate.objects.all()
        return render(request, self.template_name, locals())

class CreateTemplateView(View):
    form_class = CreateTemplateForm
    template_name = 'create_email_template.html'


    def get(self, request):
        selected_html_template = "<b>hi</b>"
        return render(request, self.template_name, locals())


    def post(self, request):
        #Get the posted form
        MyForm = self.form_class(request.POST, request.FILES)

        if MyForm.is_valid():
            CreateTemplateForm.save_template(MyForm.data['name'], MyForm.data['subject'], MyForm.data['body'])
            return HttpResponseRedirect("/")
        else:
            return render(request, self.template_name, locals())

class SendEmailsView(View):
    form_class = SubmitForm
    template_name = 'submit.html'

    def get(self, request):
        submit_form = self.form_class()
        return render(request, self.template_name, locals())

    def post(self, request):
        success = False
        #Get the posted form
        submit_form = self.form_class(request.POST, request.FILES)

        if submit_form.is_valid():
            success = True
            (matched_emails, unmatched_names, unmatched_images) = ProfileForm.extract_emails(submit_form.cleaned_data['name'],  [], [])
            template = submit_form.cleaned_data["selected_template"]
            submit_form.send_emails(matched_emails, template)


        # TODO load error_msg
        error_msg = submit_form.errors

        return render(request, self.template_name, locals())
