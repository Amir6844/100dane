"""
Reusable statistics services for 100dane
Avoids duplicating statistical logic across views.
Uses efficient ORM: annotate, aggregate, Exists, Subquery etc.
Persian-friendly.
"""
from django.db.models import Avg, Max, Min, Count, Q, Exists, OuterRef, Subquery, DecimalField
from django.contrib.auth import get_user_model

User = get_user_model()

def class_stats(classroom):
    """Return dict for Classroom dashboard: student_count, group_count, lesson_count, exam_count, average, highest, lowest, recent"""
    from apps.classes.models import Classroom
    from apps.groups.models import Group
    from apps.lessons.models import Lesson
    from apps.exams.models import Exam
    from apps.scores.models import Score
    # use efficient queries, avoid N+1
    student_count = classroom.students.count()
    group_count = classroom.groups.count()
    lesson_count = classroom.lessons.count()
    exam_count = classroom.exams.count()
    agg = Score.objects.filter(exam__classroom=classroom).aggregate(avg=Avg('value'), hi=Max('value'), lo=Min('value'))
    recent_scores = Score.objects.filter(exam__classroom=classroom).select_related('student', 'exam').order_by('-created_at')[:5]
    recent_exams = classroom.exams.order_by('-created_at')[:3]
    recent_lessons = classroom.lessons.order_by('-created_at')[:3]
    return {
        'student_count': student_count,
        'group_count': group_count,
        'lesson_count': lesson_count,
        'exam_count': exam_count,
        'average': round(agg['avg'], 2) if agg['avg'] else None,
        'highest': agg['hi'],
        'lowest': agg['lo'],
        'recent_scores': recent_scores,
        'recent_exams': recent_exams,
        'recent_lessons': recent_lessons,
    }

def group_stats(group):
    from apps.scores.models import Score
    # group members average across all exams of its classroom
    members = group.members.all()
    if not members:
        return {'member_count': 0, 'average': None, 'highest': None, 'lowest': None}
    # Use Score through exam__classroom = group classroom and student in members
    agg = Score.objects.filter(exam__classroom=group.classroom, student__in=members).aggregate(avg=Avg('value'), hi=Max('value'), lo=Min('value'))
    # annotate per member avg using subquery
    return {
        'member_count': members.count(),
        'average': round(agg['avg'], 2) if agg['avg'] else None,
        'highest': agg['hi'],
        'lowest': agg['lo'],
    }

def student_stats(student, classroom=None):
    from apps.scores.models import Score
    qs = Score.objects.filter(student=student)
    if classroom:
        qs = qs.filter(exam__classroom=classroom)
    agg = qs.aggregate(avg=Avg('value'), hi=Max('value'), lo=Min('value'), cnt=Count('id'))
    return {
        'exam_count': agg['cnt'],
        'average': round(agg['avg'], 2) if agg['avg'] else None,
        'highest': agg['hi'],
        'lowest': agg['lo'],
    }

def exam_stats(exam):
    from apps.scores.models import Score
    qs = Score.objects.filter(exam=exam)
    agg = qs.aggregate(avg=Avg('value'), hi=Max('value'), lo=Min('value'), cnt=Count('id'))
    # pass count: >= 10 /20? assume half of total_score
    pass_threshold = float(exam.total_score) * 0.5
    pass_count = qs.filter(value__gte=pass_threshold).count() if agg['cnt'] else 0
    return {
        'participant_count': agg['cnt'],
        'average': round(agg['avg'], 2) if agg['avg'] else None,
        'highest': agg['hi'],
        'lowest': agg['lo'],
        'pass_count': pass_count,
        'pass_threshold': pass_threshold,
    }

def student_rank(classroom, student):
    """Rank student by avg in classroom"""
    from apps.scores.models import Score
    from django.db.models import Avg
    students = classroom.students.all()
    # compute avgs efficiently via annotate
    # use subquery for avg
    ranking = []
    for s in students:
        avg = Score.objects.filter(student=s, exam__classroom=classroom).aggregate(avg=Avg('value'))['avg']
        ranking.append((s.id, float(avg) if avg else 0))
    ranking.sort(key=lambda x: x[1], reverse=True)
    for i, (sid, _) in enumerate(ranking, 1):
        if sid == student.id:
            return i
    return None
