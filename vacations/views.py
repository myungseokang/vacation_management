from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from users.models import User
from vacations.models import VacationRequest


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
class CreateVacationRequestView(View):
    template_name = 'vacations/create.html'

    def get(self, request):
        if request.user.remain_date == 0:
            messages.error(request, '남은 휴가일수가 없습니다 ㅠㅠ')
            return redirect(request.META['HTTP_REFERER'])

        context = {
            'TYPE_CHOICES': VacationRequest.TYPE_CHOICES,
            'selected_menu': 'create_request',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST.get('email', '')
        vacation_type = request.POST.get('type', 0)
        start_date = request.POST.get('start_date', '')
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_date = request.POST.get('end_date', '')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        reason = request.POST.get('reason', '')
        using_date = request.POST.get('using_date', '')
        docs_file = request.FILES.get('docs_file', '')

        user = get_object_or_404(
            User,
            email=email,
        )

        using_date = round((end_date - start_date).total_seconds() / 60 / 24 / 24, 1)
        using_date = 1.0 if using_date == 0.9 else using_date

        try:
            VacationRequest.objects.create(
                user=user,
                type=vacation_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                using_date=using_date,
                # docs_file=docs_file.file,
            )

            messages.success(request, '휴가를 성공적으로 신청했습니다.')
        except Exception as e:
            messages.error(request, '휴가를 신청하던 도중 오류가 발생했습니다.')

        return redirect('vacations:unapproved_request_list')


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
