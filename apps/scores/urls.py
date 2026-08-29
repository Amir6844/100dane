from django.urls import path
from .views import BulkScoreView, StudentReportView, ExportExcelView, MyScoresView, ReportsDashboardView
app_name='scores'
urlpatterns=[
    path('exam/<int:exam_pk>/bulk/', BulkScoreView.as_view(), name='bulk'),
    path('class/<int:class_pk>/report/', StudentReportView.as_view(), name='report'),
    path('class/<int:class_pk>/export/', ExportExcelView.as_view(), name='export'),
    path('my/', MyScoresView.as_view(), name='my_scores'),
    path('reports/', ReportsDashboardView.as_view(), name='reports'),
]
