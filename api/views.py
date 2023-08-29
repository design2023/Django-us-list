from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from us_list.models import User
from us_list.models import ExcelFile
from rest_framework import status
from .serializers import UserSerializer
from .serializers import ExcelFileSerializer
import pandas as pd
import os
import json
from datetime import datetime,timedelta, date

def matches_criteria(value, criteria):
    """Checks if the given value matches the criteria."""
    if criteria is None or value is None:  # Ensure neither is None before proceeding
        return False
    
    value_str = str(value)
    criteria_str = str(criteria)
    
    if(value_str == criteria_str or criteria_str.find(value_str) != -1):
          return True
      
     
    matchNum = 0
    lastIndex = -1
    
    value_array = [char for char in value_str]
    criteria_array = [char for char in criteria_str]
       
    for valueChar in value_array:

        for indexCriteria,criteriaChar in enumerate(criteria_array):
            if(valueChar == criteriaChar and (indexCriteria > lastIndex  or lastIndex == -1)):
                matchNum +=1
                lastIndex = indexCriteria
                break
        
        if(len(value_array) == matchNum):
            break        
    
    
    if((len(value_array) - matchNum) < 2 and matchNum != 0):
        return True
            
    return False
    
    


properties_to_check = ['category', 'nationality', 'family_arabic','family_english',
                       'fullname_arabic','fullname_english','birth_date','birth_place',
                       'nick_name','street','city','country','type','document_number',
                       'issuer','from_date','to_date'] 

# get the data 
@api_view(['POST'])
def getData(request):
    
    users = User.objects.all()
    checkedUsers =[]    
    for x in users:
        if any(matches_criteria(getattr(x, prop), request.data.get(prop)) for prop in properties_to_check):
                checkedUsers.append(x)
   
        
    serializer = UserSerializer(checkedUsers, many = True)
    return Response(serializer.data)

# get all the transactions 
@api_view(['POST'])
def getTransactions(request):
    transactions = ExcelFile.objects.all()  
    serializer = ExcelFileSerializer(transactions, many = True)
    return Response(serializer.data)



def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False   
     
def getdate(value):
    
    dateValue ='-'
    epoch = date(1970, 1, 1)
    if(value != '-' and  value != None):
        if is_number(value) and (len(str(value)) != 4):
            timestamp_in_seconds = int(value) / 1000
            
            if(int(value) < 0):
                days_to_subtract = abs(timestamp_in_seconds) / (60 * 60 * 24)
                dateValue = epoch - timedelta(days=days_to_subtract)
            else:
                dateValue = datetime.utcfromtimestamp(timestamp_in_seconds).strftime('%Y-%m-%d') 
            
                      
        else:
            dateValue = (value)
            if((len(str(value)) == 4)):
                dateValue = "01/01/"+str(value)
                
                
            date_obj = datetime.strptime(dateValue, "%d/%m/%Y")
            dateValue = date_obj.strftime("%Y-%m-%d")  
      
    return dateValue



# add a new user
@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    


@api_view(['POST'])
def postFile(request):
        
        file_serializer = ExcelFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            
            
            excel_file = file_serializer.instance.file.path  # get the path to the saved file
                
            # Determine the file extension and select the appropriate engine
            file_extension = os.path.splitext(excel_file)[1]
            if file_extension == '.xlsx':
                engine = 'openpyxl'
            elif file_extension == '.xls':
                engine = 'xlrd'
            else:
                response = {"message": "The file is not correct, please Insert the correct one"}      
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(excel_file, engine=engine)
            allData = df.to_json(orient='split')
            parsed_data = json.loads(allData)
            response =''
            if(len(parsed_data["columns"]) == 19):
                User.objects.all().delete()
                k = 0
                for i in range(2, len(parsed_data["data"])):
                    k +=1
                    data = parsed_data["data"][i]   
                    birthDate =  getdate(data[7])
                    fromDate =  getdate(str(data[16]).strip() if(len(str(data[16]))>10) else data[16])
                    toDate =  getdate(str(data[17]).strip() if(len(str(data[17]))>10) else data[17])
                    
                    
                    
                    newUser = {
                            "category": data[1],
                            "nationality": data[2],
                            "family_arabic": data[3],
                            "family_english": data[4],
                            "fullname_arabic": data[5],
                            "fullname_english": data[6],
                            "birth_date": birthDate if(birthDate !='-') else date(1900, 1, 1),
                            "birth_place": data[8],
                            "nick_name": data[9],
                            "street": data[10],
                            "city": data[11],
                            "country": data[12],
                            "type": data[13],
                            "document_number": data[14],
                            "issuer": data[15],
                            "from_date": fromDate.strip() if(fromDate !='-') else date(1900, 1, 1),
                            "to_date": toDate.strip() if(toDate !='-') else date(1900, 1, 1),
                            "other_information": data[18]
                        }
                    serializer = UserSerializer(data=newUser)

                    if serializer.is_valid():
                        serializer.save()
                
                
                   
                   
                response = {
                            "message": "Successfully Uploaded",
                            "data":df.to_json(orient='split')
                        }  
                print(k)
                return Response(response, status=status.HTTP_201_CREATED)
            else: 
                response = {"message": "The file is not correct, please Insert the correct one"}         
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)
