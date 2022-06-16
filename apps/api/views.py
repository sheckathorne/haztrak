import http
import os

from django.core.exceptions import ObjectDoesNotExist
from emanifest import client as em
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Profile
from apps.trak.models import Handler, Manifest, Transporter
from lib.rcrainfo import rcrainfo

from .serializers import (HandlerSerializer, ManifestSerializer,
                          TransporterSerializer)


class ManifestView(APIView):
    response = Response

    def get(self, request: Request, mtn: str = None) -> Response:
        try:
            if mtn:
                manifest = Manifest.objects.get(mtn=mtn)
                serializer = ManifestSerializer(manifest)
                return self.response(serializer.data)
            else:
                manifest = Manifest.objects.all()
                serializer = ManifestSerializer(manifest, many=True)
                return self.response(serializer.data)
        except APIException:
            return self.response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                                 data=APIException)
        except ObjectDoesNotExist:
            return self.response(status=http.HTTPStatus.NOT_FOUND,
                                 data={'Error': f'{mtn} not found'})

    def post(self, request: Request, mtn: str = None) -> Response:
        if not mtn:
            return self.response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ManifestSerializer(data=request.data)
            valid = serializer.is_valid()
            if valid:
                serializer.save()
                return self.response(status=200)
            else:
                return self.response(status=500)


# trash, not time remove it right now
class SyncSiteManifest(APIView):
    response = Response

    def get(self, request: Request, epa_id: str = None) -> Response:
        if epa_id:
            resp = rcrainfo.get_mtns(epa_id)
            return Response(data={'mtn': resp.json})
        else:
            return self.response(status=status.HTTP_200_OK)


class HandlerView(APIView):
    response = Response

    def get(self, request: Request, epa_id: str = None) -> Response:
        try:
            if epa_id:
                handler = Handler.objects.get(epa_id=epa_id)
                serializer = HandlerSerializer(handler)
                return self.response(serializer.data)
        except APIException:
            return self.response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return self.response(status=http.HTTPStatus.NOT_FOUND,
                                 data={'Error': f'{epa_id} not found'})


class TransporterView(APIView):
    response = Response

    def get(self, request: Request, tran_id: int = None) -> Response:
        try:
            if tran_id:
                transporter = Transporter.objects.get(id=tran_id)
                serializer = TransporterSerializer(transporter)
                return self.response(serializer.data)
        except APIException:
            return self.response(status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            return self.response(status=http.HTTPStatus.NOT_FOUND,
                                 data={'Error': f'{tran_id} not found'})


# ToDo authentication, right now will work as long as user is signed
#  into haztrak via the browser for demo purposes. Just Demo!
class PullManifest(APIView):
    if os.getenv('RCRAINFO_ENV'):
        ri_client = em.new_client(os.getenv('RCRAINFO_ENV'))
    else:
        ri_client = em.new_client('preprod')

    def post(self, request: Request) -> Response:
        try:
            user_profile = Profile.objects.get(user_id=self.request.user)
            self.ri_client.Auth(user_profile.rcra_api_id, user_profile.rcra_api_key)
            data = {'mtn': []}
            for mtn in self.request.data['mtn']:
                resp = self.ri_client.GetManByMTN(mtn)
                data['mtn'].append({mtn: resp.response.status_code})
                if Manifest.objects.filter(mtn=mtn):
                    print('manifest exists')
                    pass
                else:
                    new_manifest = ManifestSerializer(data=resp.json)
                    new_manifest.is_valid()
                    new_manifest.save()
            print(data)
            return Response(status=status.HTTP_200_OK, data=data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
