import json
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin

from esr21_reports.models.dashboard_statistics import DashboardStatistics
from ..models import VaccinationStatistics, EnrollmentStatistics

class EnrollmentReportMixin(EdcBaseViewMixin):
    
    
    pregnancy_test_model = 'esr21_subject.pregnancytest'
    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    
    @property
    def pregnancy_test_cls(self):
        return django_apps.get_model(self.pregnancy_test_model)
    
    @property
    def vaccination_details_cls(self):
        return  django_apps.get_model(self.vaccination_details_model)
    
    @property
    def vaccination_details_stats(self):
        ids = self.vaccination_details_cls.objects.filter(received_dose_before='first_dose').values_list('subject_visit__subject_identifier', flat=True).distinct()
        
        gabs_pregnancy = self.pregnancy_test_cls.objects.filter(result='POS',site_id=40, subject_visit__subject_identifier__in=ids).values_list('subject_visit__subject_identifier', flat=True).distinct().count()

        maun_pregnancy = self.pregnancy_test_cls.objects.filter(result='POS',site_id=41, subject_visit__subject_identifier__in=ids).values_list('subject_visit__subject_identifier', flat=True).distinct().count()

        serowe_pregnancy = self.pregnancy_test_cls.objects.filter(result='POS',site_id=42, subject_visit__subject_identifier__in=ids).values_list('subject_visit__subject_identifier', flat=True).distinct().count()

        ftown_pregnancy = self.pregnancy_test_cls.objects.filter(result='POS',site_id=43, subject_visit__subject_identifier__in=ids).values_list('subject_visit__subject_identifier', flat=True).distinct().count()

        phikwe_pregnancy = self.pregnancy_test_cls.objects.filter(result='POS',site_id=44, subject_visit__subject_identifier__in=ids).values_list('subject_visit__subject_identifier', flat=True).distinct().count()
        
        return ['Vaccination Details', gabs_pregnancy, maun_pregnancy, serowe_pregnancy, ftown_pregnancy, phikwe_pregnancy]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
