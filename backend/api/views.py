from django.http import JsonResponse
import json

def api_home(request):
    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except:
        pass


    data['headers'] = dict(request.headers)
    data['params'] = dict(request.GET)
    data['content_type'] = request.content_type
    return JsonResponse(data)