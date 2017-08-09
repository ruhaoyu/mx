# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgView(View):
    def get(self, request):
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
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, 'org_list.html', {
                 'all_org': orgs,
                'all_citys': all_citys,
                'org_nums': org_nums,
                'city_id': city_id,
                'category': category,
                'hot_orgs': hot_orgs,
                'sort': sort,
                })
