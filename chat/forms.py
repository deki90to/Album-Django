from django import forms
from . models import ChatMessages


class ChatMessagesForm(forms.ModelForm):
    class Meta:
        model = ChatMessages
        fields = '__all__'