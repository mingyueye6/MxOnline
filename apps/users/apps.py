from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    #将每个表改成中文
    verbose_name = "用户信息"
