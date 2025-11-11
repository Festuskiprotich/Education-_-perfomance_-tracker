from django.test import TestCase
from .models import Student, Performance
from datetime import date


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            class_name="10A",
            roll_no=101,
            gender="Male"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(str(self.student), "John Doe")


class PerformanceModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="Jane Smith",
            class_name="10B",
            roll_no=102,
            gender="Female"
        )
        self.performance = Performance.objects.create(
            student=self.student,
            subject="Mathematics",
            score=85.5,
            attendance=92.0,
            term="Term 1",
            date_recorded=date.today()
        )

    def test_performance_creation(self):
        self.assertEqual(self.performance.subject, "Mathematics")
        self.assertEqual(self.performance.score, 85.5)
        self.assertEqual(str(self.performance), "Jane Smith - Mathematics")
