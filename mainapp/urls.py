from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mainapp_index'),
    path('step1', views.step1, name='mainapp_step1'),
    path('report/<str:report_id>/', views.enviar_resultado),
    path('decision', views.decision, name='mainapp_decision'),
    path('exito/<str:report_id>/', views.mostrar_resultado),
    path('mostrar_reporte', views.mostrar_reporte, name='mainapp_mostrar'),
    path('volver', views.volver, name='mainapp_volver')
]