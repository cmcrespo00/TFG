from django.urls import path
from . import views

urlpatterns = [
    path('', views.paginaprincipal, name="principal"),
    path('perfil/', views.perfil, name="perfil"),
    path('alertas/', views.alertas, name="alertas"),
    path('alertas/<int:id_alerta>/', views.mostraralerta),
    path('temperaturas/', views.temperaturas, name="temperatura"),
    path('humedad/', views.humedad, name="humedad"),
    path('quienessomos/', views.quienessomos, name="quienessomos"),
    path('privacidad/', views.privacidad, name="privacidad"),
]