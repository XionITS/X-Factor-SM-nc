from django.db import models, transaction
#
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


class Xfactor_ncdb(models.Model):
    companyCode = models.CharField(max_length=100, null=True)
    userName = models.CharField(max_length=100, null=True)
    userNameEn = models.CharField(max_length=100, null=True)
    userId = models.CharField(primary_key=True, max_length=100)
    email = models.CharField(max_length=100, null=True)
    empNo = models.CharField(max_length=100, null=True)
    joinDate = models.CharField(max_length=100, null=True)
    retireDate = models.CharField(max_length=100, null=True)
    deptCode = models.CharField(max_length=100, null=True)
    deptName = models.CharField(max_length=100, null=True)
    managerUserName = models.CharField(max_length=100, null=True)
    managerUserId = models.CharField(max_length=100, null=True)
    managerEmpNo = models.CharField(max_length=100, null=True)

class Xfactor_Common(models.Model):
    computer_id = models.CharField(max_length=100, primary_key=True)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.TextField(null=True)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100, null=True)
    essential2 = models.CharField(max_length=100, null=True)
    essential3 = models.CharField(max_length=100, null=True)
    essential4 = models.CharField(max_length=100, null=True)
    essential5 = models.CharField(max_length=100, null=True)
    mem_use = models.CharField(max_length=100, null=True)
    disk_use = models.CharField(max_length=100, null=True)
    t_cpu = models.CharField(max_length=100, null=True)
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True)
    user_date = models.DateTimeField(auto_now_add=True)

class Xfactor_Daily(models.Model):
    computer_id = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.CharField(max_length=100)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100)
    essential2 = models.CharField(max_length=100)
    essential3 = models.CharField(max_length=100)
    essential4 = models.CharField(max_length=100)
    essential5 = models.CharField(max_length=100)
    mem_use = models.CharField(max_length=100)
    disk_use = models.CharField(max_length=100)
    t_cpu = models.CharField(max_length=100)
    security1 = models.CharField(max_length=100)
    security2 = models.CharField(max_length=100)
    security3 = models.CharField(max_length=100)
    security4 = models.CharField(max_length=100)
    security5 = models.CharField(max_length=100)
    security1_ver = models.CharField(max_length=100)
    security2_ver = models.CharField(max_length=100)
    security3_ver = models.CharField(max_length=100)
    security4_ver = models.CharField(max_length=100)
    security5_ver = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    multi_boot = models.CharField(max_length=100)
    ext_chr = models.TextField()
    ext_chr_ver = models.TextField()
    ext_edg = models.TextField()
    ext_edg_ver = models.TextField()
    ext_fir = models.TextField()
    ext_fir_ver = models.TextField()
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True)
    user_date = models.DateTimeField()


class Xfactor_Purchase(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    mem_use = models.TextField()
    disk_use = models.TextField()
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Security(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    security1 = models.CharField(max_length=100)
    security2 = models.CharField(max_length=100)
    security3 = models.CharField(max_length=100)
    security4 = models.CharField(max_length=100)
    security5 = models.CharField(max_length=100)
    security1_ver = models.CharField(max_length=100)
    security2_ver = models.CharField(max_length=100)
    security3_ver = models.CharField(max_length=100)
    security4_ver = models.CharField(max_length=100)
    security5_ver = models.CharField(max_length=100)
    uuid = models.CharField(max_length=500)
    multi_boot = models.TextField()
    first_network = models.TextField()
    last_boot = models.TextField()
    ext_chr = models.TextField()
    ext_chr_ver = models.TextField()
    ext_edg = models.TextField()
    ext_edg_ver = models.TextField()
    ext_fir = models.TextField()
    ext_fir_ver = models.TextField()
    user_date = models.DateTimeField(auto_now_add=True)



class Xfactor_Nano(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50, null=True)
    user_email = models.EmailField(null=True)
    user_dep = models.CharField(max_length=50, null=True)
    domain_id = models.CharField(max_length=50, null=True)
    open_id = models.CharField(max_length=50, null=True)
    xfactor_id = models.CharField(max_length=50, null=True)
    depno = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=100, null=True)

class Xfactor_Xuser(models.Model):
    x_id = models.CharField(max_length=500, primary_key=True)
    x_pw = models.CharField(max_length=500, null=True)
    x_name = models.CharField(max_length=50, null=True)
    x_email = models.CharField(max_length=500, null=True)
    x_auth = models.CharField(max_length=500, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

class Xfactor_Xuser_Group(models.Model):
    xgroup_name = models.CharField(max_length=500)
    xgroup_note = models.TextField(null=True)
    xuser_id_list = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

class Xfactor_Auth(models.Model):
    auth_id = models.CharField(max_length=500, primary_key=True)
    auth_name = models.CharField(max_length=500)
    auth_url = models.CharField(max_length=500)
    auth_num = models.IntegerField()


class Xfactor_Xuser_Auth(models.Model):
    auth_use = models.CharField(max_length=500)
    xfactor_xuser = models.ForeignKey(Xfactor_Xuser, on_delete=models.CASCADE, related_name='xuser', to_field='x_id')
    xfactor_auth = models.ForeignKey(Xfactor_Auth, on_delete=models.CASCADE, related_name='auth', to_field='auth_id')

class Xfactor_Xgroup_Auth(models.Model):
    auth_use = models.CharField(max_length=500)
    xfactor_xgroup = models.TextField(null=True)
    xgroup = models.ForeignKey(Xfactor_Xuser_Group, on_delete=models.CASCADE, related_name='xgroup', to_field='id')
    xfactor_auth = models.ForeignKey(Xfactor_Auth, on_delete=models.CASCADE, related_name='group_auth', to_field='auth_id')


class Daily_Statistics(models.Model):
    daily_statistics_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    statistics_collection_date = models.DateTimeField(auto_now=True)


class Daily_Statistics_log(models.Model):
    daily_statistics_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    statistics_collection_date = models.DateTimeField(auto_now=True)


class Xfactor_Group(models.Model):
    group_id = models.CharField(max_length=500, primary_key=True)
    group_name = models.CharField(max_length=500)
    group_note = models.TextField(null=True)
    computer_id_list = models.TextField(null=True)
    computer_name_list = models.TextField(null=True)


class Xfactor_Deploy(models.Model):
    deploy_id = models.CharField(max_length=500, primary_key=True)
    group_id = models.ForeignKey(Xfactor_Group, on_delete=models.CASCADE)
    deploy_name = models.CharField(max_length=500)


class Xfactor_Report(models.Model):
    report_num = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    classification = models.CharField(max_length=500)
    item = models.TextField()
    item_count = models.IntegerField()
    report_collection_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Log(models.Model):
    log_func = models.CharField(max_length=100)
    log_item = models.CharField(max_length=100)
    log_result = models.CharField(max_length=100)
    log_user = models.CharField(max_length=100)
    log_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Common_Cache(models.Model):
    computer_id = models.CharField(max_length=100)
    computer_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    chassistype = models.CharField(max_length=100)
    os_simple = models.CharField(max_length=100)
    os_total = models.CharField(max_length=100)
    os_version = models.CharField(max_length=500)
    os_build = models.CharField(max_length=500)
    hw_cpu = models.CharField(max_length=500)
    hw_ram = models.CharField(max_length=500)
    hw_mb = models.CharField(max_length=500)
    hw_disk = models.CharField(max_length=500)
    hw_gpu = models.CharField(max_length=500)
    sw_list = models.TextField()
    sw_ver_list = models.TextField()
    sw_install = models.TextField(null=True)
    sw_lastrun = models.TextField(null=True)
    first_network = models.TextField(null=True)
    last_network = models.TextField(null=True)
    hotfix = models.TextField(null=True)
    hotfix_date = models.TextField(null=True)
    subnet = models.TextField(null=True)
    memo = models.TextField(null=True)
    essential1 = models.CharField(max_length=100, null=True)
    essential2 = models.CharField(max_length=100, null=True)
    essential3 = models.CharField(max_length=100, null=True)
    essential4 = models.CharField(max_length=100, null=True)
    essential5 = models.CharField(max_length=100, null=True)
    mem_use = models.CharField(max_length=100, null=True)
    disk_use = models.CharField(max_length=100, null=True)
    t_cpu = models.CharField(max_length=100, null=True)
    logged_name_id = models.ForeignKey(Xfactor_ncdb, on_delete=models.SET_NULL, null=True)
    cache_date = models.DateTimeField(null=True)
    user_date = models.DateTimeField(auto_now_add=True)


# @receiver(pre_save, sender=Xfactor_Common)
# def copy_to_cache(sender, instance: Xfactor_Common, **kwargs):
#     # Check if this is an update
#     try:
#         if instance.pk is not None:
#             # If the object has changed...
#             old_instance = Xfactor_Common.objects.get(pk=instance.pk)
#             user_date_before_update = old_instance.user_date
#             # ... create a new Xfactor_Common_Cache record.
#             Xfactor_Common_Cache.objects.create(
#                 computer_id=instance.computer_id,
#                 computer_name=instance.computer_name,
#                 ip_address=instance.ip_address,
#                 mac_address=instance.mac_address,
#                 chassistype=instance.chassistype,
#                 os_simple=instance.os_simple,
#                 os_total=instance.os_total,
#                 os_version=instance.os_version,
#                 os_build=instance.os_build,
#                 hw_cpu=instance.hw_cpu,
#                 hw_ram=instance.hw_ram,
#                 hw_mb=instance.hw_mb,
#                 hw_disk=instance.hw_disk,
#                 hw_gpu=instance.hw_gpu,
#                 sw_list=instance.sw_list,
#                 sw_ver_list=instance.sw_ver_list,
#                 sw_install=instance.sw_install,
#                 sw_lastrun=instance.sw_lastrun,
#                 first_network=instance.first_network,
#                 last_network=instance.last_network,
#                 hotfix=instance.hotfix,
#                 hotfix_date=instance.hotfix_date,
#                 subnet=instance.subnet,
#                 memo=instance.memo,
#                 essential1=instance.essential1,
#                 essential2=instance.essential2,
#                 essential3=instance.essential3,
#                 essential4=instance.essential4,
#                 essential5=instance.essential5,
#                 mem_use=instance.mem_use,
#                 disk_use=instance.disk_use,
#                 t_cpu=instance.t_cpu,
#                 logged_name=instance.logged_name,
#                 cache_date=user_date_before_update,
#                 user_date=timezone.now()
#             )
#     except Exception as e:
#         print(e)


# 트랜잭션 시작
# with transaction.atomic():
#     # Xfactor_Common의 모든 레코드 가져오기
#     xfactor_common_records = Xfactor_Common.objects.all()
#
#     # Xfactor_Common_Cache 업데이트
#     for record in xfactor_common_records:
#         Xfactor_Common_Cache.objects.create(
#             computer_id=record.computer_id,
#             computer_name=record.computer_name,
#             ip_address=record.ip_address,
#             mac_address=record.mac_address,
#             chassistype=record.chassistype,
#             os_simple=record.os_simple,
#             os_total=record.os_total,
#             os_version=record.os_version,
#             os_build=record.os_build,
#             hw_cpu=record.hw_cpu,
#             hw_ram=record.hw_ram,
#             hw_mb=record.hw_mb,
#             hw_disk=record.hw_disk,
#             hw_gpu=record.hw_gpu,
#             sw_list=record.sw_list,
#             sw_ver_list=record.sw_ver_list,
#             sw_install=record.sw_install,
#             sw_lastrun=record.sw_lastrun,
#             first_network=record.first_network,
#             last_network=record.last_network,
#             hotfix=record.hotfix,
#             hotfix_date=record.hotfix_date,
#             subnet=record.subnet,
#             memo=record.memo,
#             essential1=record.essential1,
#             essential2=record.essential2,
#             essential3=record.essential3,
#             essential4=record.essential4,
#             essential5=record.essential5,
#             mem_use=record.mem_use,
#             disk_use=record.disk_use,
#             t_cpu=record.t_cpu,
#             logged_name=record.logged_name,
#             cache_date=record.user_date,
#             user_date=timezone.now()
#             # 필요한 모든 필드 추가...
#         )
