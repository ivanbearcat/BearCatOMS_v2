from django.http import HttpResponse
import json

def web_hook_api(request):
    data = json.loads(request.body)
    from pprint import pprint
    pprint(data)
    return HttpResponse(json.dumps({'code': 0, 'msg': 'success'}), content_type='application/json;charset = utf-8')