import pandas as pd
import plotly.express as px
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Avg
from .forms import UploadFileForm
from .models import Performance, Student


def dashboard(request):
    data = Performance.objects.all().values()
    total_students = Student.objects.count()
    total_records = Performance.objects.count()

    stats = Performance.objects.aggregate(
        avg_score=Avg('score'),
        avg_attendance=Avg('attendance')
    )

    if data:
        df = pd.DataFrame(data)
        subject_avg = df.groupby('subject')['score'].mean().reset_index()
        fig = px.bar(
            subject_avg, x='subject', y='score',
            title='Average Scores by Subject',
            color='score',
            color_continuous_scale='Viridis'
        )
        chart = fig.to_html(full_html=False)
    else:
        chart = "<p>No data yet. Please upload a file.</p>"

    context = {
        'chart': chart,
        'total_students': total_students,
        'total_records': total_records,
        'avg_score': stats['avg_score'] or 0,
        'avg_attendance': stats['avg_attendance'] or 0,
    }
    return render(request, 'tracker/dashboard.html', context)


def upload_csv(request):
    chart = None
    msg = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_path = fs.path(filename)
            try:
                df = pd.read_csv(uploaded_file_path)
                required_cols = {
                    'student', 'subject', 'score',
                    'attendance', 'term', 'date_recorded'
                }
                if not required_cols.issubset(df.columns):
                    msg = "CSV missing required columns."
                else:
                    # Save data to database
                    records_added = 0
                    for _, row in df.iterrows():
                        student, created = Student.objects.get_or_create(
                            name=row['student'],
                            defaults={
                                'class_name': row.get('class', 'N/A'),
                                'roll_no': row.get('roll_no', 0),
                                'gender': row.get('gender', 'N/A')
                            }
                        )
                        Performance.objects.create(
                            student=student,
                            subject=row['subject'],
                            score=row['score'],
                            attendance=row['attendance'],
                            term=row['term'],
                            date_recorded=row['date_recorded']
                        )
                        records_added += 1

                    # Generate preview chart
                    subject_data = (
                        df.groupby('subject')['score']
                        .mean().reset_index()
                    )
                    fig = px.bar(
                        subject_data,
                        x='subject', y='score',
                        title='Average Scores by Subject'
                    )
                    chart = fig.to_html(full_html=False)
                    msg = f"Successfully added {records_added} records!"
            except Exception as e:
                msg = f"Error: {e}"
    else:
        form = UploadFileForm()
    context = {'form': form, 'chart': chart, 'msg': msg}
    return render(request, 'tracker/upload.html', context)


def students_list(request):
    students = Student.objects.annotate(
        performance_count=Count('performance')
    ).order_by('roll_no')
    return render(request, 'tracker/students.html', {'students': students})


def reports(request):
    data = Performance.objects.all().values()

    if data:
        df = pd.DataFrame(data)

        # Subject-wise performance
        subject_avg = df.groupby('subject')['score'].mean().reset_index()
        fig1 = px.bar(
            subject_avg, x='subject', y='score',
            title='Average Scores by Subject',
            color='score',
            color_continuous_scale='Blues'
        )
        subject_chart = fig1.to_html(full_html=False)

        # Term-wise analysis
        term_avg = df.groupby('term')['score'].mean().reset_index()
        fig2 = px.line(
            term_avg, x='term', y='score',
            title='Performance Trend by Term',
            markers=True
        )
        term_chart = fig2.to_html(full_html=False)

        # Attendance vs Performance scatter
        fig3 = px.scatter(
            df, x='attendance', y='score',
            title='Attendance vs Performance Correlation',
            color='subject',
            size='score',
            hover_data=['term']
        )
        scatter_chart = fig3.to_html(full_html=False)
    else:
        subject_chart = "<p>No data available.</p>"
        term_chart = "<p>No data available.</p>"
        scatter_chart = "<p>No data available.</p>"

    context = {
        'subject_chart': subject_chart,
        'term_chart': term_chart,
        'scatter_chart': scatter_chart,
    }
    return render(request, 'tracker/reports.html', context)


def files_list(request):
    import os
    from django.conf import settings

    uploads_dir = settings.MEDIA_ROOT
    files = []

    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(uploads_dir, filename)
                file_stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': file_stat.st_size,
                    'date': pd.Timestamp.fromtimestamp(
                        file_stat.st_mtime
                    ).strftime('%Y-%m-%d %H:%M')
                })

    files.sort(key=lambda x: x['date'], reverse=True)
    return render(request, 'tracker/files.html', {'files': files})


def file_view(request, filename):
    import os
    from django.conf import settings
    from django.http import Http404

    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(filepath) or not filename.endswith('.csv'):
        raise Http404("File not found")

    try:
        df = pd.read_csv(filepath)

        # Calculate statistics
        total_records = len(df)
        unique_students = (
            df['student'].nunique() if 'student' in df.columns else 0
        )
        unique_subjects = (
            df['subject'].nunique() if 'subject' in df.columns else 0
        )
        avg_score = df['score'].mean() if 'score' in df.columns else 0

        # Generate charts
        charts_html = ""
        if 'subject' in df.columns and 'score' in df.columns:
            subject_avg = df.groupby('subject')['score'].mean().reset_index()
            fig1 = px.bar(
                subject_avg, x='subject', y='score',
                title='Average Scores by Subject',
                color='score',
                color_continuous_scale='Viridis'
            )
            charts_html += fig1.to_html(full_html=False)

        if 'student' in df.columns and 'score' in df.columns:
            student_avg = (
                df.groupby('student')['score']
                .mean().reset_index()
                .sort_values('score', ascending=False)
                .head(10)
            )
            fig2 = px.bar(
                student_avg, x='student', y='score',
                title='Top 10 Students by Average Score',
                color='score',
                color_continuous_scale='Blues'
            )
            charts_html += fig2.to_html(full_html=False)

        # Generate table HTML
        table_html = df.head(50).to_html(
            classes='table',
            index=False,
            border=0
        )

        context = {
            'filename': filename,
            'total_records': total_records,
            'unique_students': unique_students,
            'unique_subjects': unique_subjects,
            'avg_score': avg_score,
            'charts': charts_html,
            'table_html': table_html,
        }
        return render(request, 'tracker/file_view.html', context)

    except Exception as e:
        raise Http404(f"Error reading file: {e}")


def file_delete(request, filename):
    import os
    from django.conf import settings
    from django.shortcuts import redirect
    from django.http import Http404

    filepath = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(filepath) or not filename.endswith('.csv'):
        raise Http404("File not found")

    try:
        os.remove(filepath)
    except Exception:
        pass

    return redirect('files_list')
