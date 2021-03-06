# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CourseOrg, CityDict, Teacher
from courses.models import Course
from operation.models import UserFavorate
from users.models import UserProfile
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


class OrgView(View):
    def get(self, request):
        current = 'org_list'
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 课程机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        # 热门机构，用于排序
        hot_orgs = CourseOrg.objects.order_by('click_nums')[:3].all()
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 所在城市
        all_citys = CityDict.objects.all()
        city_id = request.GET.get('city', '')
        # 城市筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 课程机构数量
        org_nums = all_orgs.count()
        # 学习人数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_num')
        # 课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org_list.html', {
                 'all_org': orgs,
                'all_citys': all_citys,
                'org_nums': org_nums,
                'city_id': city_id,
                'category': category,
                'hot_orgs': hot_orgs,
                'sort': sort,
                'current': current,
                })


class OrgHomeView(View):
    '''机构首页'''
    def get(self, request,org_id):
        current = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        user_fav = False
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                user_fav = True
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current': current,
            'user_fav': user_fav,
        })


class OrgCourseView(View):
    '''机构课程列表页'''
    def get(self, request,org_id):
        current = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        user_fav = False
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                user_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current': current,
            'user_fav': user_fav,
        })


class OrgDetailView(View):
    '''机构课程介绍'''
    def get(self, request,org_id):
        current = 'detail'
        course_org = CourseOrg.objects.get(id=int(org_id))
        user_fav = False
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                user_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current': current,
            'user_fav': user_fav,
        })


class OrgTeacherView(View):
    '''机构课程教师'''
    def get(self, request,org_id):
        current = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        user_fav = False
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                user_fav = True
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teacher': all_teacher,
            'current': current,
            'user_fav': user_fav,
        })


class AddFavView(View):
    '''用户收藏,以及取消收藏'''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}')
        exist_records = UserFavorate.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            # 如果收藏记录存在，则取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                course.save()
            if int(fav_type) == 2:
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_nums -= 1
                org.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                teacher.save()
            return HttpResponse('{"status":"fail", "msg":"收藏"}')
        else:
            if fav_type > 0 and fav_id > 0:
                user_fav = UserFavorate()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}')


class TeacherView(View):
    '''授课教师列表'''
    def get(self, request):
        current = 'teacher'
        teachers = Teacher.objects.all()
        teacher_nums = teachers.count()
        hot_teachers = Teacher.objects.order_by('fav_nums').all()[:5]
        # 课程机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            teachers = teachers.filter(Q(name__icontains=search_keywords) | Q(points__icontains=search_keywords))
        # 排列名次
        index = range(1, 6)
        dict_hot_teachers = zip(index, hot_teachers)
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                teachers = teachers.order_by('fav_nums')
            if sort == 'all':
                teachers = teachers

        # 授课教师分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'current': current,
            'teachers': teachers,
            'teacher_nums': teacher_nums,
            'dict_hot_teachers':dict_hot_teachers,
            'sort': sort,
        })


class TeacherViewDetail(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        hot_teachers = Teacher.objects.all().order_by('fav_nums')[:5]
        # 排列名次
        index = range(1, 6)
        # 名次和对应的数据组成字典
        dict_teacher = zip(index, hot_teachers)
        # 收藏状态在未登录状态下置为未收藏
        teacher_user_fav = False
        org_user_fav = False
        # 在登录情况下，判断是否已收藏
        if request.user.is_active:
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                teacher_user_fav = True
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                org_user_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'dict_teacher': dict_teacher,
            'teacher_user_fav': teacher_user_fav,
            'org_user_fav': org_user_fav,
        })




