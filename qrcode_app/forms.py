from django import forms
from allauth.account.forms import SignupForm
from .models import Profile


class CustomSignupForm(SignupForm):
    business_name = forms.CharField(max_length=100, required=False)
    business_address = forms.CharField(widget=forms.Textarea, required=False)
    contact_number = forms.CharField(max_length=15, required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.profile.business_name = self.cleaned_data.get('business_name')
        user.profile.business_address = self.cleaned_data.get('business_address')
        user.profile.contact_number = self.cleaned_data.get('contact_number')
        user.profile.save()
        return user


class BusinessInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['business_name', 'business_address', 'contact_number', 'profile_picture', 'banner_image']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class TwoFactorForm(forms.Form):
    code = forms.CharField(max_length=6)