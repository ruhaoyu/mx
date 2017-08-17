# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CourseOrg, CityDict
from operation.models import UserFavorate
from users.models import UserProfile
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class OrgView(View):
    def get(self, request):
        current = 'org_list'
        # 课程机构
        all_orgs = CourseOrg.objects.all()
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
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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
            return HttpResponse('{"status":"fail", "msg":"收藏"}')
        else:
            if fav_type > 0 and fav_id > 0:
                user_fav = UserFavorate()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}')

