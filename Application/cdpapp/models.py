from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime

deleted_choices = [('N', 'NO'), ('Y', 'YES')]


class Algo_master(models.Model):
    algo = models.CharField(max_length=30, null=False)
    algo_desc = models.CharField(max_length=80, default='description')
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.algo

    class Meta:
        managed = True
        db_table = "Algo_master"


class Bill_plan(models.Model):
    billplan = models.CharField(max_length=100)
    billplan_cd = models.CharField(max_length=100)
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.billplan

    class Meta:
        managed = True
        db_table = "Bill_plan"


status_choices = [('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended')]


class Cust_org(models.Model):
    cust_org = models.CharField(max_length=50, unique=True)
    cust_org_acro = models.CharField(max_length=15)
    onboard_date = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices, default='Active')
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)
    bill_plan = models.ForeignKey(Bill_plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.cust_org

    class Meta:
        managed = True
        db_table = "Cust_org"


class Cluster(models.Model):
    cluster_name = models.CharField(unique=True, blank=False, max_length=100)
    description = models.CharField(max_length=500)
    customer = models.ForeignKey(Cust_org, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20, default='')
    modified_on = models.DateTimeField(auto_now=True, blank=True)
    modified_by = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "Cluster"


algo_choices = [('Vehicle', 'Vehicle'), ('Person', 'Person')]
other_choices = [('Age', 'Age'), ('Gender', 'Gender'),
                 ('Emotion', 'Emotion'), ('People Count', 'People Count'),
                 ('Vehicle Count', 'Vehicle Count'),
                 ('Unique People Count', 'Unique People Count'),
                 ('Unique Vehicle Count', 'Unique Vehicle Count')]


class Camera(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    camname = models.CharField(unique=True, blank=False, max_length=100)
    camip = models.CharField(max_length=100, null=False, default=0)
    algo_type = models.CharField(max_length=20, choices=algo_choices, default='Type')
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    x1_cord = models.IntegerField(null=False, default=0)
    x2_cord = models.IntegerField(null=False, default=0)
    y1_cord = models.IntegerField(null=False, default=0)
    y2_cord = models.IntegerField(null=False, default=0)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = "Camera"


class Menu(models.Model):
    menu = models.CharField(max_length=20, blank=False)
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.menu

    class Meta:
        managed = True
        db_table = "Menu"


class Submenu(models.Model):
    submenu = models.CharField(max_length=20)
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return self.submenu

    class Meta:
        managed = True
        db_table = "Submenu"


class Role(models.Model):
    role = models.CharField(max_length=100, blank=False)
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    role_desc = models.CharField(max_length=200, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.role

    class Meta:
        managed = True
        db_table = "Role"


class Roledetail(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    submenu = models.ForeignKey(Submenu, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.role

    class Meta:
        managed = True
        db_table = "Roledetail"


designation_choices = [('Lead', 'Lead'), ('Manager', 'Manager')]


class Appuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+91'. Up to 15 digits allowed.")
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    mobile = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)
    customer = models.ForeignKey(Cust_org, on_delete=models.CASCADE)
    is_superuser = models.CharField(max_length=1, choices=deleted_choices, default='N')
    designation = models.CharField(max_length=20, choices=designation_choices, default='designation')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)
    profile_pic = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True
        db_table = "Appuser"



class Agent(models.Model):
    fname = models.CharField(max_length=15, default='fname')
    lname = models.CharField(max_length=20, default='lname')
    is_deleted = models.CharField(max_length=1, choices=deleted_choices, default='N')
    mac_id = models.CharField(max_length=30, null=True, blank=True)
    customer = models.ForeignKey(Cust_org, on_delete=models.CASCADE)
    manager_id = models.IntegerField()
    lead = models.ForeignKey(Appuser, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.fname

    class Meta:
        managed = True
        db_table = "Agent"

notification_status_choices = [('Open', 'Open'), ('Viewed', 'Viewed')]

class Incident(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default='category', null=False)
    mac_id = models.CharField(max_length=30, null=True, blank=True)
    notification_status = models.CharField(max_length=10, choices=notification_status_choices, default='Open')
    incident_date = models.DateTimeField(auto_now_add=True, blank=True)
    incident_img = models.ImageField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=20)
    modified_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=20)

    def __str__(self):
        return self.agent

    class Meta:
        managed = True
        db_table = "Incident"





