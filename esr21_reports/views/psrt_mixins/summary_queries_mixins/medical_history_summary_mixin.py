from django.apps import apps as django_apps
from django.db.models import Q

class MedicalHistorySummaryMixin:
    medical_history_model = 'esr21_subject.medicalhistory'
    

    @property
    def medical_history_cls(self):
        return django_apps.get_model(self.medical_history_model)

    @property
    def male_child_bearing_potential_statistics(self):
        """
        Male and child bearing potential is Yes    
        """
        return ["First dose missing and second dose not missing", 0, 0, 0, 0, 0, 0]

    @property
    def no_hiv_results_statistics(self):
        """
        No HIV result    
        """
        return ["No HIV result", 0, 0, 0, 0, 0, 0]

    @property
    def no_medical_history_statistics(self):
        """
        No medical history form    
        """
        # enrolled with no medical histories
        no_medical_histories = []

        for site_id in self.site_ids:
            medical_histories = self.medical_history_cls.objects.filter(Q(site_id=site_id) & ~Q(
                subject_visit__subject_identifier__in=self.enrolled)).count()
            no_medical_histories.append(medical_histories)

        return ["No medical history form", *no_medical_histories, sum(no_medical_histories)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            male_child_bearing_stats = self.male_child_bearing_potential_statistics,
            no_hiv_results_stats = self.no_hiv_results_statistics,
            no_medical_history_stats = self.no_medical_history_statistics,)

        return context