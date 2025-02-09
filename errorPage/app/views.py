from django.shortcuts import render

from django.http import *

from .models import ErrorLog

import requests
from django.conf import settings



GOOGLE_API_KEY = getattr(settings, "GOOGLE_API_KEY", "")
SEARCH_ENGINE_ID = getattr(settings, "SEARCH_ENGINE_ID", "")

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID
    }
    response = requests.get(url, params=params)
    return response.json()


def search_view(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        data = google_search(query)
        results = data.get("items", [])

    return render(request, "buscador.html", {"results": results, "query": query})





def index(request):
    return render(request,'index.html',status=200)

def error404(request,exception):
    return render(request,'404.html',status=404)

def error500(request,exception):
    return render(request, '500.html',status=500)

def error(request):
    return 7/0

def error_logs(request):
    return render(request,'error_logs.html')

def get_error_logs(request):
    errors = ErrorLog.objects.values('id','codigo','mensaje','fecha')
    return JsonResponse({'data': list(errors)})




# Create your views here.
