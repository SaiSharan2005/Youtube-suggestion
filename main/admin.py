from django.contrib import admin
from .models import Category,Sub_course,UserSelectedCourse,Sub_Topic,DefaultTopic,Default_Subtopics,UserSelected_Sub,Documentation,DocumentationData

admin.site.register(Category)
admin.site.register(Sub_course)
admin.site.register(UserSelectedCourse)
admin.site.register(Sub_Topic)
admin.site.register(DefaultTopic)
admin.site.register(Default_Subtopics)
admin.site.register(UserSelected_Sub)
admin.site.register(Documentation)
admin.site.register(DocumentationData)
