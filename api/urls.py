from rest_framework.routers import DefaultRouter
from djoser import views
from django.urls import include, path, re_path
from djoser import views, urls
import djoser.urls.authtoken
from django.contrib.auth import get_user_model

djoser.urls.authtoken.urlpatterns = [
    re_path(r"^token/login/?$", views.TokenCreateView.as_view(), name="login"),
    re_path(r"^token/logout/?$", views.TokenDestroyView.as_view(), name="logout"),
]


router = DefaultRouter()
router.register("users", views.UserViewSet)

User = get_user_model()

urls.urlpatterns = [
    # url(r"^me/?$", views.UserView.as_view(), name="user"),
    # url(r"^users/create/?$", views.UserCreateView.as_view(), name="user-create"),
    # url(r"^users/delete/?$", views.UserDeleteView.as_view(), name="user-delete"),
    # url(r"^users/activate/?$", views.ActivationView.as_view(), name="user-activate"),
    # re_path(
    #     r"^users/resend/?$",
    #     views.ResendActivationView.as_view(),
    #     name="user-activate-resend",
    # ),
    # url(
    #     r"^{0}/?$".format(User.USERNAME_FIELD),
    #     views.SetUsernameView.as_view(),
    #     name="set_username",
    # ),
    re_path(r"^password/?$", views.SetPasswordView.as_view(), name="set_password"),
    re_path(
        r"^password/reset/?$", views.PasswordResetView.as_view(), name="password_reset"
    ),
    re_path(
        r"^password/reset/confirm/?$",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # re_path(r"^$", views.RootView.as_view(), name="root"),
    re_path(r"^", include(router.urls)),
]

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
