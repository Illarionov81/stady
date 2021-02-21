from django.http import Http404, HttpResponseNotFound


class RestrictIds:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # '''Тут обработка входящего реквеста - можно добавить данные в сам реквест
        # (request.samthing = samthing) или выкинуть ошибку например. '''
        parts = request.path.split('/')
        pk = None
        for part in parts:
            try:
                pk = int(part)
            except ValueError:
                pass
            if pk in range(1, 101):
                # raise Http404
                return HttpResponseNotFound('Обьекты с  id от 1 до 100 недоступны для просмотра')
        response = self.get_response(request)
        # Тут можно обработать выходящий реквест
        return response


class TypeOfResponse:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Тут можно обработать выходящий реквест
        to_text = request.GET.get('to_text')
        # если в строке запроса будет параметр
        # to_text=1 то вывод будет в формате текст
        if to_text:
            response['Content-Type'] = 'text/plain; charset=UTF-8'
        return response
