from datetime import datetime
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from users.models import User
from vacations.forms import VacationRequestForm
from vacations.models import VacationRequest
from vacations.utils import get_using_date


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'vacations/index.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class VacationRequestHistoryListView(View):
    template_name = 'vacations/request_history_list.html'

    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)
        queryset = VacationRequest.objects.filter(user=user)

        context = {
            'vacation_list': queryset,
            'remain_vacation': user.remain_date,
            'selected_menu': 'request_history_list',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UnapprovedVacationRequestView(View):
    template_name = 'vacations/unapproved_request_list.html'

    def get(self, request):
        queryset = VacationRequest.objects.filter(status=0)
        context = {
            'vacation_list': queryset,
            'selected_menu': 'unapproved_request_list',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class VacationRequestCreate(CreateView):
    model = VacationRequest
    success_url = reverse_lazy('vacations:unapproved_request_list')
    form_class = VacationRequestForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.using_date = get_using_date(form.instance.start_date, form.instance.end_date)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TodoApproveListView(View):
    template_name = 'vacations/todo_approve_list.html'

    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)
        queryset = VacationRequest.objects.filter(
            user__team=user.team,
            status=0,
        )
        context = {
            'team': user.get_team_display(),
            'selected_menu': 'todo_approve_list',
            'vacation_list': queryset,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class VacationRequestDetailView(View):
    template_name = 'vacations/detail.html'

    def get(self, request, request_id):
        vacation = get_object_or_404(VacationRequest, id=request_id)
        context = {
            'TYPE_CHOICES': VacationRequest.TYPE_CHOICES,
            'vacation': vacation,
        }
        return render(request, self.template_name, context)

    def post(self, request, request_id):
        vacation = get_object_or_404(VacationRequest, id=request_id)
        # _approve 값을 가지면 승인 아니면 기각
        approve = True if request.POST.get('_approve', False) else False

        try:
            if approve:
                vacation.status = 1
            else:
                vacation.status = 2
            vacation.approver = request.user.name
            vacation.save(update_fields=['status', 'approver'])
        except Exception as e:
            messages.error(request, '휴가신청 상태를 변경하는 데 오류가 발생했습니다: {}'.format(str(e)))
        return redirect('vacations:todo_approve_list')
