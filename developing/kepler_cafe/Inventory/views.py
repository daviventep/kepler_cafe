from datetime import date, timedelta, datetime, time
import pytz, traceback

from django.db.models import F, Func, Value, CharField
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import make_aware, utc
from django.contrib.auth.decorators import login_required

from .models import Product, Category
from Movement.models import Shopping_Car

# Create your views here.

# @login_required
def products_list(request):
    search_product = ""
    selected_category = None
    if request.POST:
        search_product = request.POST.get("search_product", '')
        selected_category = request.POST.get("selected_category", None)
    products_list = Product.objects.filter(status = True)
    
    if selected_category and selected_category != "":
        products_list = products_list.filter(category__pk = selected_category)
    
    if search_product and search_product != "":
        products_list = products_list.filter(name__contains = search_product)
    
    products_list = list(products_list.values(
        'name',
        'money_unit_price',
        'point_unit_price',
        'quantity',
        'weight',
        'measure_unit',
        category_name = F('category__name'),
        ))
    categories_list = list(Category.objects.all().values(
        'pk',
        'name'
        ))
    shopping_car_quantity = 0
    if request.user.is_authenticated:
        shopping_car_quantity = Shopping_Car.objects.filter(user_id = request.user.identification).count()
    context = {
        'categories_list': categories_list,
        'products_list': products_list,
        'shopping_car_quantity': shopping_car_quantity,
        'search_product': search_product,
        'selected_category': selected_category
    }
    return render(request, 'inventory/products_shop.html', context)

def Product_Description(request):
    """
        Description:
            This function has the objective to get information about the Product selected. 
    """
    return_content = {'errors': [], 'message': {}}
    return_errors = []

    id_product = request.GET.get('id', None)
    if not id_product or id_product == "":
        return_errors.append({ 'title': 'Producto', 'content': 'No se recibió información de algún producto.' })
    elif not Product.objects.filter(pk = id_product).exists():
        return_errors.append({ 'title': 'Producto', 'content': f'No existe el producto con identificación {id_product}.' })
    else:
        product_info = Product.objects.filter(pk = id_product).values("name", "money_unit_price", "point_unit_price", "quantity", "weight", "measure_unit", "category_name", category_name = F("category__name")).get()
        print(product_info)
        return_content
        return_content.update(product_info)

    return_content['errors'] = return_errors
    return render(request, 'inventory/product_detail.html', return_content)
    # return JsonResponse(return_content)
    # return redirect("/")