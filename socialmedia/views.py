from django.shortcuts import redirect, render
from django.http import JsonResponse

from django.conf import settings
from django.urls import reverse

from rest_framework.response import Response
from utilities.GM2 import GenericMethodsMixin

import requests

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET


class FacebookLoginView(GenericMethodsMixin):
    def get(self, request):
        facebook_oauth_url = "https://www.facebook.com/v12.0/dialog/oauth"
        redirect_uri = request.build_absolute_uri(reverse("facebook_callback"))

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": "demo",
            "scope": "email,user_posts,pages_manage_posts",
        }

        redirect_url = f"{facebook_oauth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

        return redirect(redirect_url)


class FacebookCallbackView(GenericMethodsMixin):
    def get(self, request):
        error = request.GET.get("error")
        error_reason = request.GET.get("error_reason")
        error_description = request.GET.get("error_description")

        if error:
            return Response(
                {
                    "error": error,
                    "error_reason": error_reason,
                    "error_description": error_description,
                },
                status=400,
            )

        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code:
            return JsonResponse(
                {"error": "Authorization failed or was denied"}, status=400
            )

        if state != "demo":
            return JsonResponse({"error": "Invalid state parameter"}, status=400)

        access_token = self.exchange_code_for_token(request, code)
        if access_token:
            request.thisUser.access_token = access_token
            return Response({"msg": "Token stored successfully."})
        return Response({"error": "Failed to exchange code for token"}, status=400)

    def exchange_code_for_token(request, code):
        url = "https://graph.facebook.com/v12.0/oauth/access_token"
        params = {
            "client_id": client_id,
            "redirect_uri": request.build_absolute_uri(reverse("facebook_callback")),
            "client_secret": client_secret,
            "code": code,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None


def get_long_lived_token(short_lived_token):
    url = "https://graph.facebook.com/v12.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "fb_exchange_token": short_lived_token,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch long-lived token"}


class FacebookPostsView(GenericMethodsMixin):
    def get(self, request, *args, **kwargs):
        url = "https://graph.facebook.com/v12.0/me/posts"
        params = {"access_token": request.user.access_token}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return Response(response.json(), status=200)
        return Response({"error": "Unable to fetch posts"}, status=response.status_code)


class CommentOnPostView(GenericMethodsMixin):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        message = request.data.get("message")
        if not post_id or not message:
            return Response({"error": "post_id and message are required"}, status=400)

        url = f"https://graph.facebook.com/v12.0/{post_id}/comments"
        data = {"message": message, "access_token": request.user.access_token}
        response = requests.post(url, data=data)
        return Response(response.json(), status=response.status_code)


class SharePostFacebookView(GenericMethodsMixin):
    def post(self, request, *args, **kwargs):
        message = request.data.get("message")
        if not message:
            return Response({"error": "message is required"}, status=400)

        url = "https://graph.facebook.com/v12.0/me/feed"
        data = {"message": message, "access_token": request.user.access_token}
        response = requests.post(url, data=data)
        return Response(response.json(), status=response.status_code)


class LikePostView(GenericMethodsMixin):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        if not post_id:
            return Response({"error": "post_id is required"}, status=400)

        url = f"https://graph.facebook.com/v12.0/{post_id}/likes"
        data = {"access_token": request.user.access_token}
        response = requests.post(url, data=data)
        return Response(response.json(), status=response.status_code)
