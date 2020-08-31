from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from apps.food import models


@login_required(login_url=reverse_lazy('admin:login'))
def charts_view(request):
    context = {
        'data': models.EatingAction.get_by_date()
    }
    print(context)
    return render(request, 'food/charts.html', context=context)
