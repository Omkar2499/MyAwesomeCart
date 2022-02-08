from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    
   
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handeLogin, name="handleLogin"),
    path('signup/login/', views.handeLogin, name="handleLogin"),
    path('login/logout/', views.handelLogout, name="handleLogout"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path('signup/login/logout/', views.handelLogout, name="handleLogout"),
    path('payment/',views.payment,name="payment")
    

]
