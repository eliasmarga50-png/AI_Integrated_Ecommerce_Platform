


from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [

    # Customer dashboard
    path(
        "customer/",
        views.customer_dashboard,
        name="customer_dashboard",
    ),


    # Seller dashboard
    path(
        "seller/",
        views.seller_dashboard,
        name="seller_dashboard",
    ),


    # Admin dashboard
    path(
        "admin/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

]


