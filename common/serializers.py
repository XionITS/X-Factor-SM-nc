from rest_framework import serializers
from .models import XFactor_User, XFactor_Auth, XFactor_UserAuth, XFactor_Nano


class UserSerializer(serializers.ModelSerializer):  #user 정보
    class Meta:
        model = XFactor_User
        fields = '__all__'

class NanoSerializer(serializers.ModelSerializer):
    xfactor_user = UserSerializer()
    class Meta:
        model = XFactor_Nano
        fileds = '__all__'

class AuthSerializer(serializers.ModelSerializer): #auth 정보
    class Meta:
        model = XFactor_Auth
        fields = '__all__'

class UserAuthSerializer(serializers.ModelSerializer): #User별 auth정보
    xfactor_auth = AuthSerializer()
    class Meta:
        model = XFactor_UserAuth
        fields = '__all__'
