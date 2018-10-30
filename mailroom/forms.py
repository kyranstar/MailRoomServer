from django.forms import CharField, Form, FileField, ClearableFileInput
from django.db import models
import csv

class ProfileForm(Form):
   name = CharField(max_length = 500, required=False)
   file_field = FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)
   emails_field = FileField(widget=ClearableFileInput(), required=False)

   """
   Extracts names from a given comma seperated names field, and a set of image
   files to run character recognition on.
   """
   def extract_emails(self, namesfield, files, email_field):
       if(len(email_field) > 0):
           self.save_email_file(email_field[0])

       emails = self.load_email_file()
       # Get map from names to emails

       names = map(lambda x: x.strip().lower(), namesfield.split(","))
       names = filter(lambda x: len(x) > 0, names)
       names = list(names)


       matched_names = list(filter(lambda name: name in emails, names))

       unmatched_names = list(filter(lambda name: not name in matched_names, names))

       (matched_img_emails, unmatched_images) = self.match_images_emails(emails, files)

       matched_emails = [emails[name] for name in matched_names] + matched_img_emails

       return (matched_emails, unmatched_names, unmatched_images)

   def match_images_emails(self, emails, image_files):
       # TODO implement
       return ([], image_files)

   def save_email_file(self, email_file):
       if (email_file.name.endswith(".csv")):
           # Clear database
           EmailEntry.objects.all().delete()
           data = csv.DictReader(email_file.read().decode('utf-8').splitlines())
           for line in data:
               if not 'Name' in line or not 'Email' in line:
                   continue

               entry = EmailEntry(name=line['Name'].strip().lower(), email=line['Email'])
               try:
                   entry.save()
               except:
                   # if the're a problem anywhere, you wanna know about it
                   print("there was a problem with line: " + str(line))
           return

   def load_email_file(self):
       return {entry.name: entry.email for entry in EmailEntry.objects.all()}

class EmailEntry(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
