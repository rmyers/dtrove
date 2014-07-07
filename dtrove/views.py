
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def cluster(request):
    return render(request, 'cluster.html')


def details(request, cluster_id):
    return render(request, 'cluster_details.html')
