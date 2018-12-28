from django.contrib import admin
from courses.models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(BannerCourse)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(CourseRecourse)
