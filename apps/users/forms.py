from django import forms
from captcha.fields import CaptchaField
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


#定义验证码的form
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    #error_messages:自定义错误提示信息
    captcha = CaptchaField(error_messages={'invalid':"验证码错误"})



class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    #error_messages:自定义错误提示信息
    captcha = CaptchaField(error_messages={'invalid':"验证码错误"})

class ModifyPwdform(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UplaodImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserinfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address','mobile']

