from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from store.models import Category, Order, OrderItem, Product

User = get_user_model()


@pytest.mark.django_db
def test_order_item_subtotal():
    user = User.objects.create_user(username="u1", password="pass")
    category = Category.objects.create(name="Cat", slug="cat")
    product = Product.objects.create(name="P1", price=Decimal("10.00"), category=category)
    order = Order.objects.create(user=user)
    item = OrderItem.objects.create(order=order, product=product, quantity=3, price=Decimal("10.00"))
    assert item.subtotal == Decimal("30.00")


@pytest.mark.django_db
def test_order_total():
    user = User.objects.create_user(username="u2", password="pass")
    category = Category.objects.create(name="Cat2", slug="cat2")
    p1 = Product.objects.create(name="P2", price=Decimal("5.00"), category=category)
    p2 = Product.objects.create(name="P3", price=Decimal("15.00"), category=category)
    order = Order.objects.create(user=user)
    OrderItem.objects.create(order=order, product=p1, quantity=2, price=Decimal("5.00"))
    OrderItem.objects.create(order=order, product=p2, quantity=1, price=Decimal("15.00"))
    assert order.total == Decimal("25.00")


@pytest.mark.django_db
def test_order_default_status():
    user = User.objects.create_user(username="u3", password="pass")
    order = Order.objects.create(user=user)
    assert order.status == Order.Status.PENDING


@pytest.mark.django_db
def test_product_list_returns_200():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_list_filter_by_category():
    client = Client()
    cat_a = Category.objects.create(name="Alpha", slug="alpha")
    cat_b = Category.objects.create(name="Beta", slug="beta")
    Product.objects.create(name="In Alpha", price=Decimal("1.00"), category=cat_a)
    Product.objects.create(name="In Beta", price=Decimal("2.00"), category=cat_b)
    response = client.get("/?category=alpha")
    assert response.status_code == 200
    products = list(response.context["products"])
    assert all(p.category == cat_a for p in products)
    assert len(products) == 1


@pytest.mark.django_db
def test_order_create_redirects_anonymous():
    client = Client()
    response = client.get("/orders/create/")
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


@pytest.mark.django_db
def test_order_detail_forbidden_for_other_user():
    client = Client()
    user_a = User.objects.create_user(username="user_a", password="pass")
    User.objects.create_user(username="user_b", password="pass")
    order = Order.objects.create(user=user_a)
    client.login(username="user_b", password="pass")
    response = client.get(f"/orders/{order.pk}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_product_detail_returns_200():
    client = Client()
    category = Category.objects.create(name="DetailCat", slug="detail-cat")
    product = Product.objects.create(name="DetailProd", price=Decimal("9.99"), category=category)
    response = client.get(f"/products/{product.pk}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_list_shows_only_own_orders():
    client = Client()
    user_a = User.objects.create_user(username="list_a", password="pass")
    user_b = User.objects.create_user(username="list_b", password="pass")
    Order.objects.create(user=user_a)
    Order.objects.create(user=user_b)
    client.login(username="list_a", password="pass")
    response = client.get("/orders/")
    assert response.status_code == 200
    orders = list(response.context["orders"])
    assert len(orders) == 1
    assert orders[0].user == user_a


@pytest.mark.django_db
def test_order_create_post_creates_order():
    client = Client()
    user = User.objects.create_user(username="buyer", password="pass")
    category = Category.objects.create(name="PostCat", slug="post-cat")
    product = Product.objects.create(name="PostProd", price=Decimal("20.00"), category=category)
    client.login(username="buyer", password="pass")
    response = client.post("/orders/create/", {"product": product.pk, "quantity": 2})
    assert response.status_code == 302
    order = Order.objects.get(user=user)
    assert order.items.count() == 1
    assert order.items.first().quantity == 2
