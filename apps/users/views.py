from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
#generic 类
from django.views.generic.base import View
#给明文加密
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from .forms import *
# Create your views here.
from .models import *
from utils.mixin_utils import LoginRequiredMixin
from operation.models import *
from organization.models import *

#自定义登录方式(指:用邮箱还是用用户名登录)


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #前端传来的密码是明文,所以不能用不能直接用上方法查询
            #check_password方法可以可将明文转为密文并和用户名做判断
            if user.check_password(password):
                return user
        except Exception as e:
            return None
#基于类:
class LogoutView(View):
    """
    退出
    """
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import  reverse
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        #request传入到LoginForm会自动判断如:是否为空,最小字节数等信息
        #所以表单的字段名要HMTL中的name的值相对应(Django中的form检验是对应名判断)
        login_form = LoginForm(request.POST)
        #is_valid()方法判断验证是否有错
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 验证账号和密码的
            # authenticate参数是密码和用户名如果正确返回用户的对象,如果不存在则返回None
            user = authenticate(username=user_name, password=password)
            if user is not None:
                # 完成登录
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {"msg": "用户未激活","login_form":login_form})
            else:
                return render(request, 'login.html', {"msg": "用户名密码错误","login_form":login_form})
        else:
            return render(request,'login.html',{"login_form":login_form})

#基于函数
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get('username','')
#         password = request.POST.get('password','')
#         #验证账号和密码的
#         #authenticate参数是密码和用户名如果正确返回用户的对象,如果不存在则返回None
#         user = authenticate(username=user_name,password=password)
#         if user is not None:
#             #完成登录
#             login(request,user)
#             return render(request,'index.html',{})
#         else:
#             return render(request,'login.html',{"msg":"用户名密码错误"})
#
#     elif request.method == "GET":
#         return render(request,'login.html',{})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email",'')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"register_form": register_form,'msg':'用户已经存在'})
            pass_word = request.POST.get("password",'')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = True
            user_profile.save()
            #写入欢迎注册消息
            user_message =UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册暮学在在线网'
            user_message.save()
            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request,'register.html',{"register_form":register_form})

#邮箱处理
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse("链接已失效")
        return render(request,'login.html')

#处理忘记密码的处理:
class ForgetPwView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, 'forget')
            return HttpResponse("邮件已经发送成功,请注意成功")
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


#重置密码:
class ResetView(View):
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for user in all_records:
                email = user.email
                return render(request,'password_reset.html',{"email":email})
        else:
            return HttpResponse("链接已失效")
        return render(request, 'login.html')

#修改密码


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self,request):
        modify_form = ModifyPwdform(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1",'')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,"msg":'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        userinfo = UserinfoForm(request.POST,instance=request.user)
        if userinfo.is_valid():
            userinfo.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo.errors), content_type='application/json')



class UploadImageView(LoginRequiredMixin,View):
    """
    用户修改图像
    """
    def post(self,request):
        image_form = UplaodImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    在个人中心修改用户密码
    """
    def post(self,request):
        modify_form = ModifyPwdform(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1",'')
            pwd2 = request.POST.get("password2", '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
           return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    """
    修改个人邮箱
    """
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        eixted_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if eixted_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{'user_courses':user_courses})


class MyFavOrfView(LoginRequiredMixin,View):
    '''
    我收藏课程机构
    '''
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id

            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{'org_list':org_list})


class MyFavTeacherView(LoginRequiredMixin,View):
    """
    我收藏的授课的讲师
    """

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id

            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list})


class MyFavCouserView(LoginRequiredMixin,View):
    """
    我收藏的课程
    """
    def get(self, request):
        couser_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id

            course = Course.objects.get(id=course_id)
            couser_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'couser_list': couser_list})


class MyMessageView(LoginRequiredMixin,View):
    """
    我的消息
    """
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user= request.user.id, has_read=False)
        for all_unread_message in all_unread_messages:
            all_unread_message.has_read = True
            all_unread_message.save()
        #对个人信息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{'messages':messages})

class IndexView(View):
    def get(self,request):
        #取出轮播图:
        print
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request ,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,

        })



def page_not_found(request):
    #全局404函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_orror(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response