from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField
from organization.models import *
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name="课程机构",null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name="课程名称")
    desc = models.CharField(max_length=300,verbose_name="课程描述")
    detail = models.TextField(verbose_name='课程详情')
    # Content = UEditorField(verbose_name='课程详情', width=600, height=300,imagePath="courses/ueditor/", filePath="courses/ueditor/",default='')
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',null=Teacher,blank=True)
    degree = models.CharField(choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2)
    learn_times = models.IntegerField(default=0,verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums= models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to='course/%Y/%m',verbose_name='封面',max_length=100,null=True)
    click_num = models.IntegerField(default=0,verbose_name="点击数")
    category = models.CharField(max_length=20,verbose_name="课程类别",default="后端开发")
    tag = models.CharField(default='',verbose_name="课程标签",max_length=10)
    youneed_know = models.CharField(max_length=300,default='',verbose_name='课程描述')
    teacher_tell = models.CharField(max_length=300,default='',verbose_name='老师告诉你')
    is_banner = models.BooleanField(default=False,verbose_name='是否轮播')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name
    #获取章节数
    def get_zj_nums(self):
        return  self.lesson_set.all().count()
    #修改此方法在后台的显示名称:
    get_zj_nums.short_description = '章节数'

    #允许写html代码的
    def go_to(self):
        #调用一个函数不然会以文本的格式形式而不是HTML代码显示
        from django.utils.safestring import  mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')
    go_to.short_description = '调转'
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]
    #获取课程所有章节
    def get_course_lession(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name

#定义一个model注册两个管理器
class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        #一定将proxy设置为True否则会自动在生成一张表
        proxy = True

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name
    #获取章节视频
    def get_lessoon_video(self):
        return self.video_set.all()
    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    url = models.CharField(max_length=200,verbose_name='访问地址',default='')
    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResourse(models.Model):
    course = models.ForeignKey(Course,verbose_name="课程名称")
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name="资源文件",max_length=100)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
