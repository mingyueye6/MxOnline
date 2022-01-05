import xadmin

from .models import *


class CityDictAdmin(object):
    list_display = ["name", "desc", "add_time"]
    search_field = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]


class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    search_field = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city"]
    list_filter = ["name", "desc", "click_nums", "fav_nums", "image", "address", "city", "add_time"]
    #课程和课程结构是相关联的
    #设置在课程的后台详情页选择时完成可以搜索的功能:
    relfield_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums", "add_time"]
    search_field = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums"]
    list_filter = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums", "fav_nums", "add_time"]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)