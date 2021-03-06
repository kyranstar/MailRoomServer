from django.forms import CharField, Form, FileField, ClearableFileInput, ChoiceField, ModelChoiceField
from django.db import models
import csv
import datetime
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

class ProfileForm(Form):
   name = CharField(max_length = 500, required=False)
   file_field = FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)
   emails_field = FileField(widget=ClearableFileInput(), required=False)

   def extract_emails(namesfield, files, email_field):
       """
       Saves email_field to the database,  parses images in files for names,
       and then creates a list of emails from all the names in namesfield and the parsed names.

       Arguments:
        namesfield (`str`):
            Field of comma seperated names to email
        files (:obj:`list` of :obj:`UploadedFile`):
        email_field (:obj:`list` of `UploadedFile`):
            An empty list or a list of a csv file with name to email mappings.
        Returns:
            (matched_emails_data, unmatched_names, unmatched_images) where
            matched_emails are a list of EmailData associated with names in namesfield
            or in text read from files, unmatched_names is a list of elements
            from namesfield that had no associated email, unmatched_images is a
            list of elements from files that could not be parsed for an associated email.
       """
       # If we recievd an email_field, save it to database
       if(len(email_field) > 0):
           ProfileForm.save_email_file(email_field[0])

       # Load email mapping from database. TODO: If no emails, give an error
       emails = ProfileForm.load_email_file()

       # Clean given names
       names = map(lambda x: x.strip().lower(), namesfield.split(","))
       names = filter(lambda x: len(x) > 0, names)
       names = list(names)

       curr_date = datetime.datetime.now()

       # Find names that have emails and names that don't from namesfield
       matched_names = list(filter(lambda name: name in emails, names))
       unmatched_names = list(filter(lambda name: not name in matched_names, names))

       # Parse imageas for matching emails
       (matched_img_emails, unmatched_images) = ProfileForm.match_images_emails(emails, files)

       matched_emails = [EmailData(name, emails[name], curr_date) for name in matched_names] + matched_img_emails

       return (matched_emails, unmatched_names, unmatched_images)

   def match_images_emails(emails, image_files):
       """
       Takes a list of uploaded files, and for each image, tries to extract the name written in the image, and gets its associated email.
       Arguments:
        emails - a map from names to emails
        image_files - a list of UploadedFiles
       Returns:
        A tuple (matched_emails, unmatched_images) where matched_emails is a list of EmailData,
        and unmatched_images is a list of elmeents from image_files that could not be understood.
       """
       # TODO: implement
       return ([], image_files)

   def save_email_file(email_file):
       """
       Given a csv file with columns 'Name' and 'Email', saves this mapping to the EmailEntry database.
       Arguments:
        email_file (UploadedFile): The uploaded mapping from names to emails. If not a csv file, this method does nothing.
       """
       if (not email_file.name.endswith(".csv")):
           # TODO log error
           return
       # Clear database
       EmailEntry.objects.all().delete()
       data = csv.DictReader(email_file.read().decode('utf-8').splitlines())
       for line in data:
           try:
               entry = EmailEntry(name=line['Name'].strip().lower(), email=line['Email'])
               entry.save()
           except:
               # if the're a problem anywhere, you wanna know about it TODO better error logging
               print("there was a problem with line: " + str(line))

   def load_email_file():
       """
       Loads names and emails from the database and creates a dict.
       """
       return {entry.name: entry.email for entry in EmailEntry.objects.all()}

class SubmitForm(Form):
    name = CharField(max_length = 500)
    selected_template = ModelChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
       super(SubmitForm, self).__init__(*args, **kwargs)
       self.fields['selected_template'].queryset = EmailTemplate.objects.all()

    def send_emails(self, emails, template):
        for emaildata in emails:
            substituted = emaildata.substitute(template)
            html_content = substituted.body
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(substituted.subject, text_content, 'baker-mail-room@example.com', [emaildata.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

class CreateTemplateForm(Form):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)

    def save_template(name, subject, body):
        EmailTemplate(name=name, subject=subject, body=body).save()
        print(EmailTemplate.objects.all())

class EmailTemplate(models.Model):
    """
    A model representing an email template.
    """
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)


class EmailEntry(models.Model):
    """
    A model representing an entry in the mapping from names to emails.
    """
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

class EmailData:
    """A structure representing all the data needed to send an email.

    Attributes:
        name (str): The name of the person receiving the email.
        email (str): The email of the person.
        date (:obj:`datetime`): The date the package was recieved.
    """
    def __init__(self, name, email, date):
        self.name = name
        self.email = email
        self.date = date

    def substitute(self, template):
        template.subject = template.subject.replace("%name%", self.name)
        template.subject = template.subject.replace("%email%", self.email)
        template.subject = self.date.strftime(template.subject)
        template.body = template.body.replace("%name%", self.name)
        template.body = template.body.replace("%email%", self.email)
        template.body = self.date.strftime(template.body)
        print(template)
        return template
    def __str__(self):
        return "{Name: %s, Email: %s, Date: %s}" % (self.name, self.email, str(self.date))
    def __repr__ (self):
        return "{Name: %s, Email: %s, Date: %s}" % (repr(self.name), repr(self.email), repr(self.date))
