from rest_framework_json_api import serializers, pagination
from rest_framework_json_api.utils import get_related_resource_type
from drf_yasg import openapi, inspectors, utils, errors
import rest_auth
import rest_framework_jwt


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


class LoginJSONAPIMeta:
    resource_name = "login"


class TokenJSONAPIMeta:
    resource_name = "token"


class JWTJSONAPIMeta:
    resource_name = "jwt"


class UserDetailsJSONAPIMeta:
    resource_name = "user-details"


class PasswordResetJSONAPIMeta:
    resource_name = "password-reset"


class PasswordResetConfirmJSONAPIMeta:
    resource_name = "password-reset-confirm"


class PasswordChangeJSONAPIMeta:
    resource_name = "password-change"


class RegisterJSONAPIMeta:
    resource_name = "register"


class VerifyEmailJSONAPIMeta:
    resource_name = "verify-email"


rest_auth.serializers.LoginSerializer.JSONAPIMeta = LoginJSONAPIMeta
rest_auth.serializers.TokenSerializer.JSONAPIMeta = TokenJSONAPIMeta
rest_auth.serializers.JWTSerializer.JSONAPIMeta = JWTJSONAPIMeta
rest_auth.serializers.UserDetailsSerializer.JSONAPIMeta = UserDetailsJSONAPIMeta
rest_auth.serializers.PasswordResetSerializer.JSONAPIMeta = PasswordResetJSONAPIMeta
rest_auth.serializers.PasswordResetConfirmSerializer.JSONAPIMeta = PasswordResetConfirmJSONAPIMeta
rest_auth.serializers.PasswordChangeSerializer.JSONAPIMeta = PasswordChangeJSONAPIMeta
rest_auth.registration.serializers.RegisterSerializer.JSONAPIMeta = RegisterJSONAPIMeta
rest_auth.registration.serializers.VerifyEmailSerializer.JSONAPIMeta = VerifyEmailJSONAPIMeta


class JWTTokenJSONAPIMeta:
    resource_name = "jwt-token"


class JWTRefreshJSONAPIMeta:
    resource_name = "jwt-refresh"


class JWTVerifyJSONAPIMeta:
    resource_name = "jwt-verify"


rest_framework_jwt.serializers.JSONWebTokenSerializer.JSONAPIMeta = JWTTokenJSONAPIMeta
rest_framework_jwt.serializers.RefreshJSONWebTokenSerializer.JSONAPIMeta = JWTRefreshJSONAPIMeta
rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.JSONAPIMeta = JWTVerifyJSONAPIMeta


customs = [rest_auth.serializers.TokenSerializer,
           rest_auth.serializers.JWTSerializer,
           rest_auth.serializers.UserDetailsSerializer,
           rest_auth.serializers.LoginSerializer,
           rest_auth.serializers.PasswordResetSerializer,
           rest_auth.serializers.PasswordResetConfirmSerializer,
           rest_auth.serializers.PasswordChangeSerializer,
           rest_auth.registration.serializers.RegisterSerializer,
           rest_auth.registration.serializers.VerifyEmailSerializer,
           rest_framework_jwt.serializers.JSONWebTokenSerializer,
           rest_framework_jwt.serializers.RefreshJSONWebTokenSerializer,
           rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer,
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
