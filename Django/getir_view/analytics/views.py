from django.shortcuts import render

# Create your views here.
from .models import Siparis, SipPerCapita, SipDensityPerHood

def home(request):
    return render(request, 'home.html')


def sip_per_capita(request):
    qs = SipPerCapita.objects.all()
    district_name = request.GET.get('district_name')
    hood_name = request.GET.get('hood_name')
    population = request.GET.get('population')
    sip_count = request.GET.get('sip_count')
    sip_per_capita = request.GET.get('sip_per_capita')

    if district_name:
        qs = qs.filter(district_name__icontains=district_name)
    if hood_name:
        qs = qs.filter(hood_name__icontains=hood_name)
    if population:
        qs = qs.filter(population=population)
    if sip_count:
        qs = qs.filter(sip_count=sip_count)
    if sip_per_capita:
        qs = qs.filter(sip_per_capita=sip_per_capita)

    return render(request, 'sip_per_capita.html', {'data': qs})

def siparis_list(request):
    qs = Siparis.objects.all()

    # Get filter values from GET parameters
    order_id = request.GET.get('order_id')
    min_delivery_duration = request.GET.get('min_delivery_duration')
    max_delivery_duration = request.GET.get('max_delivery_duration')
    min_basket_value = request.GET.get('min_basket_value')
    max_basket_value = request.GET.get('max_basket_value')
    district_name = request.GET.get('district_name')
    hood_name = request.GET.get('hood_name')

    # Apply filters
    if order_id:
        qs = qs.filter(order_id=order_id)

    if min_delivery_duration and max_delivery_duration:
        qs = qs.filter(delivery_duration__gte=min_delivery_duration, delivery_duration__lte=max_delivery_duration)
    elif min_delivery_duration:
        qs = qs.filter(delivery_duration__gte=min_delivery_duration)
    elif max_delivery_duration:
        qs = qs.filter(delivery_duration__lte=max_delivery_duration)

    if min_basket_value and max_basket_value:
        qs = qs.filter(basket_value__gte=min_basket_value, basket_value__lte=max_basket_value)
    elif min_basket_value:
        qs = qs.filter(basket_value__gte=min_basket_value)
    elif max_basket_value:
        qs = qs.filter(basket_value__lte=max_basket_value)

    if district_name:
        qs = qs.filter(district_name__icontains=district_name)

    if hood_name:
        qs = qs.filter(hood_name__icontains=hood_name)
    
    return render(request, 'siparis_list.html', {'siparis_list': qs})
    

def sip_density_per_hood(request):
    qs = SipDensityPerHood.objects.all()

    hood_name = request.GET.get('hood_name')
    district_name = request.GET.get('district_name')
    area_km2 = request.GET.get('area_km2')
    population = request.GET.get('population')
    sip_count = request.GET.get('sip_count')
    population_density = request.GET.get('population_density')
    order_density = request.GET.get('order_density')

    if hood_name:
        qs = qs.filter(hood_name__icontains=hood_name)
    if district_name:
        qs = qs.filter(district_name__icontains=district_name)
    if area_km2:
        try:
            qs = qs.filter(area_km2=area_km2)
        except:
            pass
    if population:
        qs = qs.filter(population=population)
    if sip_count:
        qs = qs.filter(sip_count=sip_count)
    if population_density:
        try:
            qs = qs.filter(population_density=population_density)
        except:
            pass
    if order_density:
        try:
            qs = qs.filter(order_density=order_density)
        except:
            pass

    return render(request, 'sip_density_per_hood.html', {'data': qs})
