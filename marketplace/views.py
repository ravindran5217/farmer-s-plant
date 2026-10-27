from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import Order, Product, TradeEnquiry


def home(request):
    featured_products = Product.objects.filter(is_available=True, quantity__gt=0)[:6]
    return render(request, "home.html", {"featured_products": featured_products})


@require_http_methods(["GET", "POST"])
def trade(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        company = request.POST.get("company", "").strip()
        enquiry_type = request.POST.get("enquiry_type", "").strip()
        product = request.POST.get("product", "").strip()
        quantity = request.POST.get("quantity", "").strip()
        message = request.POST.get("message", "").strip()

        valid_types = {choice[0] for choice in TradeEnquiry.ENQUIRY_CHOICES}
        if not all([name, email, enquiry_type, product, message]) or enquiry_type not in valid_types:
            messages.error(request, "Please complete all required fields with valid details.")
        else:
            TradeEnquiry.objects.create(
                name=name, email=email, company=company, enquiry_type=enquiry_type,
                product=product, quantity=quantity, message=message
            )
            messages.success(request, "Your trade enquiry has been submitted successfully.")
            return redirect("marketplace:trade")

    products = Product.objects.filter(is_available=True, quantity__gt=0)
    return render(request, "trade.html", {"products": products})


@require_http_methods(["GET", "POST"])
def marketplace(request):
    search_query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    products = Product.objects.filter(is_available=True, quantity__gt=0)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(farmer_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    if category in {"Fruit", "Vegetable"}:
        products = products.filter(category=category)

    if request.method == "POST":
        product_id = request.POST.get("product_id", "")
        customer_name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        try:
            requested_quantity = Decimal(request.POST.get("quantity", "0"))
        except (InvalidOperation, TypeError):
            requested_quantity = Decimal("0")

        product = get_object_or_404(Product, pk=product_id)
        if not all([customer_name, phone, address]) or requested_quantity <= 0:
            messages.error(request, "Enter your name, phone, delivery address, and a valid quantity.")
        else:
            with transaction.atomic():
                locked_product = Product.objects.select_for_update().get(pk=product.pk)
                if not locked_product.is_available or requested_quantity > locked_product.quantity:
                    messages.error(request, f"Sorry, only {locked_product.quantity} {locked_product.unit} of {locked_product.name} are available.")
                else:
                    order = Order.objects.create(
                        customer_name=customer_name,
                        phone=phone,
                        address=address,
                        product=locked_product,
                        quantity=requested_quantity,
                        total_price=(locked_product.price * requested_quantity).quantize(Decimal("0.01")),
                    )
                    locked_product.quantity -= requested_quantity
                    if locked_product.quantity <= 0:
                        locked_product.is_available = False
                    locked_product.save(update_fields=["quantity", "is_available"])
                    messages.success(request, "Your order has been placed.")
                    return redirect("marketplace:order_success", order_id=order.pk)

    return render(request, "marketplace.html", {
        "products": products,
        "search_query": search_query,
        "selected_category": category,
    })


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "order_success.html", {"order": order})
