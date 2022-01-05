from .models import *
import xadmin
from organization.models import CourseOrg

#实现一个表的详情页中关联多个表同时修改
class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResourse
    extra = 0


class CourseAdmin(object):
    list_display = ["name", "desc","detail", "degree", "learn_times", "students", "fav_nums", "click_num",'course_org', "add_time",'category','get_zj_nums','go_to']
    search_field = ["name", "desc", "detail","degree", "learn_times", "students", "fav_nums", "image", "click_num",'course_org','category']
    list_filter = ["name", "desc", "detail","degree", "learn_times", "students", "fav_nums", "image", "click_num", 'course_org',"add_time",'category']
    #设置后台字段的排序:
    ordering = ['-click_num']
    #定义列表页中允许修改的字段
    list_editable = ["name", "desc","detail"]
    #定义设置详情页为只读字段
    readonly_fields = ["name", "desc","students"]
    #exclude(排除)定义设置详情页不做显示注:不能和readonly_fields设置冲突
    exclude = ["image"]
    inlines = [LessonInline,CourseResourceInline]
    #设置自动刷新页面的时间以秒为单位
    refresh_times = [3,5]

    import_excel=True
    #在做保存时候增加我们的逻辑
    def save_models(self):
        #在保存课程机构的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            # course_org.course_num = 4
            course_org.save()

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin.self).post(request,args,kwargs)

class BannerCourseAdmin(object):
    list_display = ["name", "desc","detail", "degree", "learn_times", "students", "fav_nums", "click_num",'course_org', "add_time",'category']
    search_field = ["name", "desc", "detail","degree", "learn_times", "students", "fav_nums", "image", "click_num",'course_org','category']
    list_filter = ["name", "desc", "detail","degree", "learn_times", "students", "fav_nums", "image", "click_num", 'course_org',"add_time",'category']
    #设置后台字段的排序:
    ordering = ['-click_num']
    #定义列表页中允许修改的字段
    list_editable = ["name", "desc","detail"]
    #定义设置详情页为只读字段
    readonly_fields = ["name", "desc","detail","students"]
    #exclude(排除)定义设置详情页不做显示注:不能和readonly_fields设置冲突
    exclude = ["image"]
    inlines = [LessonInline,CourseResourceInline]
    #过滤指定的字段
    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_filed = ["course", "name"]
    list_filter = ["course", "name", "add_time"]


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    search_filed = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time"]


class CourseResourseAdmin(object):
    list_display = ["course", "name", "add_time", "download"]
    search_filed = ["course", "name", "add_time", "download"]
    list_filter = ["course", "name", "add_time", "download"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)
#关联注册:
xadmin.site.register(BannerCourse,BannerCourseAdmin)