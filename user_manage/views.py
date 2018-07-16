from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json



@login_required
def chpasswd(request):
    path = request.path.split('/')[1]
    return render(request, 'user_manage/chpasswd.html', {'user':'%s%s' % (request.user.last_name,request.user.first_name),
                                                         'path1':'user_manage',
                                                         'path2':path,
                                                         'page_name1':u'用户管理',
                                                         'page_name2':u'修改密码',})

@login_required
def post_chpasswd(request):
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    user = User.objects.get(username=request.user.username)
    if not user.check_password(password_current):
        code = 1
        msg = u'当前密码错误'
    elif password_new == '' or password_new_again == '':
        code = 2
        msg = u'新密码不能为空'
    elif not password_new == password_new_again:
        code = 3
        msg = u'新密码不一致'
    else:
        try:
            user.set_password(password_new)
            user.save()
            code = 0
            msg = u'密码修改成功'
        except Exception:
            code = 4
            msg = u'密码修改失败'
    return HttpResponse(json.dumps({'code':code,'msg':msg}),content_type="application/json")
