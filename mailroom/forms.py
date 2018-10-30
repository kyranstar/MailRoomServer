from django.forms import CharField, Form, FileField, ClearableFileInput

class ProfileForm(Form):
   name = CharField(max_length = 500, required=False)
   file_field = FileField(widget=ClearableFileInput(attrs={'multiple': True}), required=False)

   def process_data(self, names, files):
       print("PRINTING")
       print(names)
       print(files)
       print("processing email")
