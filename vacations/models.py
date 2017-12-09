from django.db import models


class VacationRequest(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=None,
        related_name='vacation_request_set',
        related_query_name='vacation_request',
    )

    TYPE_CHOICES = (
        (0, '정기 휴가'),
        (1, '병가'),
        (2, '출산휴가'),
        (3, '경조사 휴가(결혼, 장례, 기타)'),
        (4, '무급 휴가'),
    )
    type = models.PositiveSmallIntegerField('휴가 타입', choices=TYPE_CHOICES)
    start_date = models.DateTimeField('휴가 시작일')
    end_date = models.DateTimeField('휴가 종료일')
    using_date = models.FloatField('사용 일수')
    APPROVAL_STATUS_CHOICE = (
        (0, '신청'),
        (1, '승인'),
        (2, '기각'),
    )
    status = models.PositiveSmallIntegerField('상태', choices=APPROVAL_STATUS_CHOICE, default=0)
    approver = models.CharField('승인자', max_length=16)
    reason = models.TextField('사유')
    document = models.FileField(upload_to='documents/%Y/%m/%d/')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
