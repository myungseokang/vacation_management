from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    template_name = 'index.html'

    def get(self, request):
        context = {
            'selected_menu': 'index',
        }
        if request.user.is_team_leader:
            context['vacation_list'] = VacationRequest.objects.filter(status=0, user__team=request.user.team)

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class VacationRequestHistoryListView(View):
    template_name = 'vacations/request_history_list.html'

    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)
        queryset = VacationRequest.objects.filter(user=user)

        context = {
            'vacation_list': queryset,
            'selected_menu': 'request_history_list',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class VacationRequestCreate(CreateView):
    model = VacationRequest
    success_url = reverse_lazy('vacations:request_history_list')
    form_class = VacationRequestForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.using_date = get_using_date(form.instance.start_date, form.instance.end_date)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_menu'] = 'create_request'
        return context


@method_decorator(login_required, name='dispatch')
class TodoApproveListView(View):
    template_name = 'vacations/todo_approve_list.html'

    def get(self, request):
        user = get_object_or_404(User, email=request.user.email)

        if not user.is_team_leader:
            messages.error(request, '권한이 없습니다.')
            redirect('vacations:request_history_list')

        queryset = VacationRequest.objects.filter(
            user__team=user.team,
            status=0,
        )
        context = {
            'team': user.get_team_display(),
            'vacation_list': queryset,
            'selected_menu': 'todo_approve_list',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class TeamAllRequestListView(View):
    template_name = 'vacations/team_all_request_list.html'

    def get(self, request):
        team = request.user.team
        queryset = VacationRequest.objects.filter(user__team=team)

        context = {
            'vacation_list': queryset,
            'selected_menu': 'team_all_request_list',
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
        vacation = get_object_or_404(
            VacationRequest.objects.select_related('user'),
            id=request_id
        )
        # _approve 값을 가지면 승인 아니면 기각
        approve = True if request.POST.get('_approve', False) else False

        try:
            if approve:
                vacation.status = 1
            else:
                vacation.status = 2
            vacation.approver = request.user.name
            if vacation.type == 0:
                result_date = vacation.user.remain_date - vacation.using_date
                if result_date < 0:
                    messages.error(request, '사용일수가 남은 일수보다 높습니다.')
                    raise Exception
                else:
                    vacation.user.remain_date = result_date

                vacation.user.save(update_fields=['remain_date'])

            vacation.save(update_fields=['status', 'approver'])
        except Exception as e:
            messages.error(request, '휴가신청 상태를 변경하는 데 오류가 발생했습니다: {}'.format(str(e)))
        return redirect('vacations:request_history_list')
