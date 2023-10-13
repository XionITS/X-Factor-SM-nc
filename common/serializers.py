from rest_framework import serializers
from .models import *

class NcdbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xfactor_ncdb
        fields = '__all__'

class CommonSerializer(serializers.ModelSerializer):  #user 정보
    ncdb_data = serializers.SerializerMethodField()

    class Meta:
        model = Xfactor_Common
        fields = '__all__'

    def get_ncdb_data(self, obj):
        try:
            # logged_name과 관련된 Xfactor_ncdb 인스턴스를 검색
            ncdb_instance = Xfactor_ncdb.objects.get(userId=obj.logged_name)
            # Xfactor_ncdbSerializer를 사용하여 관련 인스턴스를 직렬화
            ncdb_serializer = NcdbSerializer(ncdb_instance)
            return ncdb_serializer.data
        except Xfactor_ncdb.DoesNotExist:
            # 일치하는 데이터가 없을 경우 빈 값을 반환
            return {}

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


class XfactorDailyserializer(serializers.ModelSerializer):

    class Meta:
        model = Xfactor_Daily
        fields = '__all__'


class XfactorLogserializer(serializers.ModelSerializer):

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


