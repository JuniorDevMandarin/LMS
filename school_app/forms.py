from django import forms
from tinymce.widgets import TinyMCE

class NewsletterForm(forms.Form):


    subject = forms.CharField()
    receivers = forms.EmailField(label='Email:', required=False)
    message = forms.CharField(widget=TinyMCE(), label="Email content")