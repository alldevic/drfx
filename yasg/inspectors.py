from rest_framework_json_api import serializers, pagination
from rest_framework_json_api.utils import get_related_resource_type
from drf_yasg import openapi, inspectors, utils, errors
import djoser
import rest_framework_simplejwt


class ResourceRelatedFieldInspector(inspectors.FieldInspector):
    def field_to_swagger_object(
            self, field, swagger_object_type, use_references, **kwargs
    ):
        if isinstance(field, serializers.ResourceRelatedField):
            return None

        return inspectors.NotHandled


class ModelSerializerInspector(inspectors.FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        if (isinstance(obj, serializers.ModelSerializer) and
                method_name == 'field_to_swagger_object'):
            model_response = self.formatted_model_result(result, obj)
            if obj.parent is None and self.view.action != 'list':
                # It will be top level object not in list, decorate with data
                return self.decorate_with_data(model_response)

            return model_response

        return result

    def generate_relationships(self, obj):
        relationships_properties = []
        for field in obj.fields.values():
            if isinstance(field, serializers.ResourceRelatedField):
                relationships_properties.append(
                    self.generate_relationship(field)
                )
        if relationships_properties:
            return openapi.Schema(
                title='Relationships of object',
                type=openapi.TYPE_OBJECT,
                properties=utils.OrderedDict(relationships_properties),
            )

    def generate_relationship(self, field):
        field_schema = openapi.Schema(
            title='Relationship object',
            type=openapi.TYPE_OBJECT,
            properties=utils.OrderedDict((
                ('type', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='Type of related object',
                    enum=[get_related_resource_type(field)]
                )),
                ('id', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='ID of related object',
                ))
            ))
        )
        return field.field_name, self.decorate_with_data(field_schema)

    def formatted_model_result(self, result, obj):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['properties'],
            properties=utils.OrderedDict((
                ('type', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[serializers.get_resource_type_from_serializer(obj)],
                    title='Type of related object',
                )),
                ('id', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    title='ID of related object',
                    read_only=True
                )),
                ('attributes', result),
                ('relationships', self.generate_relationships(obj))
            ))
        )

    def decorate_with_data(self, result):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties=utils.OrderedDict((
                ('data', result),
            ))
        )


class DjangoRestJsonApiResponsePagination(inspectors.PaginatorInspector):
    def get_paginator_parameters(self, paginator):
        return [
            openapi.Parameter(
                'limit', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'offset', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            ),
        ]

    def get_paginated_response(self, paginator, response_schema):
        paged_schema = None
        if isinstance(paginator, pagination.LimitOffsetPagination):
            paged_schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=utils.OrderedDict((
                    ('links', self.generate_links()),
                    ('data', response_schema),
                    ('meta', self.generate_meta())
                )),
                required=['data']
            )

        return paged_schema

    def generate_links(self):
        return openapi.Schema(
            title='Links',
            type=openapi.TYPE_OBJECT,
            required=['first', 'last'],
            properties=utils.OrderedDict((
                ('first', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to first object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('last', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to last object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('next', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to next object',
                    read_only=True, format=openapi.FORMAT_URI
                )),
                ('prev', openapi.Schema(
                    type=openapi.TYPE_STRING, title='Link to prev object',
                    read_only=True, format=openapi.FORMAT_URI
                ))
            ))
        )

    def generate_meta(self):
        return openapi.Schema(
            title='Meta of result with pagination count',
            type=openapi.TYPE_OBJECT,
            required=['count'],
            properties=utils.OrderedDict((
                ('count', openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    title='Number of results on page',
                )),
            ))
        )


class ActivationJSONAPIMeta:
    resource_name = "activation"


class TokenJSONAPIMeta:
    resource_name = "token"


class PasswordResetJSONAPIMeta:
    resource_name = "password-reset"


class PasswordResetConfirmJSONAPIMeta:
    resource_name = "password-reset-confirm"


class PasswordChangeJSONAPIMeta:
    resource_name = "password-change"


class PasswordResetConfirmRetypeJSONAPIMeta:
    resource_name = "password-reset-confirm-retype"


class SetPasswordRetypeJSONAPIMeta:
    resource_name = "set-password-retype"


class SetPasswordJSONAPIMeta:
    resource_name = "set-password"


class SetUsernameRetypeJSONAPIMeta:
    resource_name = "set-username-retype"


class SetUsernameJSONAPIMeta:
    resource_name = "set-username"


class UserJSONAPIMeta:
    resource_name = "user"


class UserCreateJSONAPIMeta:
    resource_name = "user-create"


class UserDeleteJSONAPIMeta:
    resource_name = "user-delete"


class CurrentUserJSONAPIMeta:
    resource_name = "current-user"


class TokenCreateJSONAPIMeta:
    resource_name = "token-create"


class TokenObtainJSONAPIMeta:
    resource_name = "jwt-obtain"


class TokenVerifyJSONAPIMeta:
    resource_name = "jwt-verify"


class TokenRefreshJSONAPIMeta:
    resource_name = "jwt-refresh"


djoser.serializers.ActivationSerializer.JSONAPIMeta = ActivationJSONAPIMeta
djoser.serializers.PasswordResetSerializer.JSONAPIMeta = PasswordResetJSONAPIMeta
djoser.serializers.PasswordResetConfirmSerializer.JSONAPIMeta = PasswordResetConfirmJSONAPIMeta
djoser.serializers.PasswordResetConfirmRetypeSerializer.JSONAPIMeta = PasswordResetConfirmRetypeJSONAPIMeta
djoser.serializers.SetPasswordSerializer.JSONAPIMeta = SetPasswordJSONAPIMeta
djoser.serializers.SetPasswordRetypeSerializer.JSONAPIMeta = SetPasswordRetypeJSONAPIMeta
djoser.serializers.SetUsernameSerializer.JSONAPIMeta = SetUsernameJSONAPIMeta
djoser.serializers.SetUsernameRetypeSerializer.JSONAPIMeta = SetUsernameRetypeJSONAPIMeta
djoser.serializers.UserCreateSerializer.JSONAPIMeta = UserCreateJSONAPIMeta
djoser.serializers.UserDeleteSerializer.JSONAPIMeta = UserDeleteJSONAPIMeta
djoser.serializers.UserSerializer.JSONAPIMeta = UserJSONAPIMeta
djoser.serializers.CurrentUserSerializer.JSONAPIMeta = CurrentUserJSONAPIMeta
djoser.serializers.TokenSerializer.JSONAPIMeta = TokenJSONAPIMeta
djoser.serializers.TokenCreateSerializer.JSONAPIMeta = TokenCreateJSONAPIMeta
rest_framework_simplejwt.serializers.TokenObtainSerializer.JSONAPIMeta = TokenObtainJSONAPIMeta
rest_framework_simplejwt.serializers.TokenVerifySerializer.JSONAPIMeta = TokenVerifyJSONAPIMeta
rest_framework_simplejwt.serializers.TokenRefreshSerializer.JSONAPIMeta = TokenRefreshJSONAPIMeta

customs = [djoser.serializers.ActivationSerializer,
           djoser.serializers.PasswordResetSerializer,
           djoser.serializers.PasswordResetConfirmSerializer,
           djoser.serializers.PasswordResetConfirmRetypeSerializer,
           djoser.serializers.SetPasswordSerializer,
           djoser.serializers.SetPasswordRetypeSerializer,
           djoser.serializers.SetUsernameSerializer,
           djoser.serializers.SetUsernameRetypeSerializer,
           djoser.serializers.UserCreateSerializer,
           djoser.serializers.UserDeleteSerializer,
           djoser.serializers.UserSerializer,
           djoser.serializers.CurrentUserSerializer,
           djoser.serializers.TokenSerializer,
           djoser.serializers.TokenCreateSerializer,
           rest_framework_simplejwt.serializers.TokenObtainSerializer,
           rest_framework_simplejwt.serializers.TokenVerifySerializer,
           rest_framework_simplejwt.serializers.TokenRefreshSerializer,
           ]


class CustomSerializerInspector(inspectors.FieldInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        for sr in customs:
            fl = isinstance(obj, sr)
            if fl:
                break

        if (fl and method_name == 'field_to_swagger_object'):
            model_response = self.formatted_model_result(result, obj)
            if obj.parent is None:
                # It will be top level object not in list, decorate with data
                return self.decorate_with_data(model_response)

            return model_response

        return result

    def formatted_model_result(self, result, obj):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['properties'],
            properties=utils.OrderedDict((
                ('type', openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[serializers.get_resource_type_from_serializer(obj)],
                    title='Type of related object',
                )),
                ('attributes', result),
            ))
        )

    def decorate_with_data(self, result):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties=utils.OrderedDict((
                ('data', result),
            ))
        )
