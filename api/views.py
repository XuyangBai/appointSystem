# coding=utf-8
import datetime

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from account.models import Account
from account.serializer import AccountSerializer
from appointment.models import Appointment, STATUS
from appointment.serializer import AppointmentSerializer
from classroom.models import Classroom


class ClassroomViewSet(viewsets.GenericViewSet):
    serializer_class = AppointmentSerializer

    # STATUS为 cancaled的订单信息不会返回
    def list(self, request, **kwargs):
        classroom = kwargs['classroom']
        user = request.user
        today = datetime.date.today()
        endday = today + datetime.timedelta(28)
        classroom = Classroom.objects.get(name=classroom)
        appointments = classroom.appointment_set.filter(date__gte=today,
                                                        date__lte=endday,
                                                        status=STATUS.waiting).distinct()
        if 'mine' in request.GET:
            appointments = appointments.filter(custom__user=user)
        appointments = appointments.values('id',
                                           'reason',
                                           'date',
                                           'start',
                                           'end',
                                           'desk',
                                           'multimedia',
                                           'status',
                                           'custom__user__username',
                                           'custom__telephone')
        size = len(appointments)
        return Response({"success": True,
                         "size": size,
                         "appointments": appointments,
                         },
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk, **kwargs):
        classroom = get_object_or_404(Classroom, name=kwargs['classroom'])
        appointment = get_object_or_404(classroom.appointment_set, id=pk)
        serializer = AppointmentSerializer(appointment)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @csrf_exempt
    def create(self, request, **kwargs):
        classroom = kwargs["classroom"]
        if not Classroom.objects.filter(name=classroom).exists():
            return Response({"message": "Classroom Not Found"}, status=404)
        classroom = Classroom.objects.get(name=classroom)
        appointment = AppointmentSerializer(data=request.POST)
        if appointment.is_valid(raise_exception=True):
            appointment.save(custom=Account.objects.get(user=request.user), classroom=classroom)
            return Response(status=201)
        return Response({"message": appointment.errors}, status=400)

    # # delete并非真正删除，而是将status置为canceled
    # def delete(self, request, pk, **kwargs):
    #     classroom = get_object_or_404(Classroom, name=kwargs['classroom'])
    #     appointment = get_object_or_404(classroom.appointment_set, id=pk)
    #     appointment.status = STATUS.canceled
    #     appointment.save()
    #     return Response({"message": "cancel this appointment"}, status=status.HTTP_204_NO_CONTENT)

    # 这种写法实际上是不符合REST的规范的
    @csrf_exempt
    @detail_route(methods=['post'])
    def delete_appoint(self, request, pk, **kwargs):
        classroom = get_object_or_404(Classroom, name=kwargs['classroom'])
        appointment = get_object_or_404(classroom.appointment_set, id=pk)
        appointment.status = STATUS.canceled
        appointment.save()
        return Response({"message": "cancel this appointment"}, status=status.HTTP_204_NO_CONTENT)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
