import simplejson
from MySQLdb._exceptions import IntegrityError
from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404, _get_queryset
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, time, timedelta
from django.views.decorators import gzip
from calendar import *
import urllib.request
import requests
import cv2
import numpy as np
from .camera import VideoCamera


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                messages.success(request, f"You are now logged in as {request.user.username}")
                return redirect('/Dashboard')
            else:
                pass

        else:
            pass
    form = AuthenticationForm()
    return render(request, "cdpapp/b1.html", context={"form": form})


def register(request):
    if request.method == 'POST':
        return redirect('/Dashboard')
    else:
        return render(request, 'cdpapp/register.html')



def getNavigation(request):
    activeuser = Appuser.objects.get(user=request.user)
    print(activeuser)
    activeuser = Appuser.objects.get(user=request.user)
    print(activeuser)
    # activeuser = 12
    query = ' select sm.* ' \
            ' from Roledetail rd ' \
            ' inner join Submenu sm on sm.id = rd.submenu_id ' \
            ' inner join Role r on r.id = rd.role_id ' \
            ' inner join Appuser au on au.role_id = r.id ' \
            ' inner join auth_user atu on atu.id = au.user_id ' \
            ' inner join Menu m on m.id = sm.menu_id ' \
            ' where atu.username = "%s" AND sm.is_deleted = "N" ' % (activeuser)
    print(query)
    submenusvalue = Submenu.objects.raw(query)
    print(Submenu.objects.all())

    return submenusvalue


@csrf_exempt
def get_cameras(request):
    cameras = Camera.objects.filter(cluster_id=request.POST.get('cluster_id', ''))
    camera_obj = serializers.serialize('python', cameras)
    return JsonResponse(camera_obj, safe=False)


@csrf_exempt
def get_clusters(request):
    clusters = Cluster.objects.filter(customer_id=request.POST.get('customer_id', ''))
    cluster_obj = serializers.serialize('python', clusters)
    return JsonResponse(cluster_obj, safe=False)


@csrf_exempt
def get_agents(request):
    agents = Agent.objects.filter(customer_id=request.POST.get('customer_id', ''))
    agent_obj = serializers.serialize('python', agents)
    return JsonResponse(agent_obj, safe=False)


@csrf_exempt
def customer_validation(request):

    present = 0
    is_present = Cust_org.objects.filter(cust_org=request.POST.get('customer', ''))

    if is_present:
        present = 1
    else:
        present = 0

    data = {
        'present':present
    }

    return JsonResponse(data)

# ********************        DASHBOARD         **************#


def dashboard(request):
    (multiple_people_today, mobile_detected_today, unidentified_person_today, camera_tampered_today) = (0, 0, 0, 0)
    (multiple_people, mobile_detected, unidentified_person, camera_tampered) = (0, 0, 0, 0)

    delta = timedelta(days=1)
    start_date = date(2020, 3, 27)
    end_date = date.today()

    start = start_date
    end = end_date

    categories = ['Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']

    while start <= end:

        for category in categories:
            incidents = Incident.objects.filter(incident_date=start, category=category)
            total = 0

            for incident in incidents:
                total += 1

            if category == 'Camera Tampered':
                camera_tampered += total
            elif category == 'Mobile Detected':
                mobile_detected += total
            elif category == 'Multiple People':
                multiple_people += total
            else :
                unidentified_person += total

        start += delta


    today = date.today()

    for category in categories:
        incidents = Incident.objects.filter(incident_date=today, category=category)
        cur = 0

        for incident in incidents:
            cur += 1

        if category == 'Camera Tampered':
            camera_tampered_today += cur
        elif category == 'Mobile Detected':
            mobile_detected_today += cur
        elif category == 'Multiple People':
            multiple_people_today += cur
        else :
            unidentified_person_today += cur




    context = {
        'multiple_people_today': multiple_people_today,
        'mobile_detected_today': mobile_detected_today,
        'unidentified_person_today': unidentified_person_today,
        'camera_tampered_today': camera_tampered_today,
        'multiple_people': multiple_people,
        'mobile_detected': mobile_detected,
        'unidentified_person': unidentified_person,
        'camera_tampered': camera_tampered,
        'submenusvalue': getNavigation(request)
    }

    return render(request, 'cdpapp/main dashboard.html', context=context)


def visitor_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/visitors-count.html', {'clusters': clusters, 'cameras': cameras, 'customers': customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'cdpapp/visitors-count.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def vehicle_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/vehicle-count.html', {'clusters': clusters, 'cameras': cameras, 'customers': customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/vehicle-count.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def age_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/age_detail.html', {'clusters': clusters, 'cameras': cameras,  'customers':customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'cdpapp/age_detail.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def gender_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/gender_detail.html', {'clusters': clusters, 'cameras': cameras, 'customers':customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'cdpapp/gender_detail.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def repeat_vehicle_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/repeat-vehicle.html', {'clusters': clusters,'customers':customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    return render(request, 'cdpapp/repeat-vehicle.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def repeat_visitor_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/repeat-visitors.html', {'clusters': clusters, 'cameras': cameras, 'customers':customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    return render(request, 'cdpapp/repeat-visitors.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})















def camera_tampering_details_dashboard(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    categories = [ 'Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))
    return render(request, 'cdpapp/cameratampering_details.html', {'agents':agents, 'categories':categories, 'customers':customers, 'submenusvalue': getNavigation(request)})



def mobile_detected_details_dashboard(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    categories = [ 'Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))
    return render(request, 'cdpapp/mobiledetected_details.html', {'agents':agents, 'categories':categories, 'customers':customers, 'submenusvalue': getNavigation(request)})



def multiple_people_details_dashboard(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    categories = ['Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))
    return render(request, 'cdpapp/multiplepeople_details.html', {'agents':agents, 'categories':categories, 'customers':customers, 'submenusvalue': getNavigation(request)})




def unidentified_person_details_dashboard(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    categories = ['Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))
    return render(request, 'cdpapp/unidentifiedperson_details.html', {'agents':agents, 'categories':categories, 'customers':customers, 'submenusvalue': getNavigation(request)})




















def profile(request):
    if request.method == 'POST':
        activeuser = Appuser.objects.get(user=request.user)
        form1 = ProfileForm(request.POST, instance=request.user)
        form2 = ProfileForm1(request.POST, request.FILES, instance=request.user)
        if form1.is_valid() and form2.is_valid():
            userform = form1.save()
            # customeform = form2.save()
            # customeform.user = userform
            # customeform.save()
            print(request.FILES)
            data = form2.cleaned_data

            print(data)
            mobile = data["mobile"]

            image = data["profile_pic"]
            # profile_pic = 'profile_image/' + str(image)
            # print(profile_pic)

            if image != None:
                Appuser.objects.filter(user=request.user).update(mobile=mobile, profile_pic=image)
                print(image)
                print(image.name)
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)

                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
            else:
                Appuser.objects.filter(user=request.user).update(mobile=mobile)

            messages.success(request, f"Profile Updated Successfully")
            return redirect('/Profile')
        else:
            messages.error(request, form2.errors)
            return redirect('/Profile')

    else:
        form1 = ProfileForm(instance=request.user)
        form2 = ProfileForm1(instance=request.user)
        app_user = Appuser.objects.get(user=request.user)
        return render(request, 'cdpapp/main-Profile.html', {'form1': form1, 'form2': form2, 'app_user': app_user, 'submenusvalue': getNavigation(request)})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/Profile')


    else:
        form = PasswordChangeCustomForm(request.user)
        app_user = Appuser.objects.get(user=request.user)
    return render(request, 'cdpapp/change password.html', {'form': form, 'app_user': app_user, 'submenusvalue': getNavigation(request)})








# *********************  REPORT  ******************************




def count_visitors(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report visitors.html', {'customers': customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report visitors.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def age_gender(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report age-gender count.html', {'customers': customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report age-gender count.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def count_vehicles(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report vehicle.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report vehicle.html', {'clusters': clusters})


def repeat_vehicles_count(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report rvehicle.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report rvehicle.html', {'clusters': clusters})


def repeat_visitors_count(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report rvisitors.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report rvisitors.html', {'clusters': clusters})


def camera_tampering(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report camera tempering.html', {'customers': customers, 'submenusvalue': getNavigation(request)})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'cdpapp/report camera tempering.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})





# *********************  REPORT - DETAILS ******************************


@csrf_exempt
def visitor_details(request):
    visitors = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera), str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        people = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            people = data1[i][str(start)][str(camera)]
            dates.append(start)
            visitors.append(people)
            # visitors.append({"date" : start,"people": people})
            start += delta
            i += 1

    print(visitors)
    print()

    data = {
        'dates': dates,
        'visitors': visitors
    }

    return JsonResponse(data)


@csrf_exempt
def age_details(request):
    dates = []
    data_male = []
    data_female = []

    if request.is_ajax():
        x = request.POST.get('startdate','')
        y = request.POST.get('enddate','')
        camera = request.POST.get('camera','')

        print(x)
        print(camera)

        (month_start, date_start, month_end, date_end) = (0,0,0,0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if(len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)


        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if(len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)


        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate
        delta = timedelta(days=1)

        while start<=end:
            url = "http://3.93.246.89:8000/GetData?chartType=Gender&cameraName={}&startDate={}&endDate={}".format(str(camera), str(start), str(start))
            response = requests.get(url)
            data1 = response.json()

            data_male.append(data1[0][str(camera)]['Male'])
            data_female.append(data1[0][str(camera)]['Female'])


            dates.append(start)
            start += delta

    data = {'dates': dates, 'data_male': data_male, 'data_female': data_female}
    print(data_female)
    print(data_male)

    return JsonResponse(data)




















@csrf_exempt
def vehicle_details(request):
    vehicles = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=Vehicle&cameraName=&startDate={}&endDate={}".format(str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        vehicle = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            vehicle = data1[i][str(start)]['B3-Parking']
            dates.append(start)
            vehicles.append(vehicle)
            start += delta
            i += 1

    print(vehicles)
    print()

    data = {
        'dates': dates,
        'vehicles': vehicles
    }

    return JsonResponse(data)


@csrf_exempt
def repeat_vehicle_details(request):
    repeatvehicles = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=Vehicle&cameraName=&startDate={}&endDate={}".format(str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        vehicle = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            vehicle = data1[i][str(start)]['B3-Parking']
            dates.append(start)
            repeatvehicles.append(vehicle)
            start += delta
            i += 1

    print(repeatvehicles)
    print()

    data = {
        'dates': dates,
        'repeatvehicles': repeatvehicles
    }

    return JsonResponse(data)



@csrf_exempt
def repeat_visitor_details(request):
    repeatvisitors = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera), str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        people = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            people = data1[i][str(start)][str(camera)]
            dates.append(start)
            repeatvisitors.append(people)
            # visitors.append({"date" : start,"people": people})
            start += delta
            i += 1

    print(repeatvisitors)
    print()

    data = {
        'dates': dates,
        'repeatvisitors': repeatvisitors
    }

    return JsonResponse(data)



@csrf_exempt
def camera_tampering_details(request):
    pass


















def agent_list(request):
    activeuser = Appuser.objects.get(user=request.user)
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    agent_list = Agent.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(agent_list, 5)

    try:
        agents = paginator.page(page)
    except PageNotAnInteger:
        agents = paginator.page(1)
    except EmptyPage:
        agents = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/agent table.html', {'agents': agents, 'submenusvalue': getNavigation(request)})


def add_agent(request):
    if request.method == 'POST':
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        fname = request.POST['f_name']
        lname = request.POST['l_name']
        mac_id = request.POST['mac_id']
        created_by = request.user.username
        modified_by = request.user.username
        lead = request.POST['lead']
        manager = request.POST['manager']
        u = User.objects.get(first_name=manager)
        a = Appuser.objects.get(user=u)
        user = User.objects.get(first_name=lead)
        appuser = Appuser.objects.get(user=user)
        new_agent = Agent(fname=fname, lname=lname, created_by=created_by, modified_by=modified_by,customer=cust_inst, lead=appuser, manager_id=a.pk, mac_id=mac_id)
        new_agent.save()
        return redirect('/Admin/Agent')
    else:
        if request.user.is_superuser:
            leads = Appuser.objects.filter(designation='Lead')
            managers = Appuser.objects.filter(designation='Manager')
            return render(request, 'cdpapp/agent.html', {'leads':leads, 'managers':managers, 'submenusvalue': getNavigation(request)})
        else:
            activeuser = Appuser.objects.get(user=request.user)
            cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
            leads = Appuser.objects.filter(customer=cust_inst, designation='Lead')
            managers = Appuser.objects.filter(customer=cust_inst, designation='Manager')
            return render(request, 'cdpapp/agent.html', {'leads':leads, 'managers':managers, 'submenusvalue': getNavigation(request)})


def edit_agent(request, agent_id):
    print(agent_id)
    agent = Agent.objects.get(pk=agent_id)
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            return redirect('/Admin/Agent')
    else:
        form = AgentForm(instance=agent)
        return render(request, 'cdpapp/agent_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, pk=agent_id)
    agent.is_deleted = 'Y'
    agent.save()
    return redirect('/Admin/Agent')



def mysql_query(request):
    activeuser = Appuser.objects.get(user=request.user)
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    query = "select ag.* from Agent ag inner join Incident ic on ag.id = ic.agent_id  where ag.customer_id ={}".format(cust_inst.pk)
    objs = Agent.objects.raw(query)
    print(objs)
    return  objs


# ************  NOTIFICATIONS *********************


def notification_list(request):
    activeuser = Appuser.objects.get(user=request.user)
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))
    print(incident_list)

    page = request.GET.get('page', 1)
    paginator = Paginator(incident_list, 5)

    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    except EmptyPage:
        incidents = paginator.page(paginator.num_pages)



    return render(request, 'cdpapp/notification_list.html', {"incidents":incidents, 'submenusvalue': getNavigation(request)})


def current_notifications(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))



    return render(request, 'cdpapp/notification_list_current.html', {'agents':agents, 'customers':customers, 'submenusvalue': getNavigation(request)})


def old_notifications(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = list(Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on"))


    return render(request, 'cdpapp/notification_list_old.html', {'agents':agents, 'customers':customers, 'submenusvalue': getNavigation(request)})



def view_notification(request, notification_id):
    notification = Incident.objects.get(id=notification_id)
    notification.notification_status = 'Viewed'
    notification.save()
    return render(request, 'cdpapp/notification_detail.html', {"notification":notification, 'submenusvalue': getNavigation(request)})










def reports(request):
    customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
    cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
    categories = ['All', 'Camera Tampered', 'Mobile Detected', 'Multiple People', 'Unidentified Person']
    agents = Agent.objects.filter(customer=cust_inst)
    agent_ids = set(map(lambda x: x.id, agents))
    incident_list = Incident.objects.filter(id__in=agent_ids).order_by("-created_on", "-modified_on")
    return render(request, 'cdpapp/reports.html', {'agents':agents, 'categories':categories, 'customers':customers, 'submenusvalue': getNavigation(request)})



@csrf_exempt
def report_data(request):
    incident_data = []
    dates = []
    macids = []
    agent_data = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        agentid = request.POST.get('agent_id', '')
        category = request.POST.get('category', '')
        print(x)
        print(agentid)
        print(category)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start)

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end)

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)



        delta = timedelta(days=1)

        while start <= end :

            if category == 'All' and agentid == 'All':
                incidents = Incident.objects.filter(incident_date=start)
            elif category == 'All':
                incidents = Incident.objects.filter(incident_date=start, agent_id=agentid)
            elif agentid == 'All':
                incidents = Incident.objects.filter(incident_date=start, category=category)
            else:
                incidents = Incident.objects.filter(incident_date=start, category=category, agent_id=agentid)


            for incident in incidents:
                incident_data.append(incident.category)
                dates.append(start)
                macids.append(incident.mac_id)
                agent_data.append(incident.agent.fname)


            start += delta

    print()

    data = {
        'dates': dates,
        'macids' : macids,
        'agent_data' : agent_data,
        'incident_data' : incident_data
    }

    return JsonResponse(data)





@csrf_exempt
def current_notifications_data(request):
    incident_data = []
    ids = []
    dates = []
    macids = []
    agent_data = []

    if request.is_ajax():
        agentid = request.POST.get('agent_id', '')



        if request.user.is_superuser:
            customer_id = request.POST.get('customer_id', '')
            cust_inst = Cust_org.objects.get(id=customer_id)
            if agentid == 'All':
                agents = Agent.objects.filter(customer=cust_inst)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Open').order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    incident_data.append(incident.category)
                    ids.append(incident.id)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
            else:
                agents = Agent.objects.filter(customer=cust_inst, id=agentid)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Open').order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(int(incident.id))
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
        else:
            activeuser = Appuser.objects.get(user=request.user)
            cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
            if agentid == 'All':
                agents = Agent.objects.filter(customer=cust_inst)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Open').order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(incident.id)
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
            else:
                agents = Agent.objects.filter(customer=cust_inst, id=agentid)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Open').order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(incident.id)
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)


    data = {
        'ids': ids,
        'dates': dates,
        'macids' : macids,
        'agent_data' : agent_data,
        'incident_data' : incident_data
    }

    return JsonResponse(data)



@csrf_exempt
def old_notifications_data(request):
    incident_data = []
    ids = []
    dates = []
    macids = []
    agent_data = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        agentid = request.POST.get('agent_id', '')


        (month_start, date_start) = (0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start)

        date_start = int(temp_date_start)


        startdate = date(2020, month_start, date_start)

        start = startdate




        if request.user.is_superuser:
            customer_id = request.POST.get('customer_id', '')
            cust_inst = Cust_org.objects.get(id=customer_id)
            if agentid == 'All':
                agents = Agent.objects.filter(customer=cust_inst)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Viewed', incident_date=start).order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    incident_data.append(incident.category)
                    ids.append(incident.id)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
            else:
                agents = Agent.objects.filter(customer=cust_inst, id=agentid)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Viewed', incident_date=start).order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(incident.id)
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
        else:
            activeuser = Appuser.objects.get(user=request.user)
            cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
            if agentid == 'All':
                agents = Agent.objects.filter(customer=cust_inst)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Viewed', incident_date=start).order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(incident.id)
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)
            else:
                agents = Agent.objects.filter(customer=cust_inst, id=agentid)
                agent_ids = set(map(lambda x: x.id, agents))
                incident_list = Incident.objects.filter(id__in=agent_ids, notification_status='Viewed', incident_date=start).order_by("-created_on", "-modified_on")

                for incident in incident_list:
                    ids.append(incident.id)
                    incident_data.append(incident.category)
                    dates.append(incident.incident_date)
                    macids.append(incident.mac_id)
                    agent_data.append(incident.agent.fname)


    data = {
        'ids': ids,
        'dates': dates,
        'macids' : macids,
        'agent_data' : agent_data,
        'incident_data' : incident_data
    }

    return JsonResponse(data)





def user_list(request):
    if request.user.is_superuser:  # for super admin we want to show all the customers list
        user_list = Appuser.objects.filter(is_deleted='N', is_superuser='N').order_by("-created_on", "-modified_on")
    else:
        activeuser = Appuser.objects.get(user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
        cust_inst = Cust_org.objects.filter(cust_org=activeuser.customer)[0]
        user_list = Appuser.objects.filter(is_deleted='N', is_superuser='N', customer=cust_inst).order_by("-created_on", "-modified_on")

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/userlist.html', {'users': users, 'submenusvalue': getNavigation(request)})


def add_user(request):
    if request.method == 'POST':
        designation = request.POST['desig']
        user_form = UserForm(request.POST)
        if request.user.is_superuser:
            super_admin_user_form = SuperAdminUserForm(request.POST)
            if user_form.is_valid() and super_admin_user_form.is_valid():
                user = user_form.save()

                user.save()
                app_user = super_admin_user_form.save(commit=False)
                app_user.user = user
                app_user.created_by = 'Shyena Tech'
                app_user.modified_by = 'Shyena Tech'
                app_user.designation = designation
                app_user.save()
                messages.success(request, 'User saved successfully.')
                return redirect('/Admin/User')
            else:
                print(user_form.errors)
                print(super_admin_user_form.errors)
                messages.error(request, user_form.errors)
                messages.error(request, super_admin_user_form.errors)
                return redirect('/Admin/User/Add_User')


        else:  # ther user is not a superuser
            other_user_form = OtherUserForm(request.POST)
            if user_form.is_valid() and other_user_form.is_valid():
                user = user_form.save()

                user.save()

                activeuser = Appuser.objects.get(user=request.user)
                cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)

                app_user = other_user_form.save(commit=False)
                app_user.customer = cust_inst
                app_user.user = user
                app_user.designation = designation
                app_user.created_by = request.user.username
                app_user.modified_by = request.user.username
                app_user.save()
                messages.success(request, 'User saved successfully.')
                return redirect('/Admin/User')
            else:
                print(user_form.errors)
                print(other_user_form.errors)
                messages.error(request, user_form.errors)
                messages.error(request, other_user_form.errors)
                return redirect('/Admin/User/Add_User')

    else:
        roles = Role.objects.filter(is_deleted='N')
        customers = Cust_org.objects.filter(is_deleted='N')
        user_form = UserForm()
        super_admin_user_form = SuperAdminUserForm()
        other_user_form = OtherUserForm()
        return render(request, 'cdpapp/add user.html',
                      {'roles': roles, 'customers': customers, 'user_form': user_form, 'super_admin_user_form': super_admin_user_form,
                       'other_user_form': other_user_form, 'submenusvalue': getNavigation(request)})


def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form1 = EditUserForm1(request.POST, instance=user)
        form2 = EditUserForm2(request.POST, instance=user)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/Admin/User')
    else:
        form1 = EditUserForm1(instance=user)
        form2 = EditUserForm2(instance=user)
        return render(request, 'cdpapp/user_edit.html', {'form1': form1, 'form2':form2, 'submenusvalue': getNavigation(request)})


def delete_user(request, user_id):
    user = get_object_or_404(Appuser, pk=user_id)
    user.is_deleted = 'Y'
    user.save()
    return redirect('/Admin/User')


def authorization(request):
    return render(request, 'cdpapp/roles.html')




def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def view_feed(request):
    if request.method == 'POST':

        camera = request.POST.get('camera')
        cluster = request.POST.get('clust')

        print(cluster)

        try:
            camera_inst = Camera.objects.get(camname=camera)
        except Camera.DoesNotExist:
            messages.error(request, 'Select a Camera')
            clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
            return render(request, 'cdpapp/view_feed.html', {'clusters': clusters})

        id = camera_inst.pk

        ip = camera_inst.camip
        ip = str(ip)

        print(ip)
        print(camera)
        print(cluster)

        # cap = cv2.VideoCapture('rtsp://Aditya:1234@192.168.1.101:7777')
        # cap = cv2.VideoCapture(ip)

        opt = request.POST.get('submit')
        if opt == 'view':

            try:
                return StreamingHttpResponse(gen(VideoCamera(ip)), content_type="multipart/x-mixed-replace;boundary=frame")
            except HttpResponseServerError as e:
                print("aborted")

            '''while (True):

                ret, frame = cap.read()
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()'''

        elif opt == 'stop':
            pass
    else:

        if request.user.is_superuser:
            clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
            cameras = Camera.objects.filter(is_deleted='N')
            return render(request, 'cdpapp/view_feed.html', {'clusters': clusters, 'cameras': cameras})
        else:
            clusters = Cluster.objects.filter(is_deleted='N', created_by=request.user.username).order_by("-created_on", "-modified_on")
            cluster_ids = set(map(lambda x: x.pk, clusters))
            cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
            return render(request, 'cdpapp/view_feed.html', {'clusters': clusters, 'cameras': cameras})


def subscription(request):
    return render(request, 'cdpapp/subscription.html', {'submenusvalue': getNavigation(request)})


def subscription_plan(request):
    return render(request, 'cdpapp/subscription plan.html', {'submenusvalue': getNavigation(request)})


def summary(request):
    return render(request, 'cdpapp/summary.html', {'submenusvalue': getNavigation(request)})


# ****************************       Super-Admin   *************************


def algo_list(request):
    algo_list = Algo_master.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(algo_list, 5)

    try:
        algorithms = paginator.page(page)
    except PageNotAnInteger:
        algorithms = paginator.page(1)
    except EmptyPage:
        algorithms = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/algorithm table.html', {'algorithms': algorithms, 'submenusvalue': getNavigation(request)})


def add_algo(request):
    if request.method == 'POST':
        algo = request.POST['algo_name']
        algo_desc = request.POST['descr']
        # created_by = request.user.username
        # modified_by = request.user.username
        new_algo = Algo_master(algo=algo, algo_desc=algo_desc)
        new_algo.save()
        return redirect('/Super-Admin/algorithms')
    else:
        return render(request, 'cdpapp/algorithm.html', {'submenusvalue': getNavigation(request)})


def edit_algo(request, algo_id):
    algo = Algo_master.objects.get(pk=algo_id)
    if request.method == 'POST':
        form = AlgoithmForm(request.POST, instance=algo)
        if form.is_valid():
            form.save()
            return redirect('/Super-Admin/algorithms')
    else:
        form = AlgoithmForm(instance=algo)
        return render(request, 'cdpapp/algo_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_algo(request, algo_id):
    algo = get_object_or_404(Algo_master, pk=algo_id)
    algo.is_deleted = 'Y'
    algo.save()
    return redirect('/Super-Admin/algorithms')


def customer_list(request):
    customer_list = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(customer_list, 5)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/customer table.html', {'customers': customers, 'submenusvalue': getNavigation(request)})


def add_customer(request):
    if request.method == 'POST':
        if IntegrityError:
            bills = Bill_plan.objects.filter(is_deleted='N')
            messages.error(request, "Customer Organization already Exists.")

            return render(request, 'cdpapp/customer.html', {'bills': bills, 'submenusvalue': getNavigation(request)})

        cust_org = request.POST['cust_org']
        cust_org_acro = request.POST['cust_acro']
        created_by = request.user.username
        modified_by = request.user.username
        bill_plan = request.POST['bill']
        status = request.POST['status']
        date_str = request.POST['onboard']

        bill_plan_inst = Bill_plan.objects.get(billplan=bill_plan)
        temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_customer = Cust_org(cust_org=cust_org, cust_org_acro=cust_org_acro, status=status, bill_plan=bill_plan_inst, onboard_date=temp_date, created_by=created_by, modified_by=modified_by)
        new_customer.save()
        return redirect('/Super-Admin/Customers')
    else:
        bills = Bill_plan.objects.filter(is_deleted='N')
        '''
        try:
            last_inserted = Cust_org.objects.order_by('-id')[0]
            customerid = last_inserted.id
        except IndexError:
            customerid = 1
        except Cust_org.DoesNotExist:
            customerid = 1'''

        return render(request, 'cdpapp/customer.html', {'bills': bills, 'submenusvalue': getNavigation(request)})


def edit_customer(request, customer_id):
    customer = Cust_org.objects.get(pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/Super-Admin/Customers')
    else:
        form = CustomerForm(instance=customer)
        return render(request, 'cdpapp/customer_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_customer(request, customer_id):
    customer = get_object_or_404(Cust_org, pk=customer_id)
    customer.is_deleted = 'Y'
    customer.save()
    return redirect('/Super-Admin/Customers')


def bill_list(request):
    bill_list = Bill_plan.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(bill_list, 5)

    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/Bill Plan Table.html', {'bills': bills, 'submenusvalue': getNavigation(request)})


def add_bill(request):
    if request.method == 'POST':
        billplan = request.POST['billplan']
        billplan_cd = request.POST['billplan_cd']
        created_by = request.user.username
        modified_by = request.user.username
        new_bill = Bill_plan(billplan=billplan, billplan_cd=billplan_cd, created_by=created_by, modified_by=modified_by)
        new_bill.save()
        return redirect('/Super-Admin/Bill-Plan')
    else:
        return render(request, 'cdpapp/BillPlan.html', {'submenusvalue': getNavigation(request)})


def edit_bill(request, bill_id):
    bill = Bill_plan.objects.get(pk=bill_id)
    if request.method == 'POST':
        form = BillPlanForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('/Super-Admin/Bill-Plan')
    else:
        form = BillPlanForm(instance=bill)
        return render(request, 'cdpapp/bill_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill_plan, pk=bill_id)
    bill.is_deleted = 'Y'
    bill.save()
    return redirect('/Super-Admin/Bill-Plan')


def menu_list(request):
    menu_list = Menu.objects.filter(is_deleted='N').order_by("menu","-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(menu_list, 10)

    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/Menu List.html', {'menus': menus, 'submenusvalue': getNavigation(request)})


def add_menu(request):
    if request.method == 'POST':
        menu = request.POST['menu']
        created_by = request.user.username
        modified_by = request.user.username
        new_menu = Menu(menu=menu, created_by=created_by, modified_by=modified_by)
        new_menu.save()
        return redirect('/Super-Admin/Menu')
    else:
        return render(request, 'cdpapp/Menu.html', {'submenusvalue': getNavigation(request)})


def edit_menu(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('/Super-Admin/Menu')
    else:
        form = MenuForm(instance=menu)
        return render(request, 'cdpapp/menu_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.is_deleted = 'Y'
    menu.save()
    return redirect('/Super-Admin/Menu')


def submenu_list(request):
    menu_list = Menu.objects.filter(is_deleted='N').order_by("menu","-created_on", "-modified_on")
    submenus = Submenu.objects.filter(is_deleted='N')
    page = request.GET.get('page', 1)
    paginator = Paginator(menu_list, 3)

    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/Sub Menu List.html', {'menus': menus, 'submenus' : submenus, 'submenusvalue': getNavigation(request)})






def add_submenu(request):
    if request.method == 'POST':
        submenu = request.POST['submenu']
        menu = request.POST['menu']
        created_by = request.user.username
        modified_by = request.user.username
        menu_inst = Menu.objects.get(menu=menu)
        new_submenu = Submenu(submenu=submenu, menu=menu_inst, created_by=created_by, modified_by=modified_by)
        new_submenu.save()
        return redirect('/Super-Admin/SubMenu')
    else:
        menus = Menu.objects.filter(is_deleted='N')
        return render(request, 'cdpapp/SubMenu.html', {'menus': menus, 'submenusvalue': getNavigation(request)})


def edit_submenu(request, submenu_id):
    submenu = Submenu.objects.get(pk=submenu_id)
    if request.method == 'POST':
        form = SubMenuForm(request.POST, instance=submenu)
        if form.is_valid():
            form.save()
            return redirect('/Super-Admin/SubMenu')
    else:
        form = SubMenuForm(instance=submenu)
        return render(request, 'cdpapp/submenu_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_submenu(request, submenu_id):
    submenu = get_object_or_404(Submenu, pk=submenu_id)
    submenu.is_deleted = 'Y'
    submenu.save()
    return redirect('/Super-Admin/SubMenu')


# ************************  Admin  *******************************


def role_list(request):
    role_list = Role.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(role_list, 5)

    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/Role List.html', {'roles': roles, 'submenusvalue': getNavigation(request)})


def add_role(request):
    if request.method == 'POST':
        role = request.POST['role']
        role_desc = request.POST['role_desc']
        created_by = request.user.username
        modified_by = request.user.username

        new_role = Role(role=role, role_desc=role_desc, created_by=created_by, modified_by=modified_by)
        new_role.save()

        List = []

        for menu in Menu.objects.all():  # Fetching the selected checkboxes' values
            if menu.is_deleted == 'N':
                x = str(menu) + '[]'
                r = request.POST.getlist(x)
                # print(r)
                if (len(r) != 0):
                    List.append(r)

        print(List)

        for i in List:
            menu_name = i.pop(0)
            print(menu_name)
            for j in i:
                submenu_name = j
                print(submenu_name)
                menu_inst = Menu.objects.get(menu=menu_name)
                for x in Submenu.objects.all():
                    if x.menu == menu_inst and x.submenu == submenu_name:
                        print(x)
                        new_role_detail = Roledetail(menu=menu_inst, submenu=x, role=new_role)
                        new_role_detail.save()

        return redirect('/Admin/Roles')
    else:
        menus = Menu.objects.filter(is_deleted='N')
        submenus = Submenu.objects.filter(is_deleted='N')



        return render(request, 'cdpapp/Role.html', {'menus': menus, 'submenus': submenus, 'submenusvalue': getNavigation(request)})


def edit_role(request, role_id):
    role = Role.objects.get(pk=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('/Admin/Roles')
    else:
        form = RoleForm(instance=role)
        return render(request, 'cdpapp/role_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def role_details(request, role_id):
    role = Role.objects.get(pk=role_id)
    if request.method == 'POST':
        form = RoleDetailForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('/Admin/Roles')
    else:
        form = RoleDetailForm(instance=role)
        return render(request, 'cdpapp/role_detail.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    role.is_deleted = 'Y'
    role.save()
    return redirect('/Admin/Roles')


def cluster_list(request):
    cluster_list = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(cluster_list, 5)

    try:
        clusters = paginator.page(page)
    except PageNotAnInteger:
        clusters = paginator.page(1)
    except EmptyPage:
        clusters = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/cluster table.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def add_cluster(request):
    if request.method == 'POST':
        cluster_name = request.POST['cluster_name']
        description = request.POST['descr']
        created_by = request.user.username
        new_cluster = Cluster(cluster_name=cluster_name, description=description)
        new_cluster.save()
        return redirect('/Admin/Configuration/Cluster')
    else:
        return render(request, 'cdpapp/cluster.html', {'submenusvalue': getNavigation(request)})


def edit_cluster(request, cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    if request.method == 'POST':
        form = ClusterForm(request.POST, instance=cluster)
        if form.is_valid():
            form.save()
            cluster.modified_by = request.user.username
            cluster.save()
            return redirect('/Admin/Configuration/Cluster')
    else:
        form = ClusterForm(instance=cluster)
        return render(request, 'cdpapp/cluster_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_cluster(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cluster.is_deleted = 'Y'
    cluster.save()
    return redirect('/Admin/Configuration/Cluster')


def camera_table(request):
    camera_list = Camera.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(camera_list, 5)

    try:
        cameras = paginator.page(page)
    except PageNotAnInteger:
        cameras = paginator.page(1)
    except EmptyPage:
        cameras = paginator.page(paginator.num_pages)

    return render(request, 'cdpapp/camera table.html', {'cameras': cameras, 'submenusvalue': getNavigation(request)})


def add_camera(request):
    if request.method == 'POST':
        camname = request.POST['camname']
        camip = request.POST['camip']
        x1_cord = request.POST['x1']
        y1_cord = request.POST['y1']
        x2_cord = request.POST['x2']
        y2_cord = request.POST['y2']
        cluster = request.POST['clust']
        algo_type = request.POST['algo']

        clusterinst = Cluster.objects.get(cluster_name=cluster)

        new_camera = Camera(camname=camname, camip=camip, x1_cord=x1_cord, y1_cord=y1_cord, x2_cord=x2_cord, y2_cord=y2_cord, cluster=clusterinst,
                            algo_type=algo_type)
        new_camera.save()

        return redirect('/Admin/Configuration/Camera')
    else:
        clusters = Cluster.objects.filter(is_deleted='N')



        return render(request, 'cdpapp/Camera.html', {'clusters': clusters, 'submenusvalue': getNavigation(request)})


def edit_camera(request, camera_id):
    camera = Camera.objects.get(pk=camera_id)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
            return redirect('/Admin/Configuration/Camera')
    else:
        form = CameraForm(instance=camera)
        return render(request, 'cdpapp/camera_edit.html', {'form': form, 'submenusvalue': getNavigation(request)})


def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    camera.is_deleted = 'Y'
    camera.save()
    return redirect('/Admin/Configuration/Camera')


def other_config(request):
    return render(request, 'cdpapp/other-config.html', {'submenusvalue': getNavigation(request)})  # REMAINING


def logout_request(request):
    logout(request)
    return redirect('/')
