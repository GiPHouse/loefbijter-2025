"""Module defining the views for accountinfopage."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from loefsys.users.models import MemberDetails, Membership

from . import forms


def get_account_info(request):
    """Get account information from request."""
    user_info = {
        "name": request.user.display_name.strip(),
        "email": request.user.email,
        "phone_number": request.user.phone_number,
        "picture": request.user.picture,
        "groups": request.user.groups.all(),
    }

    member_info = []
    qs_member = MemberDetails.objects.filter(user=request.user)
    if qs_member.count() == 1:
        member = qs_member[0]
        qs_membership = Membership.objects.filter(member=member)
        if qs_membership.count() > 0:
            membership = qs_membership[::-1][0]
            member_info = {
                "birthday": member.birthday.__str__(),
                "show_birthday": member.show_birthday,
                "member_since": membership.start.__str__(),
                "activities": "",
            }
        else:
            raise Exception("Member has no membership")
    return user_info, member_info


@login_required(login_url="signup_page")
def accountinfoedit(request):
    """View for editing accountinformation."""
    if request.method == "POST":
        old_picture = request.user.picture
        user_form = forms.EditUserInfo(
            request.POST, request.FILES, instance=request.user
        )
        member_list = MemberDetails.objects.filter(user=request.user)
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
    else:
        user_form = forms.EditUserInfo(instance=request.user)
        member_list = MemberDetails.objects.filter(user=request.user)
        member_form = (
            forms.EditMemberInfo(instance=member_list[0])
            if member_list.count() > 0
            else None
        )

    return render(
        request,
        "accountinfoeditpage.html",
        {"user_form": user_form, "member_form": member_form},
    )


@login_required(login_url="signup_page")
def accountinfo(request):
    """View for loading the accountinformation page."""
    user_info, member_info = get_account_info(request)

    return render(
        request,
        "accountinfopage.html",
        {"user_info": user_info, "member_info": member_info},
    )
