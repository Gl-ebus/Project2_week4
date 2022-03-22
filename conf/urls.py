"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from DevJunior import user_company
from DevJunior.views import MainView, AllVacancies, VacanciesSpecialty, VacancyView, CompanyView, custom_handler404, \
    custom_handler500, JobLoginView, JobSignupView, SendView
from conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='home'),
    path('vacancies/', AllVacancies.as_view(), name='vacancies'),
    path('vacancies/cat/<str:spec>/', VacanciesSpecialty.as_view(), name='specialization'),
    path('vacancies/<int:id_vacancy>/', VacancyView.as_view(), name='for vacancy'),
    path('vacancies/<int:id_vacancy>/send/', SendView.as_view(), name='send_application'),
    path('companies/<int:id_company>/', CompanyView.as_view(), name='company'),

    path('mycompany/letsstart/', user_company.UserCompanyStart.as_view(), name='mycompany_start'),
    path('mycompany/create/', user_company.UserCompanyCreate.as_view(), name='mycompany_create'),
    path('mycompany/', user_company.UserCompany.as_view(), name='my_company'),
    path('mycompany/vacancies/create/', user_company.UserVacancyCreate.as_view(), name='mycompany_vacancy_create'),
    path('mycompany/vacancies/<int:vacancy_id>/', user_company.UserCompanyVacancy.as_view(), name='mycompany_vacancy'),
    path('mycompany/vacancies/', user_company.UserCompanyVacancies.as_view(), name='mycompany_vacancies'),

    path('login/', JobLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', JobSignupView.as_view(), name='singup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
handler404 = custom_handler404
handler500 = custom_handler500
