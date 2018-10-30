from django.forms import CharField, Form, FileField, ClearableFileInput

class ProfileForm(Form):
   name = CharField(max_length = 100, required=False)
   file_field = FileField(widget=ClearableFileInput(attrs={'multiple': True}))

   def send_email():
       print("Sending email")
