from django.core.management.base import BaseCommand
from core.models import Lab, DiagnosticTest
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate sample diagnostic tests and labs'

    def handle(self, *args, **options):
        # Create sample labs if they don't exist
        labs_data = [
            {
                'name': 'City Diagnostic Lab',
                'address': '123 Medical Street, Downtown, City',
                'phone': '+91 98765-43210',
            },
            {
                'name': 'Apollo Diagnostics',
                'address': '456 Health Avenue, Central Hospital, City',
                'phone': '+91 98765-43211',
            },
            {
                'name': 'LabPlus Center',
                'address': '789 Wellness Road, Tech Park, City',
                'phone': '+91 98765-43212',
            },
            {
                'name': 'Prime Healthcare Labs',
                'address': '321 Care Lane, Medical Complex, City',
                'phone': '+91 98765-43213',
            },
        ]

        labs = {}
        for lab_data in labs_data:
            lab, created = Lab.objects.get_or_create(
                name=lab_data['name'],
                defaults={
                    'address': lab_data['address'],
                    'phone': lab_data['phone'],
                    'status': 'Active'
                }
            )
            labs[lab_data['name']] = lab
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created lab: {lab.name}'))
            else:
                self.stdout.write(f'Lab already exists: {lab.name}')

        # Create sample diagnostic tests
        tests_data = [
            {
                'test_name': 'Complete Blood Count (CBC)',
                'price': Decimal('500.00'),
                'lab': 'City Diagnostic Lab',
                'description': 'Complete blood count to evaluate overall health'
            },
            {
                'test_name': 'Lipid Profile',
                'price': Decimal('800.00'),
                'lab': 'City Diagnostic Lab',
                'description': 'Check cholesterol and lipid levels'
            },
            {
                'test_name': 'Liver Function Test (LFT)',
                'price': Decimal('600.00'),
                'lab': 'Apollo Diagnostics',
                'description': 'Evaluate liver health and function'
            },
            {
                'test_name': 'Kidney Function Test (KFT)',
                'price': Decimal('600.00'),
                'lab': 'Apollo Diagnostics',
                'description': 'Assess kidney function and health'
            },
            {
                'test_name': 'Thyroid Profile (TSH, T3, T4)',
                'price': Decimal('750.00'),
                'lab': 'LabPlus Center',
                'description': 'Check thyroid hormone levels'
            },
            {
                'test_name': 'Blood Sugar Fasting',
                'price': Decimal('400.00'),
                'lab': 'LabPlus Center',
                'description': 'Fasting blood glucose test'
            },
            {
                'test_name': 'COVID-19 RT-PCR Test',
                'price': Decimal('550.00'),
                'lab': 'Prime Healthcare Labs',
                'description': 'COVID-19 diagnostic test using RT-PCR'
            },
            {
                'test_name': 'Pregnancy Test (Urine HCG)',
                'price': Decimal('350.00'),
                'lab': 'Prime Healthcare Labs',
                'description': 'Home urine pregnancy test'
            },
            {
                'test_name': 'Vitamin D Test',
                'price': Decimal('650.00'),
                'lab': 'City Diagnostic Lab',
                'description': 'Check Vitamin D levels'
            },
            {
                'test_name': 'Vitamin B12 Test',
                'price': Decimal('600.00'),
                'lab': 'Apollo Diagnostics',
                'description': 'Check Vitamin B12 levels'
            },
            {
                'test_name': 'Iron Studies',
                'price': Decimal('700.00'),
                'lab': 'LabPlus Center',
                'description': 'Test for iron deficiency anemia'
            },
            {
                'test_name': 'Calcium Profile',
                'price': Decimal('550.00'),
                'lab': 'Prime Healthcare Labs',
                'description': 'Check calcium and phosphorus levels'
            },
            {
                'test_name': 'Allergy Test Panel',
                'price': Decimal('2500.00'),
                'lab': 'City Diagnostic Lab',
                'description': 'Comprehensive allergy testing'
            },
            {
                'test_name': 'Chest X-Ray',
                'price': Decimal('400.00'),
                'lab': 'Apollo Diagnostics',
                'description': 'Chest radiography'
            },
            {
                'test_name': 'Abdominal Ultrasound',
                'price': Decimal('800.00'),
                'lab': 'LabPlus Center',
                'description': 'Ultrasound imaging of abdomen'
            },
        ]

        for test_data in tests_data:
            lab = labs[test_data['lab']]
            test, created = DiagnosticTest.objects.get_or_create(
                test_name=test_data['test_name'],
                lab=lab,
                defaults={
                    'price': test_data['price'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created test: {test.test_name}'))
            else:
                self.stdout.write(f'Test already exists: {test.test_name}')

        self.stdout.write(
            self.style.SUCCESS(
                '\n✓ Successfully populated diagnostic tests database!'
            )
        )