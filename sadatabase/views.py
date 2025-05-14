from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.exceptions import FieldDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Application
from .models import ApplicationForm
import time
from datetime import date


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('/')

        return render(request, 'login.html', {'form': form})


def index_view(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    return render(request, 'index.html')


def home_view(request):

    if not request.user.is_authenticated:
        return redirect("/login")

    context = {}
    request.session["field_dict"] = ""
    whymap = {
        "Pre-Construction Phase": "pre",
        "During-Construction Phase": "during",
        "Post-Construction Phase": "post",
        "Additional Funding": "af",
        "Complete": "c"
    }

    if request.method == "POST":
        # small change
        if "moveID" in request.POST:
            obj_id = request.POST.get("moveID")
            cphase = request.POST.get("chosenPhase")
            if cphase != "Application Phase":
                app_obj = Application.objects.get(id=obj_id)
                app_obj.stage = whymap[cphase]
                app_obj.save()
        # detailed change
        elif "obj_id" in request.POST:
            obj_id = request.POST.get("obj_id")
            application = Application.objects.get(id=obj_id)
            form = ApplicationForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
        else:
            print("not submitting")

    # create stage lists
    phase_dict = {}
    phase_dict["pre"] = Application.objects.filter(stage="pre")
    phase_dict["during"] = Application.objects.filter(stage="during")
    phase_dict["post"] = Application.objects.filter(stage="post")
    phase_dict["af"] = Application.objects.filter(stage="af")
    context["phases"] = phase_dict
    context["phase_cats"] = ["Pre-Construction Phase", "During-Construction Phase", "Post-Construction Phase", "Additional Funding", "Complete"]

    return render(request, 'home.html', context)


def search(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    context = {}
    all_fields = ["Development_Name", "Development_Owner", "City", "County", "Total_Units", "MR_Units",
                                "Last_Updated"]
    context["search_fields"] = all_fields

    if request.method == "POST":

        # recreate search terms ui
        if request.session.get("field_dict", False):
            field_dict = request.session["field_dict"]
        else:
            field_dict = {}
        context["field_dict"] = field_dict

        kwargs = {}
        for field in all_fields:
            if field in request.POST:
                # first, update that field's value in the session information
                type_default_pair = field_dict[field]
                type_default_pair[1] = request.POST.get(field)
                request.session["field_dict"][field] = type_default_pair

                # get operator, if applicable, to add ">" or "<" to the query
                op = request.POST.get(f"{field}_op")
                if op == ">=":
                    kwargs[f"{field}__gte"] = request.POST.get(field)
                elif op == "<=":
                    kwargs[f"{field}__lte"] = request.POST.get(field)
                else:
                    kwargs[field] = request.POST.get(field)

        qobjs = Application.objects.filter(**kwargs)
        context["results"] = list(qobjs)

    else:
        request.session["field_dict"] = {}

    return render(request, 'search.html', context)


def detail(request):

    if not request.user.is_authenticated:
        return redirect("/login")
    app_id = request.GET.get("app_id")
    app_obj = Application.objects.get(id=app_id)
    return render(request, "detail.html", {"detail_obj": app_obj})


def edit(request):

    if not request.user.is_authenticated:
        return redirect("/login")

    app_id = request.GET.get("app_id")
    app_obj = Application.objects.get(id=app_id)
    form = ApplicationForm(instance=app_obj)
    return render(request, "detail_form.html", {"form": form, "app_id": app_id})


def change_terms(request):

    context = {}
    context["field_dict"] = request.session["field_dict"]

    return render(request, 'term_snippet.html', context)


def update_field_defaults(request):

    if not request.user.is_authenticated:
        return redirect("/login")

    # create field dictionary, from session or a new dict
    if request.session.get("field_dict", False):
        field_dict = request.session["field_dict"]
        fdkeys = field_dict.keys()
        valslist = request.GET.get('valslist', None)
        print(f"valslist: {valslist}")
        if valslist:
            termsplit = valslist.split("&")
            for pair in termsplit:
                keyval = pair.split("=")
                # if the key, or field name exists in field_dict, update the field with the value
                if keyval[0] in fdkeys:
                    # grab the [type, default] list from the field dict
                    dvals = field_dict[keyval[0]]
                    # replace the default with the new value from valslist
                    dvals[1] = str(keyval[1]).replace("+", " ")
                    field_dict[keyval[0]] = dvals

            request.session["field_dict"] = field_dict
            out = request.session["field_dict"]
    else:
        field_dict = {}

    # make field readable by database
    field = request.GET.get("field")
    field = field.replace(" ", "_")

    # update field dictionary with new field instructions
    if field in field_dict.keys():
        # remove old entry and replace
        del field_dict[field]
        request.session["field_dict"] = field_dict
    # or add new value, get information from database
    else:
        try:
            # get field type, and map type to default
            ftype = Application._meta.get_field(field).get_internal_type()
            ftype = ftype[0:4].lower()
            default = ""
            if ftype == "inte":
                default = 0
            field_dict[field] = [ftype, default]
            request.session["field_dict"] = field_dict
        except FieldDoesNotExist:
            print("not a field")

    return HttpResponse("Success!")


def save_edits(request):

    if request.user.is_authenticated and request.method == "POST":

        obj_id = request.POST.get("obj_id")
        application = Application.objects.get(id=obj_id)
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            changes = form.changed_data
            changed_obj = form.save(commit=False)
            changed_obj.save(update_fields=changes)

        return JsonResponse({"id": obj_id, "date": date.today()})

    else:
        return redirect("/login")
