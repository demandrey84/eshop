from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import (
    LoginForm,
    MyPasswordResetForm,
    MyPasswordChangeForm,
    MySetPasswordForm,
)


urlpatterns = [
    path("", views.home),
    # home
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # product
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name="category-title"),
    path(
        "product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"
    ),
    # profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.addres, name="address"),
    path(
        "update-address/<int:pk>", views.updateAddress.as_view(), name="updateAddress"
    ),
    # cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("checkout/", views.checkout.as_view(), name="checkout"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
    path("orders/", views.orders, name="orders"),

    # search
    path("search/", views.search,name="search"),

    # wishlist
    path("wishlist/", views.show_wishlist, name="showwishlist"),
    path("pluswishlist/", views.plus_wishlist),
    path("minuswishlist/", views.minus_wishlist),
   
    # login authentication
    path(
        "registration/",
        views.CustomerRegistrationView.as_view(),
        name="customerregistration",
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="online/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path(
        "passwordchange/",
        auth_views.PasswordChangeView.as_view(
            template_name="online/passwordchange.html",
            form_class=MyPasswordChangeForm,
            success_url="/passwordchangedone",
        ),
        name="passwordchange",
    ),
    path(
        "passwordchangedone/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="online/passwordchangedone.html"
        ),
        name="passwordchangedone",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(
            template_name="online/password_reset.html", form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="online/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="online/password_reset_confirm.html",
            form_class=MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="online/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
