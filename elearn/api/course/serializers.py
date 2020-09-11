from rest_framework import serializers

from .models import Course
from api.teacher.serializers import TeacherSerializer
from django.core.exceptions import ValidationError
from django.http.multipartparser import MultiPartParser, MultiPartParserError
import datetime


class CourseSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(CourseSerializer, self).to_representation(instance)
        rep['start_date'] = instance.start_date.strftime("%d-%b-%Y")
        rep['end_date'] = instance.end_date.strftime("%d-%b-%Y")
        return rep

    def create(self, validated_data):
        err = {}
        price = validated_data.pop('price',None)
        start = validated_data.pop('start_date',None)
        end = validated_data.pop('end_date',None)

        instance = self.Meta.model(**validated_data)
        
        if len(price) > 4 :
            err['price'] = ['Price can not be more than 4 digit long!!']
        else :
            instance.price = price

        today = datetime.date.today()
        if start > today :
            if start >= end :
                err['end_date'] = ['End date must be greater than start date!!']
            else :
                instance.end_date = end
            instance.start_date = start
        else :
            err['start_date'] = ['Start date must be greater than today!!']
            
        if len(err) > 0 :
            raise ValidationError(err)

        instance.save()
        return instance

    class Meta:
        model = Course
        image = serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
        fields = ('id','coursename','description','image','price','teacher','popular','start_date','end_date')
