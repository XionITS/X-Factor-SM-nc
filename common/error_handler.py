from django.shortcuts import render


def bad_request(request, exception):
    print('400')
    return render(request, 'error_400.html', status=400)


def not_found(request, exception):
    print('404')
    return render(request, 'error_404.html', status=404)


def server_error(request):
    print('500')
    return render(request, 'error_500.html', status=500)
