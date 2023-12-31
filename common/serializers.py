import re

import pytz
from dateutil import parser
from django.db.models import Max
from rest_framework import serializers
from .models import *
from datetime import datetime, timedelta
from django.utils.html import escape, strip_tags


class NcdbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_ncdb
        fields = '__all__'

# class CommonSerializer(serializers.ModelSerializer):  #user 정보
#     ncdb_data = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Xfactor_Common
#         fields = '__all__'
#
#     def get_ncdb_data(self, obj):
#         try:
#             # logged_name과 관련된 Xfactor_ncdb 인스턴스를 검색
#             ncdb_instance = Xfactor_ncdb.objects.get(userId=obj.logged_name)
#             # Xfactor_ncdbSerializer를 사용하여 관련 인스턴스를 직렬화
#             ncdb_serializer = NcdbSerializer(ncdb_instance)
#             return ncdb_serializer.data
#         except Xfactor_ncdb.DoesNotExist:
#             # 일치하는 데이터가 없을 경우 빈 값을 반환
#             return {}


class CommonSerializer(serializers.ModelSerializer):  #user 정보
    user_date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Xfactor_Common
        fields = '__all__'
    def to_representation(self, instance):
        if instance.logged_name_id:
            # If `logged_name_id` is not None, serialize `Xfactor_ncdb` using `NcdbSerializer`
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data = super().to_representation(instance)
            data['ncdb_data'] = ncdb_data.data
        else:
            # If `logged_name_id` is None, just use `CommonSerializer`
            data = super().to_representation(instance)

        return data



class CommonHistorySerializer(serializers.ModelSerializer):  #user 정보
    class Meta:
        #추후에 history랑 nano랑만 합쳐서 할수있게
        model = Xfactor_Common
        fields = '__all__'

class XfactorSecuritySerializer(serializers.ModelSerializer):
    computer = CommonSerializer()

    class Meta:
        model = Xfactor_Security
        fields = '__all__'

class NanoSerializer(serializers.ModelSerializer):
    # 추후엔 user가 히스토리 위주로 가져올수있게
    # xfactor_user = UserHistorySerializer()
    xfactor_common = CommonSerializer()
    class Meta:
        #추후엔 히
        model = Xfactor_Nano
        fields = '__all__'

class XuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Xuser
        fields = '__all__'

class AuthSerializer(serializers.ModelSerializer): #auth 정보
    class Meta:
        model = Xfactor_Auth
        fields = '__all__'

class XuserAuthSerializer(serializers.ModelSerializer): #User별 auth정보
    xfactor_auth = AuthSerializer()
    class Meta:
        model = Xfactor_Xuser_Auth
        fields = '__all__'

class XgroupAuthSerializer(serializers.ModelSerializer): #User별 auth정보
    xfactor_auth = AuthSerializer()
    class Meta:
        model = Xfactor_Xgroup_Auth
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer): #User별 auth정보
    class Meta:
        model = Daily_Statistics
        fields = '__all__'


from rest_framework import serializers

class LimitedCommonSerializer(serializers.ModelSerializer):
    sw_list = serializers.SerializerMethodField()

    class Meta:
        model = Xfactor_Common
        fields = ('chassistype', 'computer_name', 'ip_address', 'sw_list', 'memo')

    def get_sw_list(self, obj):
        sw_list_items = obj.sw_list.split('<br>')
        limited_sw_list = '<br>'.join(sw_list_items[:4])
        return limited_sw_list

class XfactorPurchaseSerializer(serializers.ModelSerializer):
    computer = CommonSerializer()

    class Meta:
        model = Xfactor_Purchase
        fields = ['computer', 'mem_use', 'disk_use', 'user_date']


class Dailyserializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Daily
        fields = '__all__'

    def to_representation(self, instance):
        if instance.logged_name_id:
            # If `logged_name_id` is not None, serialize `Xfactor_ncdb` using `NcdbSerializer`
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data = super().to_representation(instance)
            data['ncdb_data'] = ncdb_data.data
        else:
            # If `logged_name_id` is None, just use `CommonSerializer`
            data = super().to_representation(instance)
            data['ncdb_data'] = []

        return data

class Cacheserializer(serializers.ModelSerializer):
    cache_date = serializers.SerializerMethodField()
    class Meta:
        model = Xfactor_Common_Cache
        fields = '__all__'
    def get_cache_date(self, obj):
        if obj.cache_date > obj.user_date - timedelta(hours=1):
            return "Online"
        else:
            return "Offline"
    def to_representation(self, instance):
        if instance.logged_name_id:
            # If `logged_name_id` is not None, serialize `Xfactor_ncdb` using `NcdbSerializer`
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data = super().to_representation(instance)
            data['ncdb_data'] = ncdb_data.data
        else:
            # If `logged_name_id` is None, just use `CommonSerializer`
            data = super().to_representation(instance)
            data['ncdb_data'] = []

        return data


class Cacheserializer2(serializers.ModelSerializer):
    cache_date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Xfactor_Common_Cache
        fields = '__all__'
    def to_representation(self, instance):
        if instance.logged_name_id:
            # If `logged_name_id` is not None, serialize `Xfactor_ncdb` using `NcdbSerializer`
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data = super().to_representation(instance)
            data['ncdb_data'] = ncdb_data.data
        else:
            # If `logged_name_id` is None, just use `CommonSerializer`
            data = super().to_representation(instance)
            data['ncdb_data'] = []

        return data


class Cacheserializer3(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Common_Cache
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.logged_name_id:
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data['ncdb_data'] = ncdb_data.data
        else:
            data['ncdb_data'] = []
        if instance.hotfix_date:
            date_strings = instance.hotfix_date.split('<br>')
            # 공백을 제거하고 빈 문자열을 필터링
            date_strings = [date.strip() for date in date_strings if date.strip()]
            # 문자열을 datetime 객체로 변환
            date_objects = [datetime.strptime(date.split(' ')[0], '%m/%d/%Y') for date in date_strings]
            # datetime 객체 중에서 가장 최근 날짜 찾기
            latest_date = max(date_objects)
            latest_date_formatted = latest_date.strftime('%Y-%m-%d')
            data['hotfix_date'] = latest_date_formatted
        return data


class Commonserializer2(serializers.ModelSerializer):
    user_date = serializers.SerializerMethodField()
    class Meta:
        model = Xfactor_Common
        fields = '__all__'
    def get_user_date(self, obj):
        local_tz = pytz.timezone('Asia/Seoul')
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        now = utc_now.astimezone(local_tz)
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        if obj.user_date >= start_of_today:
            return "Online"
        else:
            return "Offline"
    def to_representation(self, instance):
        if instance.logged_name_id:
            # If `logged_name_id` is not None, serialize `Xfactor_ncdb` using `NcdbSerializer`
            ncdb_data = NcdbSerializer(instance.logged_name_id)
            data = super().to_representation(instance)
            data['ncdb_data'] = ncdb_data.data
        else:
            # If `logged_name_id` is None, just use `CommonSerializer`
            data = super().to_representation(instance)
            data['ncdb_data'] = []

        return data

# class Dailyserializer(serializers.ModelSerializer):
#     ncdb_data = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Xfactor_Daily
#         fields = '__all__'
#
#     def get_ncdb_data(self, obj):
#         try:
#             # logged_name과 관련된 Xfactor_ncdb 인스턴스를 검색
#             ncdb_instance = Xfactor_ncdb.objects.get(userId=obj.logged_name)
#             # Xfactor_ncdbSerializer를 사용하여 관련 인스턴스를 직렬화
#             ncdb_serializer = NcdbSerializer(ncdb_instance)
#             return ncdb_serializer.data
#         except Xfactor_ncdb.DoesNotExist:
#             # 일치하는 데이터가 없을 경우 빈 값을 반환
#             return {}

class Commonserializer_pur(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Common
        fields = '__all__'
    def to_representation(self, instance):
        if instance.first_network:
            date_strings = instance.first_network
            latest_date_formatted = date_strings.strftime('%Y-%m-%d')
            data = super().to_representation(instance)
            data['first_network'] = latest_date_formatted
            #print(data['hotfix_date'])
            return data
    def get_user_date(self, obj):
        local_tz = pytz.timezone('Asia/Seoul')
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        now = utc_now.astimezone(local_tz)
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        if obj.user_date >= start_of_today:
            return "Online"
        else:
            return "Offline"

class XfactorLogserializer(serializers.ModelSerializer):
    log_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Xfactor_Log
        fields = '__all__'

class XuserSerializer2(serializers.ModelSerializer):
    xfactor_xuser_auth = XuserAuthSerializer()

    class Meta:
        model = Xfactor_Xuser
        fields = '__all__'

class XgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Xuser_Group
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['xgroup_name'] = escape(representation.get('xgroup_name', ''))
    #     representation['xgroup_note'] = escape(representation.get('xgroup_note', ''))
    #     return representation
