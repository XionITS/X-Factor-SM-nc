from django.db import models
#


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
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Common_log(models.Model):
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
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Service(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    essential1 = models.CharField(max_length=100)
    essential2 = models.CharField(max_length=100)
    essential3 = models.CharField(max_length=100)
    essential4 = models.CharField(max_length=100)
    essential5 = models.CharField(max_length=100)
    subnet = models.CharField(max_length=100)
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Service_log(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    essential1 = models.CharField(max_length=100)
    essential2 = models.CharField(max_length=100)
    essential3 = models.CharField(max_length=100)
    essential4 = models.CharField(max_length=100)
    essential5 = models.CharField(max_length=100)
    subnet = models.CharField(max_length=100)
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Purchase(models.Model):
    computer = models.ForeignKey(Xfactor_Common, on_delete=models.CASCADE)
    mem_use = models.TextField()
    disk_use = models.TextField()
    user_date = models.DateTimeField(auto_now_add=True)


class Xfactor_Purchase_log(models.Model):
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


class Xfactor_Security_log(models.Model):
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
    x_pw = models.CharField(max_length=500)
    x_name = models.CharField(max_length=50)
    x_email = models.CharField(max_length=500, null=True)
    x_auth = models.CharField(max_length=500, null=True)


class Xfactor_Auth(models.Model):
    auth_id = models.CharField(max_length=500, primary_key=True)
    auth_name = models.CharField(max_length=500)
    auth_url = models.CharField(max_length=500)
    auth_num = models.IntegerField()


class Xfactor_Xuser_Auth(models.Model):
    auth_use = models.CharField(max_length=500)
    xfactor_xuser = models.ForeignKey(Xfactor_Xuser, on_delete=models.CASCADE, related_name='xuser', to_field='x_id')
    xfactor_auth = models.ForeignKey(Xfactor_Auth, on_delete=models.CASCADE, related_name='auth', to_field='auth_id')


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