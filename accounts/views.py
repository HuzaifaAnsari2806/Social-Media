from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from random import randint

from utilities.GM2 import GenericMethodsMixin
from utilities.services import generate_token, my_mail

from .models import User, Profile

from .serializers import (
    UserSerializer,
    UserSerializer1,
    ChangePasswordSerializer,
    ProfileSerializer,
)


class UserApi(GenericMethodsMixin):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"


class RegisterUserApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                print(request.data)
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    subject = "User Creation Email"
                    message = (
                        "Your Account is created with Email " + " " + user.email + "."
                    )
                    # send_email_async(subject,message,[user.email])
                    return Response(
                        {
                            "message": "User Created Successfully",
                            "data": UserSerializer1(user).data,
                        },
                        status=status.HTTP_201_CREATED,
                    )
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            # Generate Token
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response(
                    {"error": False, "data": "User Not Exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            token = generate_token(user.email)
            password_match = check_password(password, user.password)
            serializer = UserSerializer1(user)
            data = {
                "error": False,
                "message": "User logged in successfully",
                "user_info": serializer.data,
                "token": token,
            }
            if password == user.password or password_match:
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"error": True, "message": "Password is not Matched"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ChangePasswordSerializer(
                data=request.data, context={"request": self.request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"Success": "Password updated successfully"},
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ForgotPasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            mail = request.data.get("email")
            print("in user", mail)
            user = User.objects.get(email=mail)
            print(user)
            otp = randint(1000, 9999)
            res = my_mail(mail, otp)
            if res == 1:
                return Response(
                    data={
                        "Success": "Otp Mail sent successfully to " + mail,
                        "OTP": str(otp),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data={"error": True, "message": "Error sending Mail"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                data={"error": True, "message": "User Email Does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateUserAPI(APIView):
    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.thisUser)
            serializer = UserSerializer1(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "error": False,
                        "message": "User updated successfully",
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetPasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                return Response(
                    data={
                        "Success": "Password for Email "
                        + str(user)
                        + " reset successful"
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(data={"Error": "Email does not exists"})
        except Exception as e:
            return Response(
                {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(GenericMethodsMixin):
    model = Profile
    serializer_class = ProfileSerializer
    lookup_field = "id"
