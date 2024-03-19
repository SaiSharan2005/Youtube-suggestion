from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from .Serializer import CategorySerializer, SubCourseSerializer, SubTopicSerializer, UserSelectedCourseSerializer,UserRegisterSerializer
from .models import Category, Sub_course, Sub_Topic, UserSelectedCourse
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadonly
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
def WholeCourse(request, pk):
    if pk is None:
        return JsonResponse({"status": "failed", "message": "Please provide the course id"})

    data = []
    course = generics.get_object_or_404(Category, id=pk)
    sub_courses = Sub_course.objects.filter(main=course)
    # permission_classes = (IsAuthenticated,) 

    # authentication_classes = (TokenAuthentication,) 

    for sub_course in sub_courses:
        temp = {}
        temp["subCourseName"] = sub_course.topic_name
        temp["subCourseId"] = sub_course.id

        temp["subTopics"] = list(
            Sub_Topic.objects.filter(main=sub_course).values())
        data.append(temp)
    return JsonResponse(data, safe=False)




class CategoryView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,) 



    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk is not None:
            return get_object_or_404(Category, id=pk)
        else:
            # You can raise a 404 here if no pk is provided
            raise Http404("No pk provided for Category")

class AllCategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        return Category.objects.all()

class SubCourse(generics.ListAPIView):
    serializer_class = SubCourseSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            # Get all subcourses
            return Sub_course.objects.all()
        else:
            # Get subcourses for a specific category by ID
            category = generics.get_object_or_404(Category, id=pk)
            return Sub_course.objects.filter(main=category)


class SubTopic(generics.RetrieveAPIView):
    serializer_class = SubTopicSerializer
    queryset = Sub_Topic.objects.all()

    # The get_object method is automatically handling the retrieval based on the URL parameter
    def get_object(self):
        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(Sub_Topic, id=pk)



# class UserSelectedCourseController(generics.ListAPIView):
#     serializer_class = UserSelectedCourseSerializer

#     def get(request):

class LogoutUserView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        


        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email
            print("damed   ",account.username,account.password)
            user = authenticate(username=account.username, password=request.data["password"])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Your authentication logic here
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class GetUserData(APIView):

    def get(self, request):
        try:
            # token = Token.objects.get(key=request.user.auth_token)
            user = request.user  # Get the user associated with the token

            # Extract user information
            user_data = {
                'username': user.username,
                # 'email': user.email,
                'id':user.id
            }
            return JsonResponse(user_data)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token is not valid'}, status=400)

