from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('admin:login'))
def charts_view(request):
    return render(request, 'food/charts.html')
