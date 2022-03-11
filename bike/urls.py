from django.urls import path, re_path
from . import views, utilitiesViews
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('', views.home, name='home'),
	path('bikelist/', views.bike_list, name='bikelist'),
	path('bikeinfo/<int:id>/',views.bikePage, name='bikePage'),
	path('gallery',views.gallery, name='gallery'),

	path('register/', views.registerPage, name='register'),
	path('logout/',views.logoutPage, name='logout'),
    path('customer/<int:id>/',views.customerPage, name='customer'),

	path('createOrder/<int:id>/',views.createOrder, name='createOrder'),
	path('makeOrder/<int:id>/',views.makeOrder, name='makeOrder'),
	path('cancelOrder/<int:id>/', views.cancelOrder, name='cancelOrder'),
    
	path('pdfView/<int:id>/', utilitiesViews.ViewPDF.as_view(), name="pdfView"),
    path('pdfDownload/<int:id>/', utilitiesViews.DownloadPDF.as_view(), name="pdfDownload"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
