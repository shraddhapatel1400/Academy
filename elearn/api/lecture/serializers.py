from rest_framework import serializers

from .models import Lecture

class LectureSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super(LectureSerializer, self).to_representation(instance)
        rep['course'] = instance.course.id
        rep['created_at'] = instance.created_at.strftime("%d-%b-%Y %H:%M:%S")
        return rep

    class Meta:
        model = Lecture
        video = serializers.FileField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
        fields = ('id','title','course','video','created_at')
