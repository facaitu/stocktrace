from django.shortcuts import render


# Create your views here.
def sw(request):
    return render(request, 'sw.html')


def history(request):
    code = request.GET.get('code') or 'SH600029'
    return render(request, 'stock_history.html', {'code': code})


def diff(request):
    code = request.GET.get('code') or 'SH600029,SH601111'
    return render(request, 'stock_diff.html', {'code': code})


def sh(request):
    return render(request, 'sh.html')


def cix(request):
    return render(request, 'cix.html')
