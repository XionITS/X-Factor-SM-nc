from django.db import models

# Create your models here.
class XFactor_User(models.Model):
    computer_id = models.CharField(max_length=150, primary_key=True)
    computer_name = models.CharField(max_length=150)
    user_name = models.CharField(max_length=50, null=True)
    user_email = models.CharField(max_length=150, null=True)
    user_dep = models.CharField(max_length=50, null=True)
    ip_address = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=50)
    chasisstype = models.CharField(max_length=50)
    domain_id = models.CharField(max_length=150, null=True)
    open_id = models.CharField(max_length=150, null=True)
    os_simple = models.CharField(max_length=50)
    os_total = models.CharField(max_length=150)
    os_version = models.CharField(max_length=150)
    os_build = models.CharField(max_length=150)
    hw_list = models.TextField()
    sw_list = models.TextField()
    hotfix = models.CharField(max_length=150, null=True)
    hotfix_date = models.DateTimeField(null=True)
    memo = models.TextField(null=True)
    user_date = models.DateTimeField(auto_now=True)

class XFactor_Nano(models.Model):
    user_name = models.CharField(max_length=50, null=True)
    user_email = models.CharField(max_length=150, null=True)
    user_dep = models.CharField(max_length=50, null=True)
    domain_id = models.CharField(max_length=150, null=True)
    open_id = models.CharField(max_length=150, null=True)
    memo = models.TextField(null=True)
    xfactor_user = models.ForeignKey(XFactor_User, on_delete=models.CASCADE)


class XFactor_Auth(models.Model):
    auth_id = models.CharField(max_length=150, primary_key=True)
    auth_name = models.CharField(max_length=150)
    auth_url = models.CharField(max_length=150)
    auth_num = models.IntegerField()

class XFactor_UserAuth(models.Model):
    computer_id = models.CharField(max_length=150)
    auth_id = models.CharField(max_length=150)
    auth_use = models.CharField(max_length=150)
    xfactor_user = models.ForeignKey(XFactor_User, on_delete=models.CASCADE, related_name='user')
    xfactor_auth = models.ForeignKey(XFactor_Auth, on_delete=models.CASCADE, related_name='auth')

class XFactor_Group(models.Model):
    group_id = models.CharField(max_length=150, primary_key=True)
    group_name = models.CharField(max_length=150)
    group_note = models.TextField(null=True)

class XFactor_GroupUser(models.Model):
    computer_id = models.CharField(max_length=150)
    group_id = models.CharField(max_length=150)
    xfactor_user = models.ForeignKey(XFactor_User, on_delete=models.CASCADE)
    xfactor_group = models.ForeignKey(XFactor_Group, on_delete=models.CASCADE)

class XFactor_Deploy(models.Model):
    deploy_id = models.CharField(max_length=150, primary_key=True)
    group_id = models.CharField(max_length=150)
    deploy_name = models.CharField(max_length=150)
    xfactor_group = models.ForeignKey(XFactor_Group, on_delete=models.CASCADE)

class XFactor_Log(models.Model):
    log_num = models.IntegerField(primary_key=True)
    log_func = models.CharField(max_length=150)
    log_item = models.CharField(max_length=150)
    log_result = models.CharField(max_length=150)
    log_user = models.CharField(max_length=100)
    log_time = models.DateTimeField()

class XFactor_Program(models.Model):
    program_id = models.CharField(max_length=150, primary_key=True)
    program_name = models.CharField(max_length=150)

class XFactor_ProgramUser(models.Model):
    computer_id = models.CharField(max_length=150)
    program_id = models.CharField(max_length=150)
    program_installed = models.CharField(max_length=150)
    xfactor_user = models.ForeignKey(XFactor_User, on_delete=models.CASCADE)
    xfactor_program = models.ForeignKey(XFactor_Program, on_delete=models.CASCADE)


class Daily_Statistics(models.Model):
    daily_statistics_num = models.IntegerField(primary_key=True)
    classification = models.CharField(max_length=100)
    item = models.TextField()
    item_count = models.CharField(max_length=100)
    statistics_collection_date = models.DateTimeField()