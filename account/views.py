from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def view(request):
    return render(request, template_name='account/view.html')
