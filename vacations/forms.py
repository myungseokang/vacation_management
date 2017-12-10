from django.forms import ModelForm

from vacations.models import VacationRequest


class VacationRequestForm(ModelForm):

    class Meta:
        model = VacationRequest
        fields = ('type', 'start_date', 'end_date', 'reason', 'document', )
