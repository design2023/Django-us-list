from rest_framework import serializers
from us_list.models import User
from us_list.models import ExcelFile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ('account_id','account_name','file', 'uploaded_at')        