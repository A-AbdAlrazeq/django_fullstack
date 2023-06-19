from django.shortcuts import render, redirect
from .models import Order, Product


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    product_id = request.POST["product_id"]
    request.session['price'] = float(Product.objects.get(id=product_id).price)
    request.session['quantity'] = int(request.POST["quantity"])
    request.session['total_charge'] = request.session['quantity'] * \
        request.session['price']
    Order.objects.create(quantity_ordered=request.session['quantity'],
                         total_price=request.session['total_charge'])
    return redirect("/result")


def result(request):
    context = {
        'total_charge': request.session['total_charge'],
        'quantity': request.session['quantity'],
        'price': request.session['price']
    }
    return render(request, "store/checkout.html", context)
