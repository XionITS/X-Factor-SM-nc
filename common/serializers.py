from rest_framework import serializers
from .models import *


class CommonSerializer(serializers.ModelSerializer):  #user 정보
    class Meta:
        #추후에 history부분 제거
        model = Xfactor_Common
        fields = '__all__'

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
        fileds = '__all__'

class XuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_Xuser
        fileds = '__all__'

class AuthSerializer(serializers.ModelSerializer): #auth 정보
    class Meta:
        model = Xfactor_Auth
        fields = '__all__'

class XuserAuthSerializer(serializers.ModelSerializer): #User별 auth정보
    xfactor_auth = AuthSerializer()
    class Meta:
        model = Xfactor_Xuser_Auth
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

class XfactorServiceserializer(serializers.ModelSerializer):
    computer = CommonSerializer()

    class Meta:
        model = Xfactor_Service
        fields = '__all__'