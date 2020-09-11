from rest_framework import serializers

from .models import Enrollment

class EnrollSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(EnrollSerializer, self).to_representation(instance)
        rep['student'] = instance.student.id
        rep['course'] = instance.course.id
        rep['created_at'] = instance.created_at.strftime("%d-%b-%Y %H:%M:%S")
        return rep
    
    class Meta:
        model = Enrollment
        fields = ('id','student','course','transaction_id','total_amount','created_at')