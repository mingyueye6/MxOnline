from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import *
from django.http import HttpResponse
from django.db.models import Q
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_num')[:3]
        sort = request.GET.get('sort','')
        #课程搜索
        seacher_keywords = request.GET.get('keywords','')

        if seacher_keywords:
            all_course  = all_course.filter(Q(name__icontains=seacher_keywords)|Q(desc__icontains=seacher_keywords)|Q(detail__icontains=seacher_keywords))


        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_num')
        #对课程进行分析
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 9, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{'all_course':courses,'sort':sort,
                                                  'hot_courses':hot_courses,
                                                })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #增加课程点击数
        course.click_num += 1
        course.save()
        tag = course.tag
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,'course-detail.html',{'course':course,'relate_courses':relate_courses,'has_fav_course':has_fav_course,'has_fav_org':has_fav_org })


class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self,request,course_id):

        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #查询用户是否已经关联了该课程

        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
        user_ids = [user_couser.user.id for user_couser in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程
        course_ids = [user_couser.course.id for user_couser in user_courses]
        #现在获取学过该用户的所有的课程
        relate_courses= Course.objects.filter(id__in = course_ids).order_by('-click_num')[:5]
        all_resources = CourseResourse.objects.filter(course=course)
        return render(request,'course-video.html',{
            'course':course,
            'course_resourse':all_resources,
            'relate_courses': relate_courses,

        })


class CommentsView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResourse.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # if not user_courses:
        #     user_course = UserCourse(user=request.user, course=course)
        #     user_course.save()
        user_ids = [user_couser.user.id for user_couser in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程
        course_ids = [user_couser.course.id for user_couser in user_courses]
        # 现在获取学过该用户的所有的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_resources = CourseResourse.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resourse': all_resources,
            'all_comments':all_comments,
            'relate_courses': relate_courses,
        })

class AddCommentView(View):
    """
    课程添加客户评论
    """
    def post(self,request):
        if not request.user.is_authenticated():

            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) >0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')


class VideoPalyView(View):
    """
    视频播放页面
    """
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联了该课程

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_ids = [user_couser.user.id for user_couser in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程
        course_ids = [user_couser.course.id for user_couser in user_courses]
        # 现在获取学过该用户的所有的课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]
        all_resources = CourseResourse.objects.filter(course=course)
        return render(request, 'course-paly.html', {
            'course': course,
            'course_resourse': all_resources,
            'relate_courses': relate_courses,
            'video':video,

        })