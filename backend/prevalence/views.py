from django.db.models import Max
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View

from .models import DiseaseStats, GlobalStats


class PrevalenceView(TemplateView):
    template_name = "prevalence.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        disease_stats = DiseaseStats.objects.filter(
            id__in=DiseaseStats.objects.values("disease")
            .annotate(max_id=Max("id"))
            .values("max_id")
        ).order_by("-n_patients")

        context["diseases"] = disease_stats[:16]

        context["patients_by_disease"] = disease_stats[:5]

        global_stats = GlobalStats.objects.order_by("-created_at").first()

        context["global_stats"] = global_stats
        context[
            "patients_by_source"
        ] = global_stats.patientsbysource_set.all().order_by("-n_patients")

        return context


class PrevalenceDataView(View):
    def get(self, request, *args, **kwargs):
        disease_stats = DiseaseStats.objects.filter(
            id__in=DiseaseStats.objects.values("disease")
            .annotate(max_id=Max("id"))
            .values("max_id")
        ).order_by("-n_patients")

        diseases = [
            {
                "name": ds.disease.name,
                "n_patients": ds.n_patients,
                "n_contributors": ds.n_contributors,
                "confidence": ds.confidence,
                "other_sources": [
                    {
                        "name": source.name,
                        "url": source.url,
                    }
                    for source in ds.disease.urlsource_set.all()
                ],
            }
            for ds in disease_stats
        ]

        global_stats = GlobalStats.objects.order_by("-created_at").first()
        global_stats_data = {
            "n_diseases": global_stats.n_diseases,
            "n_contributors": global_stats.n_contributors,
            "n_patients": global_stats.n_patients,
        }

        patients_by_source = list(
            global_stats.patientsbysource_set.all()
            .order_by("-n_patients")
            .values("source", "n_patients")
        )

        data = {
            "diseases": diseases,
            "summary": global_stats_data,
            "patients_by_source": patients_by_source,
        }

        return JsonResponse(data)
