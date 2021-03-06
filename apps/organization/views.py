from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
from .models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from courses.models import *
from operation.models import *

class OrgView(View):
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        #计算数量
        orgs_nums = all_orgs.count()
        #按点击量排序:
        hot_org = all_orgs.order_by("-click_nums")[:3]
        #城市
        all_city = CityDict.objects.all()
        #机构搜索
        seacher_keywords = request.GET.get('keywords', '')

        if seacher_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=seacher_keywords) | Q(desc__icontains=seacher_keywords))
        #取出筛选城市
        city_id = request.GET.get('city','')
        #按学习人数/课程数排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_num')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        #类别筛选:
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 计算数量
        orgs_nums = all_orgs.count()
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        return render(request,'org-list.html',{'all_orgs':orgs,'orgs_nums':orgs_nums,'all_city':all_city,'city_id':city_id,'category':category,'hot_org':hot_org,"sort":sort})


class AddUserAskView(View):
    """"
        用户添加咨询
    """

    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #直接保存数据库,如果commit=False只是提交不做保存
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"sucess"}',content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')



class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    """
    课程详情
    """
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class OrgDescView(View):
    """
    课程介绍
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{

            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',{

            'course_org':course_org,
            'all_teacher':all_teacher,
            'current_page':current_page,
            'has_fav': has_fav,
        })

class AddFavView(View):
    """"
    用户收藏,用户取消收藏
    """
    def post(self,request):
        fav_id = request.POST.get("fav_id",0)
        fav_type =request.POST.get("fav_type",0)
        #先判断用户是否登錄
        if not request.user.is_authenticated():
            #
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_reconds = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_reconds:
            #如果记录已经存在,在表示用户取消收藏
            exist_reconds.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums <0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_type)>0 and int(fav_id)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self,request):
        all_techers = Teacher.objects.all()
        seacher_keywords = request.GET.get('keywords', '')

        if seacher_keywords:
            all_techers = all_techers.filter(
                Q(name__icontains=seacher_keywords)|Q(work_company__icontains=seacher_keywords)|Q(work_position__icontains=seacher_keywords))
        sort = request.GET.get('sort','')
        if sort:
            all_techers = all_techers.order_by('-click_nums')
        sorted_teacher =  Teacher.objects.all().order_by('-click_nums')[:3]
        #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_techers, 1, request=request)
        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_techers':teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort ,
        })

class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        #讲师排行
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        all_courses = Course.objects.filter(teacher=teacher)
        has_teacher_faved = False
        has_org_faved = False
        try:
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
                has_teacher_faved = True
            if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
                has_org_faved = True
        except:
            pass
        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved,
        })