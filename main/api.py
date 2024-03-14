from rest_framework import generics
from rest_framework.response import Response
from .Serializer import CategorySerializer, SubCourseSerializer, SubTopicSerializer, UserSelectedCourseSerializer,UserRegisterSerializer
from .models import Category, Sub_course, Sub_Topic, UserSelectedCourse
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadonly

def WholeCourse(request, pk):
    if pk is None:
        return JsonResponse({"status": "failed", "message": "Please provide the course id"})

    data = []
    course = generics.get_object_or_404(Category, id=pk)
    sub_courses = Sub_course.objects.filter(main=course)
    permission_classes = [IsAuthenticated]

    for sub_course in sub_courses:
        temp = {}
        temp["subCourseName"] = sub_course.topic_name
        temp["subCourseId"] = sub_course.id

        temp["subTopics"] = list(
            Sub_Topic.objects.filter(main=sub_course).values())
        data.append(temp)
    return JsonResponse(data, safe=False)


# class CategoryView(generics.RetrieveAPIView):
#     serializer_class = CategorySerializer

#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if pk is None:
#             # Get all categories
#             return Category.objects.all()
#         else:
#             category = Category.objects.get( id=pk)
#             return category  # Wrap the single object in a list for iteration

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return JsonResponse(serializer.data[0], safe=False)

class CategoryView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            return Category.objects.all()
        else:
            
            return generics.get_object_or_404(Category, id=pk)


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
    def post(self, request, *args, **kwargs):
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
            
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            data = serializer.errors

        return Response(data)
