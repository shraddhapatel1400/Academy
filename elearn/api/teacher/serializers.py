from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes,permission_classes
from django.contrib.auth.password_validation import validate_password
from .models import Teacher
import django.contrib.auth.password_validation as validators

class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    
    def validate_password(self, data):
        validators.validate_password(password=data, user=Teacher)
        return data

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)

        enc_password = make_password(password)
        
        instance.password = enc_password
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.password(value)
            else:
                setattr(instance,attr,value)
        instance.save()
        return instance

    class Meta:
        model = Teacher
        fields = ('id','fullname','email','password','phone','institute','purpose')
