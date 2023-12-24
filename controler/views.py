from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from ai75589674.models import TrafficData
from controler.models import About_Page, Privacy_Edit
from django.contrib import messages


@login_required(login_url="Login")  # Adjust 'login' to the URL name of your login view
def dashboard(request):
    # View logic here
    total_new_users = (
        TrafficData.objects.filter(is_old_user=False)
        .values("ip_address")
        .distinct()
        .count()
    )
    total_old_users = (
        TrafficData.objects.filter(is_old_user=True)
        .values("ip_address")
        .distinct()
        .count()
    )
    total_users = TrafficData.objects.values("ip_address").distinct().count()
    content = {
        "total_new_users": total_new_users,
        "total_old_users": total_old_users,
        "total_users": total_users,
    }
    return render(request, "controler/index.html", content)


def login_view(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                return HttpResponse("Unauthorized person")
        else:
            return render(request, "controler/control_pages/singin.html")
    except Exception as e:
        return HttpResponse(e)


def about_view(request):
    try:
        if request.method == "POST":
            con = request.POST.get("aboutpage")
            title = request.POST.get("title")
            media = request.FILES.get("pfile")

            # Use Django forms for handling form data (not shown here)

            if not con:
                messages.warning(request, "Empty Content! Please write some content!")
                return redirect("a-bout")
            else:
                try:
                    about_page = About_Page.objects.get(id=1)
                except About_Page.DoesNotExist:  # Corrected the model name here
                    about_page = About_Page(title=title, content=con, image=media)

                about_page.content = con
                about_page.title = title
                about_page.image = media
                about_page.save()
                messages.success(request, "Changed Saved!")
                return redirect("a-bout")

        else:
            messages.error(request, "Bad Request!")
            return redirect("a-bout")
    except Exception as e:
        messages.error(request, e)
        return redirect("a-bout")


def privacy_view(request):
    try:
        if request.method == "POST":
            conp = request.POST.get("aboutpage")
            titlep = request.POST.get("title")
            mediap = request.FILES.get("pfile")
            # Use Django forms for handling form data (not shown here)

            if not conp:
                messages.warning(request, "Empty Content! Please write some content!")
                return redirect("Privacy")
            else:
                try:
                    privacy_page = Privacy_Edit.objects.get(id=1)
                except Privacy_Edit.DoesNotExist:
                    privacy_page = Privacy_Edit(
                        title=titlep, content=conp, image=mediap
                    )

                privacy_page.content = conp
                privacy_page.title = titlep
                privacy_page.image = mediap
                privacy_page.save()
                messages.success(request, "Changed Saved!")
                return redirect("Privacy")
        else:
            messages.error(request, "Bad Request!")
            return redirect("Privacy")
    except Exception as e:
        messages.error(request, e)
        return redirect("Privacy")


def about(request):
    try:
        m = About_Page.objects.first()
        return render(
            request, "controler/control_pages/about_edit.html", {"about_data": m}
        )
    except Exception as e:
        messages.error(request, e)
        return render(request, "controler/control_pages/about_edit.html")


def privacy(request):
    try:
        p = Privacy_Edit.objects.first()
        return render(
            request, "controler/control_pages/privacy_edit.html", {"privacy_data": p}
        )
    except Exception as e:
        messages.error(request, e)
        return render(request, "controler/control_pages/about_edit.html")


def logout_view(request):
    logout(request)
    return render(request, "controler/control_pages/singin.html")
