from django.db import models
from django import forms
from django.forms import ModelForm
from django.utils import timezone


class Tag(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=15, choices=[
        ("#6a1b9a", "Purple"),
        ("#1976d2", "Blue"),
        ("#ec407a", "Pink"),
        ("#81d4fa", "Light Blue")
    ])

    def __str__(self):
        return str(self.name)


class Application(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    Development_Name = models.CharField(max_length=50, blank=False)
    Address_Line = models.CharField(max_length=100, null=True, blank=True)
    City = models.CharField(max_length=25, null=True, blank=True)
    County = models.CharField(max_length=25, null=True, blank=True)
    Region = models.CharField(max_length=25, null=True, blank=True)
    Coordinates = models.CharField(max_length=30, null=True, blank=True)
    Census_Tract = models.CharField(max_length=25, null=True, blank=True)
    Acreage = models.CharField(max_length=25, null=True, blank=True)
    LIHTC_Units = models.IntegerField(null=True, blank=True, default=0)
    MR_Units = models.CharField(max_length=10, null=True, blank=True, default=0)
    Total_Units = models.IntegerField(null=True, blank=True, default=0)
    Developer = models.CharField(max_length=100, null=True, blank=True)
    Development_Owner = models.CharField(max_length=100, null=True, blank=True)
    HUB = models.CharField(max_length=50, null=True, blank=True)
    Non_Profit = models.BooleanField(null=True, blank=True)
    NP_Tax_Exempt = models.BooleanField(null=True, blank=True)
    Development_Entity = models.CharField(max_length=100, null=True, blank=True)
    Program = models.CharField(max_length=1, choices=[("4", "4%"), ("9", "9%")], null=True, blank=True)
    Total_Funding = models.IntegerField(null=True, blank=True)
    MFDL_Additional_Funding = models.IntegerField(null=True, blank=True)
    MFDL_Funding_Amount = models.IntegerField(null=True, blank=True)
    Supplemental_Additional_Funding = models.IntegerField(null=True, blank=True)
    Supplemental_Funding_Amount = models.IntegerField(null=True, blank=True)
    Force_Majeure_Additional_Funding = models.IntegerField(null=True, blank=True)
    Force_Majeure_Funding_Amount = models.IntegerField(null=True, blank=True)
    Fwd_Cmit_Additional_Funding = models.IntegerField(null=True, blank=True)
    Fwd_Cmit_Funding_Amount = models.IntegerField(null=True, blank=True)
    TCAP_TCEP_Additional_Funding = models.IntegerField(null=True, blank=True)
    TCAP_TCEP_Funding_Amount = models.IntegerField(null=True, blank=True)
    Common_SF = models.IntegerField(null=True, blank=True)
    NRA_SF = models.IntegerField(null=True, blank=True)
    TDHCA_Number = models.CharField(max_length=25, null=True, blank=True)
    Original_Number = models.CharField(max_length=25, null=True, blank=True)
    MFDL_Number = models.CharField(max_length=25, null=True, blank=True)
    Supplemental_Number = models.CharField(max_length=25, null=True, blank=True)
    Force_Majeure_Number = models.CharField(max_length=25, null=True, blank=True)
    Fwd_Cmit_Number = models.CharField(max_length=25, null=True, blank=True)
    TCAP_TCEP_Number = models.CharField(max_length=25, null=True, blank=True)
    Designation = models.CharField(max_length=25, null=True, blank=True)
    Pop_Served = models.CharField(max_length=50, null=True, blank=True)
    Year_Underserved = models.DateField(null=True, blank=True)
    MFDL_Year = models.DateField(null=True, blank=True)
    Supplemental_Year = models.DateField(null=True, blank=True)
    Force_Majeure_Year = models.DateField(null=True, blank=True)
    Fwd_Cmit_Year = models.DateField(null=True, blank=True)
    TCAP_TCEP_Year = models.DateField(null=True, blank=True)
    USF = models.BooleanField(null=True, blank=True)
    NRF = models.BooleanField(null=True, blank=True)
    Activity = models.CharField(max_length=50, null=True, blank=True)
    Set_Aside = models.CharField(max_length=50, null=True, blank=True)
    Last_Updated = models.DateField(null=True, blank=True, auto_now=True)
    Contact_Point = models.CharField(max_length=50, null=True, blank=True)
    Dev_Owner_Phone = models.CharField(max_length=15, null=True, blank=True)
    Asset_Manager = models.CharField(max_length=50, null=True, blank=True)
    # dates
    Commitment_Due_Original = models.DateField(null=True, blank=True)
    Commitment_Due_New = models.DateField(null=True, blank=True)
    Commitment_Submitted_Original = models.DateField(null=True, blank=True)
    Commitment_Submitted_New = models.DateField(null=True, blank=True)
    Commitment_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    Commitment_Status_New = models.CharField(max_length=25, null=True, blank=True)
    Carryover_Due_Original = models.DateField(null=True, blank=True)
    Carryover_Due_New = models.DateField(null=True, blank=True)
    Carryover_Submitted_Original = models.DateField(null=True, blank=True)
    Carryover_Submitted_New = models.DateField(null=True, blank=True)
    Carryover_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    Carryover_Status_New = models.CharField(max_length=25, null=True, blank=True)
    Ten_Percent_Due_Original = models.DateField(null=True, blank=True)
    Ten_Percent_Due_New = models.DateField(null=True, blank=True)
    Ten_Percent_Submitted_Original = models.DateField(null=True, blank=True)
    Ten_Percent_Submitted_New = models.DateField(null=True, blank=True)
    Ten_Percent_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    Ten_Percent_Status_New = models.CharField(max_length=25, null=True, blank=True)
    Cost_Cert_Due_Original = models.DateField(null=True, blank=True)
    Cost_Cert_Due_New = models.DateField(null=True, blank=True)
    Cost_Cert_Submitted_Original = models.DateField(null=True, blank=True)
    Cost_Cert_Submitted_New = models.DateField(null=True, blank=True)
    Cost_Cert_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    Cost_Cert_Status_New = models.CharField(max_length=25, null=True, blank=True)
    CSR_Due_Original = models.DateField(null=True, blank=True)
    CSR_Due_New = models.DateField(null=True, blank=True)
    CSR_Submitted_Original = models.DateField(null=True, blank=True)
    CSR_Submitted_New = models.DateField(null=True, blank=True)
    CSR_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    CSR_Status_New = models.CharField(max_length=25, null=True, blank=True)
    PiS_Due_Original = models.DateField(null=True, blank=True)
    PiS_Due_New = models.DateField(null=True, blank=True)
    PiS_Submitted_Original = models.DateField(null=True, blank=True)
    PiS_Submitted_New = models.DateField(null=True, blank=True)
    PiS_Status_Original = models.CharField(max_length=25, null=True, blank=True)
    PiS_Status_New = models.CharField(max_length=25, null=True, blank=True)

    stage = models.CharField(max_length=30, choices=[
            ("pre", "Pre-Construction Phase"),
            ("during", "During-Construction Phase"),
            ("post", "Post-Construction Phase"),
            ("af", "Additional Funding"),
            ("c", "Complete")
        ], null=True, blank=True)

    tag1 = models.ForeignKey(Tag, related_name="first_tag", on_delete=models.SET_NULL, null=True, blank=True)
    tag2 = models.ForeignKey(Tag, related_name="second_tag", on_delete=models.SET_NULL, null=True, blank=True)
    tag3 = models.ForeignKey(Tag, related_name="third_tag", on_delete=models.SET_NULL, null=True, blank=True)
    tag4 = models.ForeignKey(Tag, related_name="fourth_tag", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.Development_Name)


class ApplicationForm(ModelForm):

    ppe1 = forms.CharField(max_length=100, required=False)
    ppe2 = forms.CharField(max_length=100, required=False)
    ppe3 = forms.CharField(max_length=100, required=False)
    ppe4 = forms.CharField(max_length=100, required=False)
    ppe5 = forms.CharField(max_length=100, required=False)
    ppe6 = forms.CharField(max_length=100, required=False)
    ppe7 = forms.CharField(max_length=100, required=False)
    ppe8 = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Application
        exclude = ["stage", "USF", "NRF", "tag1", "tag2", "tag3", "tag4"]


class Event(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    development_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    google_id = models.CharField(max_length=100, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.development_name)} {self.field_name.replace('_', ' ')}"


class PreviousParticipantEntities(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    application = models.ManyToManyField(Application)

    def __str__(self):
        return str(self.name)
