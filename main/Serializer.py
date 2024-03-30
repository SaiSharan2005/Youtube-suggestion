from rest_framework import serializers
from .models import Category,Sub_course,Sub_Topic,UserSelectedCourse,Documentation,DocumentationData
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"Error": "Password Does not match"})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error": "Email already exist"})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = "__all__"
        exclude  = ["duration"]
        
        
class SubCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sub_course
        fields = "__all__"

        
class SubTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sub_Topic
        fields = "__all__"

        
        
class UserSelectedCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSelectedCourse
        fields = "__all__"

        
class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Documentation
        fields = "__all__"

class DocumentationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=DocumentationData
        fields = "__all__"
