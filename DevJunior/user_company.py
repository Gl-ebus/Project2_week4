from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from DevJunior.forms import EditCompanyForm, EditVacancyForm
from DevJunior.models import Company, Vacancy, Application


class UserCompanyStart(View):

    def get(self, request):
        return render(request, 'company_create.html')


class UserCompanyCreate(View):

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        form = EditCompanyForm
        return render(request, 'company_edit.html', context={'user': user, 'form': form})

    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        form = EditCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            return redirect('my_company')
        else:
            form = EditCompanyForm()
        context = {'form': form}
        return render(request, 'company_edit.html', context=context)


class UserCompany(View):
    company_modify = False

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        if user is None:
            return redirect('login')
        user_company = Company.objects.filter(owner=user.id).first()
        if user_company is None:
            return redirect('mycompany_start')
        else:
            form = EditCompanyForm(instance=user_company)
            context = {'user': user, 'form': form}
            return render(request, 'company_edit.html', context=context)

    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        instance = Company.objects.filter(owner=user.id).first()
        form = EditCompanyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            self.company_modify = True
        context = {'form': form, 'company_modify': self.company_modify}
        return render(request, 'company_edit.html', context=context)


class UserVacancyCreate(View):

    def get(self, request):
        form = EditVacancyForm
        return render(request, 'vacancy_edit.html', context={'form': form})

    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        form = EditVacancyForm(request.POST)
        company = get_object_or_404(Company, owner=user)
        if form.is_valid():
            vacancy_form = form.save(commit=False)
            vacancy_form.company = company
            vacancy = form.save()
            return redirect('mycompany_vacancy', vacancy_id=vacancy.pk)
        else:
            form = EditCompanyForm()
        return render(request, 'vacancy_edit.html', context={'form': form})


class UserCompanyVacancy(View):
    vacancy_modify = False

    def get(self, request, vacancy_id):
        user = request.user if request.user.is_authenticated else None
        vacancy = Vacancy.objects.annotate(applications_count=Count('applications__vacancy'))\
            .filter(id=vacancy_id).first()
        applications = Application.objects.filter(vacancy=vacancy_id)
        if user is None:
            return redirect('login')
        form = EditVacancyForm(instance=vacancy)
        context = {
            'form': form,
            'vacancy': vacancy,
            'applications': applications,
        }
        return render(request, 'vacancy_edit.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.annotate(
            applications_count=Count('applications__vacancy')).filter(id=vacancy_id).first()
        applications = Application.objects.filter(vacancy=vacancy_id)
        form = EditVacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.company = vacancy.company
            post_form.save()
            self.vacancy_modify = True
        context = {
            'form': form,
            'vacancy': vacancy,
            'applications': applications,
            'vacancy_modify': self.vacancy_modify,
        }
        return render(request, 'vacancy_edit.html', context=context)


class UserCompanyVacancies(View):

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        if user is None:
            return redirect('login')
        company = Company.objects.filter(owner=user.id).first()
        vacancies = Vacancy.objects.filter(company=company.id).annotate(
            applications_count=Count('applications__vacancy')
        )
        if company is None:
            return redirect('mycompany_start')
        if len(vacancies) == 0:
            return redirect('mycompany_vacancy_create')
        return render(request, 'vacancy_list.html', context={'vacancies': vacancies, 'user': user})
