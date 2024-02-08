from django import forms
from .models import Balance, Item, Feedback

class BalanceForm(forms.ModelForm):
    class Meta:
            model = Balance
            fields = ['amount']
                
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price','desc']
        
class InitialSavingsForm(forms.ModelForm):
        class Meta:
            model = Balance
            fields = ['savings']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['profile_picture'] 
        
class SearchForm(forms.Form):
    fields =  ['searched'] 
        
            

         

