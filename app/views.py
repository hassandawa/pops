########################################
# app\views.py
########################################
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Product, District, Market
import csv
import json
import random
from datetime import datetime, timedelta

def index(request):
    # Fetch distinct options for dropdowns
    districts = list(District.objects.values_list('name', flat=True))
    markets = list(Market.objects.values_list('name', flat=True))
    products = list(Product.objects.values_list('product', flat=True).distinct())

    # Add default "All" options
    districts.insert(0, "All Districts")
    markets.insert(0, "All Markets")

    # Get filter selections from the request
    selected_district = request.GET.get('district', "All Districts")
    selected_market = request.GET.get('market', "All Markets")
    selected_product = request.GET.get('product', '')
    selected_date = request.GET.get('date', '')
    selected_month = request.GET.get('month', '')
    selected_year = request.GET.get('year', '')

    # Start with all products
    product_list = Product.objects.all().order_by('-created_at')

    # If no filters are applied, show only products with no district and no market
    if not request.GET:
        product_list = product_list.filter(Q(district__isnull=True) & Q(market__isnull=True))

    # Apply filters for district, market, and product
    if selected_district != "All Districts":
        product_list = product_list.filter(district__name=selected_district)

    if selected_market != "All Markets":
        product_list = product_list.filter(market__name=selected_market)

    if selected_product:
        product_list = product_list.filter(product=selected_product)

    # Apply date, month, and year filtering
    if selected_date:
        try:
            date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
            product_list = product_list.filter(created_at__date=date_obj.date())
        except ValueError:
            pass  # Ignore invalid date format

    if selected_month:
        try:
            month_obj = datetime.strptime(selected_month, "%Y-%m")
            product_list = product_list.filter(
                created_at__year=month_obj.year, created_at__month=month_obj.month
            )
        except ValueError:
            pass  # Ignore invalid month format

    if selected_year:
        try:
            year_int = int(selected_year)
            product_list = product_list.filter(created_at__year=year_int)
        except ValueError:
            pass  # Ignore invalid year format

    # Format price and date for display
    for product in product_list:
        product.price = "{:,.0f}".format(product.price)  # Format price as 97,800
        if product.created_at:
            product.created_at = product.created_at.strftime("%d/%m/%y, %I:%M %p").lower()  # Format date

    # Context for rendering the template
    context = {
        'product_list': product_list,
        'districts': districts,
        'markets': markets,
        'products': products,
        'selected_district': selected_district if selected_district != "All Districts" else '',
        'selected_market': selected_market if selected_market != "All Markets" else '',
        'selected_product': selected_product,
        'selected_date': selected_date,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    return render(request, 'index.html', context)




def get_markets(request, district_id):
    """
    Fetch markets for a given district ID.
    """
    markets = Market.objects.filter(district_id=district_id)
    market_data = [{'id': market.id, 'name': market.name} for market in markets]

    return JsonResponse({'markets': market_data})


def export_csv(request):
    """
    Export product data to a CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Products.csv'

    writer = csv.writer(response)
    writer.writerow(['Products', 'Quantity', 'Price', 'District', 'Market', 'Date'])

    for product in Product.objects.all():
        writer.writerow([
            product.product,
            product.quantity,
            "{:,.0f}".format(product.price),  # Format price as 97,800
            product.district.name if product.district else "All Districts",
            product.market.name if product.market else "All Markets",
            product.created_at.strftime("%d/%m/%y, %I:%M %p").lower(),  # Format date
        ])

    return response
