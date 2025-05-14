"""Module defining the views for accountinfopage."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View

from loefsys.users.models import MemberDetails, Membership

from . import forms


class AccountinfoView(LoginRequiredMixin, View):
    """Account information view."""

    template_name = "accountinfopage.html"
    login_url = "signup_page"

    def get_account_info(self):
        """Get account information from the user."""
        user_info = {
            "name": self.request.user.display_name.strip(),
            "email": self.request.user.email,
            "phone_number": self.request.user.phone_number,
            "picture": self.request.user.picture,
            "groups": self.request.user.groups.all(),
        }


class AccountinfoeditView(LoginRequiredMixin, View):
    """Account information edit view."""

    template_name = "accountinfoeditpage.html"
    login_url = "signup_page"

    def get(self, request):
        """Handle the get request for the edit account information form."""
        user_form = forms.EditUserInfo(instance=self.request.user)
        member_list = MemberDetails.objects.filter(user=self.request.user)
        member_form = (
            forms.EditMemberInfo(instance=member_list[0])
            if member_list.count() > 0
            else None
        )
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "member_form": member_form},
        )

    def post(self, request):
        """Handle the post request for the edit account information form."""
        old_picture = self.request.user.picture

        user_form = forms.EditUserInfo(
            request.POST, request.FILES, instance=self.request.user
        )
        member_list = MemberDetails.objects.filter(user=self.request.user)
        member_form = (
            forms.EditMemberInfo(request.POST, request.FILES, instance=member_list[0])
            if member_list.count() > 0
            else None
        )
        if user_form.is_valid() and (member_form is None or member_form.is_valid()):
            if not user_form.cleaned_data.get("picture") and old_picture:
                # Delete the old profile picture from storage
                old_picture.delete(save=False)
            user_form.save()
            if member_form is not None:
                member_form.save()
            return redirect("accountinfo")
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "member_form": member_form},
        )