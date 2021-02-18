from django.shortcuts import render

import json
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def json_echo_view(request, *args, **kwargs):
    answer = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'method': request.method,
    }
    answer_as_json = json.dumps(answer)
    response = HttpResponse(answer_as_json)
    response['Content-Type'] = 'application/json'
    return response
