from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):  #user 정보
    class Meta:
        #추후에 history부분 제거
        model = XFactor_User
        fields = '__all__'

class UserHistorySerializer(serializers.ModelSerializer):  #user 정보
    class Meta:
        #추후에 history랑 nano랑만 합쳐서 할수있게
        model = XFactor_User
        fields = '__all__'

class NanoSerializer(serializers.ModelSerializer):
    # 추후엔 user가 히스토리 위주로 가져올수있게
    # xfactor_user = UserHistorySerializer()
    xfactor_user = UserSerializer()
    class Meta:
        #추후엔 히
        model = XFactor_Nano
        fileds = '__all__'

class XUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = XFactor_XUser
        fileds = '__all__'

class AuthSerializer(serializers.ModelSerializer): #auth 정보
    class Meta:
        model = XFactor_Auth
        fields = '__all__'

class UserAuthSerializer(serializers.ModelSerializer): #User별 auth정보
    xfactor_auth = AuthSerializer()
    class Meta:
        model = XFactor_XUserAuth
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer): #User별 auth정보
    class Meta:
        model = Daily_Statistics
        fields = '__all__'


from rest_framework import serializers

class LimitedUserSerializer(serializers.ModelSerializer):
    sw_list = serializers.SerializerMethodField()

    class Meta:
        model = XFactor_User
        fields = ('chasisstype', 'computer_name', 'ip_address', 'sw_list', 'memo')

    def get_sw_list(self, obj):
        sw_list_items = obj.sw_list.split('<br>')
        limited_sw_list = '<br>'.join(sw_list_items[:4])
        return limited_sw_list
