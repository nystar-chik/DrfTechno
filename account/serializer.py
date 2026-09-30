from rest_framework import serializers
from rest_framework.authentication import authenticate
from account.models import User, OTPCode

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validated_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует!')
        return value
    
class VarifyOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=6)
    phone = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']

        otp = OTPCode.objects.filter(email = email, code = code).first()

        if not otp:
            raise serializers.ValidationError({'message':'Такой код не найден'})
        
        if otp.is_expired():
            otp.delete()

            raise serializers.ValidationError({'message' : 'Срок истек'})
        
        attrs['otp'] = attrs

        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class VerifyCodePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs['email']
        code =  attrs['code']

        otp = OTPCode.objects.filter(email=email, code=code).first()

        if not otp:
            raise serializers.ValidationError({'message':'Такой код не найден'})
        
        if otp.is_expired():
            otp.delete()
            raise serializers.ValidationError({'message' : 'Срок истек'})
        
        attrs['otp'] = otp

        return attrs
    
{
"email":"abdykarovsyimyk001@gmail.com",
"code":"404798",
"new_password":"123456789"
}
            

class LoginSerilaizer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):

        user = authenticate(
            username = attrs['username'],
            password = attrs['password']
        )

        if user is None:
            raise serializers.ValidationError('Invalid username or password')
        
        attrs['user'] = user

        return attrs    
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class DateUserSerializer(serializers.Serializer):
    username = serializers.CharField()        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar', 'phone', 'email', 'last_name', 'first_name']
        





