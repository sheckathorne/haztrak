from http import HTTPStatus

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.fields import CharField
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.trak.models import Handler
from apps.trak.serializers import HandlerSerializer


class TransporterSearch(GenericAPIView):
    queryset = Handler.objects.all()

    @extend_schema(
        description='Search for Transporters saved to the Haztrak database',
        # methods=['POST'],
        request=inline_serializer(name='test',
                                  fields={'epaId': CharField(), 'name': CharField()}),
    )
    def post(self, request):
        try:
            epa_id = self.request.data['epaId']
            name = self.request.data['name']
            if len(epa_id) < 3 and len(name) < 3:
                return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)
            transporters_queryset = Handler.objects.filter(
                site_type='Transporter').filter(
                epa_id__icontains=epa_id).filter(name__icontains=name)
            data = list(transporters_queryset)
            response = []
            for i in data:
                response.append(HandlerSerializer(i).data)
            return Response(status=HTTPStatus.OK, data=response)
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)