import datetime
import jwt
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives


def generate_token(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        "asdfghjkhgfdsasdrtyu765rewsazxcvbnjkio908765432wsxcdfrt",
        algorithm="HS256",
    )
    return token


def my_mail(mail, otp):
    subject = "Password Reset OTP"
    msg = "Your one time password for resetting the password is as follows: <strong>{}</strong> <br>\nPlease do not share this with anyone.".format(
        otp
    )

    email = EmailMultiAlternatives(subject, msg, "33azharoddin@gmail.com", [mail])
    email.attach_alternative(msg, "text/html")

    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
        msg = 0

    return msg


def user_creation_mail(mail):
    subject = "Fairseed User Creation Email"
    msg = "Your Account is created with Email " + " " + mail + "."
    email = EmailMultiAlternatives(subject, msg, "33azharoddin@gmail.com", [mail])
    email.attach_alternative(msg, "text/html")  # Specify HTML content type
    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
        msg = 0

    return msg


from django.core.paginator import Paginator, EmptyPage


def paginate_model_data(model, serializer, request, filter_key=None):
    try:
        limit = max(int(request.GET.get("limit", 0)), 1)
        page_number = max(int(request.GET.get("page", 0)), 1)
        if filter_key:
            filter_value = request.GET.get(filter_key)
            data = model.objects.filter(**{filter_key: filter_value})
        else:
            data = model.objects.all()
        paginator = Paginator(data, limit)
        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
            return Response(
                {"error": True, "message": "Page not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serialized_data = serializer(current_page_data, many=True).data
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data,
        }
        return response_data
    except Exception as e:
        return Response(
            {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )


def paginate_data(model, serializer, request, data):
    try:
        limit = int(request.GET.get("limit", 1))
        page_number = int(request.GET.get("page", 1))
        data = data
        paginator = Paginator(data, limit)

        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
            return Response(
                {"error": True, "message": "Page not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            serialized_data = serializer(current_page_data, many=True).data
        except Exception as e:
            return Response(
                {"error": True, "message": f"Serialization error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data,
        }
        return response_data
    except Exception as e:
        return Response(
            {"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
