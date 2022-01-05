from django import forms
from operation.models import *
import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model= UserAsk
        #指定字段
        fields = ['name', 'mobile', 'course_name']
        #验证手机号格式必须按照以下格式:

    def clean_mobile(self):
        """
        验证手机号是否合法

        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法',code='mobile_invalid')
