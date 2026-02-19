from django.urls import include, path
from . import views
from .views import lab_reports, logout_view
from django.contrib.auth import views as auth_views
from core.views import api_lab_reports_data, export_lab_report
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),

    # Dashboards
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
   
    path('dashboard/lab/', views.lab_dashboard, name='lab_dashboard'),
    path('dashboard/lab/tests/', views.lab_tests, name='lab_tests'),
    path('dashboard/lab/results/', views.lab_results, name='lab_results'),
    path('dashboard/lab/prices/', views.lab_prices, name='lab_prices'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/frontdesk/', views.frontdesk_dashboard, name='frontdesk_dashboard'),

    # ===== PATIENTS =====
    path('dashboard/admin/users/', views.admin_users, name='admin_users'),
    path('dashboard/admin/users/add/', views.admin_patient_add, name='admin_patient_add'),
    path('dashboard/admin/users/edit/<int:user_id>/', views.admin_user_edit, name='admin_user_edit'),
    path('dashboard/admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('dashboard/admin/users/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),

    # ===== DOCTORS =====
    path('dashboard/admin/doctors/', views.admin_doctors, name='admin_doctors'),
    path('dashboard/admin/doctors/add/', views.admin_doctor_add, name='admin_doctor_add'),
    path('dashboard/admin/doctors/edit/<int:doctor_id>/', views.admin_doctor_edit, name='admin_doctor_edit'),
    path('dashboard/admin/doctors/detail/<int:doctor_id>/', views.admin_doctor_detail, name='admin_doctor_detail'),
    path('dashboard/admin/doctors/delete/<int:doctor_id>/', views.admin_doctor_delete, name='admin_doctor_delete'),

    # ===== LABS =====
    path('dashboard/admin/labs/', views.admin_labs, name='admin_labs'),
    path('dashboard/admin/labs/add/', views.admin_add_lab, name='admin_add_lab'),
    path('dashboard/admin/labs/edit/<int:lab_id>/', views.admin_edit_lab, name='admin_edit_lab'),
    path('dashboard/admin/labs/delete/<int:lab_id>/', views.admin_delete_lab, name='admin_delete_lab'),

    # ===== FRONT DESK =====
    path('dashboard/admin/frontdesk/', views.admin_frontdesk, name='admin_frontdesk'),
    path('dashboard/admin/frontdesk/add/', views.admin_add_frontdesk, name='admin_add_frontdesk'),
    path('dashboard/admin/frontdesk/edit/<int:pk>/', views.admin_edit_frontdesk, name='admin_edit_frontdesk'),
    path('dashboard/admin/frontdesk/delete/<int:pk>/', views.admin_delete_frontdesk, name='admin_delete_frontdesk'),

    # ===== LAB TECHNICIANS =====
    path('dashboard/admin/technicians/', views.admin_lab_technician, name='admin_lab_technicians'),
    path('dashboard/admin/technicians/add/', views.admin_lab_technician_add, name='admin_lab_technician_add'),
    path('dashboard/admin/technicians/add/', views.admin_lab_technician_add, name='admin_add_technician'),          # alias used in add page form action
    
    path('dashboard/admin/technicians/edit/<int:pk>/', views.admin_lab_technician_edit, name='admin_lab_technician_edit'),
    path('dashboard/admin/technicians/delete/<int:pk>/', views.admin_delete_lab_technician, name='admin_delete_lab_technician'),

    # ===== PAYMENTS =====
    path('dashboard/admin/payments/', views.admin_payments, name='admin_payments'),
    path('dashboard/admin/payments/receipt/<int:payment_id>/', views.admin_payment_receipt, name='admin_payment_receipt'),

    # ===== REPORTS =====
    path('dashboard/admin/reports/', views.admin_reports, name='admin_reports'),
    
    path('dashboard/admin/settings/', views.admin_settings, name='admin_settings'),
    path('dashboard/admin/settings/general/', views.admin_settings_general, name='admin_settings_general'),
    path('dashboard/admin/settings/profile/', views.admin_settings_profile, name='admin_settings_profile'),
    path('dashboard/admin/settings/security/', views.admin_settings_security, name='admin_settings_security'),
    path('dashboard/admin/settings/notifications/', views.admin_settings_notifications, name='admin_settings_notifications'),
    path('dashboard/admin/settings/system/', views.admin_settings_system, name='admin_settings_system'),
    path('dashboard/admin/settings/backup/', views.admin_settings_backup, name='admin_settings_backup'),


    
    # Patient Dashboard
    path('dashboard/patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/patient_book-appointment/', views.patient_book_appointment, name='patient_book_appointment'),
    path('dashboard/patient/booked-tests/', views.patient_booked_tests, name='patient_booked_tests'),
    path('dashboard/patient/book-test/<int:test_id>/', views.book_diagnostic_test, name='book_diagnostic_test'),
    # AJAX endpoint - Get doctors by specialization
    path('api/get-doctors/', views.get_doctors_by_specialization, name='get_doctors_by_specialization'),
    # Search/Browse Doctors (optional - directory page)
    path('patient/search-doctors/', views.search_doctors, name='patient_search_doctors'),

    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('patient/appointments/cancel/<int:appointment_id>/', views.patient_cancel_appointment, name='patient_cancel_appointment'),
    path('patient/appointments/<int:appointment_id>/', views.patient_appointment_detail, name='patient_appointment_detail'),
    path(
        'patient/appointments/<int:appointment_id>/reschedule/',
        views.patient_reschedule_appointment,
        name='patient_reschedule_appointment'
    ),
    path('doctor/prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
    
    path(
        'api/available-time-slots/',
        views.get_available_time_slots,
        name='get_available_time_slots'
    ),
    
    # Patient Actions
    
    path('patient/diagnostic-tests/', views.patient_diagnostic_tests, name='patient_diagnostic_tests'),
    path('book-diagnostic-test/<int:test_id>/', views.book_diagnostic_test, name='book_diagnostic_test'),
    path('patient/booked-tests/', views.patient_booked_tests, name='patient_booked_tests'),
    path('patient/test-results/', views.patient_test_results, name='patient_test_results'),
    path('cancel-test-booking/<int:booking_id>/', views.cancel_test_booking, name='cancel_test_booking'),
    path('test-details/<int:test_id>/', views.view_test_details, name='test_details'),
    path('api/labs/', views.get_labs_api, name='get_labs_api'),
    path('lab/reports/', views.lab_reports, name='lab_reports'),
    path('lab/reports/export/pdf/', views.lab_report_export_pdf, name='lab_report_export_pdf'),
    path('lab/reports/export/excel/', views.lab_report_export_excel, name='lab_report_export_excel'),
    path('lab/result/<int:result_id>/', views.lab_result_detail, name='lab_result_detail'),
    path('api/lab/analytics/', views.get_analytics_data, name='get_analytics_data'),
    path('lab/test/add/', views.lab_add_test, name='lab_add_test'),
    path('lab/test/edit/<int:test_id>/', views.lab_edit_test, name='lab_edit_test'),
    path('lab/test/delete/<int:test_id>/', views.lab_delete_test, name='lab_delete_test'),
    
    
    path('dashboard/patient/patient_prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    
    path('medical-history/', views.medical_history, name='medical_history'),
    
    # Medical History - PDF Download
    path('medical-history/download/', views.download_medical_history, name='download_medical_history'),
    
    # Add Medical Records (ALL REQUIRED)
    path('add/allergy/', views.add_allergy, name='add_allergy'),
    path('add/medication/', views.add_medication, name='add_medication'),
    path('add/condition/', views.add_condition, name='add_condition'),
    path('add/surgery/', views.add_surgery, name='add_surgery'),
    path('add/family-history/', views.add_family_history, name='add_family_history'),
    path('add/immunization/', views.add_immunization, name='add_immunization'),
    path('add/vital-signs/', views.add_vital_signs, name='add_vital_signs'),
    path('add/health-note/', views.add_health_note, name='add_health_note'),
    path('add/medical-document/', views.add_medical_document, name='add_medical_document'),
    path('add/emergency-contact/', views.add_emergency_contact, name='add_emergency_contact'),
    path('add/blood-donation/', views.add_blood_donation, name='add_blood_donation'),
    
    # Delete Medical Records (OPTIONAL but recommended)
    path('delete/allergy/<int:allergy_id>/', views.delete_allergy, name='delete_allergy'),
    path('delete/medication/<int:medication_id>/', views.delete_medication, name='delete_medication'),
    
    path('patient/payments/', views.payments, name='payments'),
    path('patient/payments/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('patient/payments/<int:payment_id>/pay/', views.process_payment, name='process_payment'),
    path('patients/payment/test/<int:payment_id>/', views.process_test_payment, name='process_test_payment'),
    
    path('patient/settings/', views.patient_settings, name='patient_settings'),
    path('patient/settings/profile/', views.patient_settings_profile, name='patient_settings_profile'),
    path('patient/settings/security/', views.patient_settings_security, name='patient_settings_security'),
    path('patient/settings/medical/', views.patient_settings_medical, name='patient_settings_medical'),
    path('patient/settings/notifications/', views.patient_settings_notifications, name='patient_settings_notifications'),
    
    



    # Doctor Dashboard
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Doctor Appointments
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/appointment/<int:appointment_id>/', views.doctor_appointment_detail, name='doctor_appointment_detail'),
    path('doctor/appointment/<int:appointment_id>/confirm/', views.doctor_confirm_appointment, name='doctor_confirm_appointment'),
    path('doctor/appointment/<int:appointment_id>/complete/', views.doctor_complete_appointment, name='doctor_complete_appointment'),
    
    # Doctor Patients
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor/patient/<int:patient_id>/', views.doctor_patient_detail, name='doctor_patient_detail'),
    
    # Doctor Prescriptions
    path('doctor/prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
    path('doctor/prescription/<int:prescription_id>/', views.doctor_prescription_detail, name='doctor_prescription_detail'),
    path('doctor/appointment/<int:appointment_id>/add-prescription/', views.doctor_add_prescription, name='doctor_add_prescription'),
    
    path('doctor/', include([
        # Prescriptions
        path('prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
        path('prescription/<int:prescription_id>/', views.doctor_prescription_detail, name='doctor_prescription_detail'),
        path('prescription/create/', views.doctor_add_prescription, name='doctor_add_prescription'),
        path('prescription/<int:prescription_id>/edit/', views.doctor_edit_prescription, name='doctor_edit_prescription'),
        path('prescription/<int:prescription_id>/delete/', views.doctor_delete_prescription, name='doctor_delete_prescription'),
        path('prescription/<int:prescription_id>/print/', views.doctor_prescription_print, name='doctor_prescription_print'),
    ])),
    
    path('doctor/patients/', 
        views.doctor_patients, 
        name='doctor_patients'),
    
    # Patient detail/profile
    path('doctor/patient/<int:patient_id>/', 
        views.doctor_patient_detail, 
        name='doctor_patient_detail'),
    
    # Patient medical history
    path('doctor/patient/<int:patient_id>/history/', 
        views.doctor_patient_medical_history, 
        name='doctor_patient_medical_history'),
    
    # Patient appointments
    path('doctor/patient/<int:patient_id>/appointments/', 
        views.doctor_patient_appointments, 
        name='doctor_patient_appointments'),
    
    # Patient prescriptions
    path('doctor/patient/<int:patient_id>/prescriptions/', 
        views.doctor_patient_prescriptions, 
        name='doctor_patient_prescriptions'),
    
    # Patient allergies
    path('doctor/patient/<int:patient_id>/allergies/', 
        views.doctor_patient_allergies, 
        name='doctor_patient_allergies'),
    
    # Doctor Schedule
    path('doctor/schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('doctor/schedule/update/', views.doctor_schedule_update, name='doctor_schedule_update'),

     # ===== LABS =====
    path('dashboard/admin/labs/', views.admin_labs, name='admin_labs'),
    path('dashboard/admin/labs/add/', views.admin_add_lab, name='admin_add_lab'),
    path('dashboard/admin/labs/edit/<int:lab_id>/', views.admin_edit_lab, name='admin_edit_lab'),
    path('dashboard/admin/labs/delete/<int:lab_id>/', views.admin_delete_lab, name='admin_delete_lab'),
    
    path('api/lab-reports-data/', api_lab_reports_data, name='api_lab_reports_data'),
    path('export-lab-report/', export_lab_report, name='export_lab_report'),
    path('dashboard/lab/reports/', lab_reports, name='lab_reports'),
    
    
    path('admin/lab-technicians/', views.admin_lab_technician, name='admin_lab_technician'),
    path('admin/lab-technician/add/', views.admin_lab_technician_add, name='admin_add_technician'),
    path('admin/lab-technician/<int:pk>/edit/', views.admin_lab_technician_edit, name='admin_edit_technician'),
    path('admin/lab-technician/<int:pk>/delete/', views.admin_delete_lab_technician, name='admin_delete_technician'),
    path('lab/report-export-pdf/', views.lab_report_export_pdf, name='lab_report_export_pdf'),
    path('lab/report-export-excel/', views.lab_report_export_excel, name='lab_report_export_excel'),
    path('lab/result-detail/<int:result_id>/', views.lab_result_detail, name='lab_result_detail'),
    path('lab/get-analytics-data/', views.get_analytics_data, name='get_analytics_data'),
    path('patient/prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('patient/medical-history/', views.medical_history, name='medical_history'),
    path('add-allergy/', views.add_allergy, name='add_allergy'),
    path('add-medication/', views.add_medication, name='add_medication'),
    path('add-condition/', views.add_condition, name='add_condition'),
    path('add-surgery/', views.add_surgery, name='add_surgery'),
    path('add-family-history/', views.add_family_history, name='add_family_history'),
    path('add-immunization/', views.add_immunization, name='add_immunization'),
    path('add-vital-signs/', views.add_vital_signs, name='add_vital_signs'),
    path('add-health-note/', views.add_health_note, name='add_health_note'),
    path('add-medical-document/', views.add_medical_document, name='add_medical_document'),
    path('add-emergency-contact/', views.add_emergency_contact, name='add_emergency_contact'),
    path('add-blood-donation/', views.add_blood_donation, name='add_blood_donation'),
    path('download-medical-history/', views.download_medical_history, name='download_medical_history'),
    path('delete-allergy/<int:allergy_id>/', views.delete_allergy, name='delete_allergy'),
    path('delete-medication/<int:medication_id>/', views.delete_medication, name='delete_medication'),
    path('patient/test-results/', views.patient_test_results, name='patient_test_results'),
    path('labs-api/', views.get_labs_api, name='get_labs_api'),
    path('patient/diagnostic-tests/', views.patient_diagnostic_tests, name='patient_diagnostic_tests'),
    path('book-test/<int:test_id>/', views.book_diagnostic_test, name='book_diagnostic_test'),
    path('patient/booked-tests/', views.patient_booked_tests, name='patient_booked_tests'),
    path('cancel-test-booking/<int:booking_id>/', views.cancel_test_booking, name='cancel_test_booking'),
    path('test-details/<int:test_id>/', views.view_test_details, name='view_test_details'),
    path('lab/tests/', views.lab_tests, name='lab_tests'),
    path('lab/results/', views.lab_results, name='lab_results'),
    path('lab/prices/', views.lab_prices, name='lab_prices'),
    path('lab/add-test/', views.lab_add_test, name='lab_add_test'),
    path('lab/edit-test/<int:test_id>/', views.lab_edit_test, name='lab_edit_test'),
    path('lab/delete-test/<int:test_id>/', views.lab_delete_test, name='lab_delete_test'),
    path('lab/booking-details/<int:booking_id>/', views.lab_booking_details, name='lab_booking_details'),path('booking/<int:booking_id>/', views.lab_booking_details, name='lab_booking_detail'),
    path('booking/<int:booking_id>/reschedule/', views.reschedule_test_booking, name='reschedule_test_booking'),
    path('booking/<int:booking_id>/download-report/', views.download_test_report, name='download_test_report'),path('lab/reports/', views.lab_reports, name='lab_reports'),
    path('api/lab-reports-data/', views.api_lab_reports_data, name='api_lab_reports_data'),
    path('export-lab-report/', views.export_lab_report, name='export_lab_report'),
    path('api/lab-reports-data/', views.api_lab_reports_data, name='api_lab_reports_data'),
    
    
    path('frontdesk/', views.frontdesk_dashboard, name='frontdesk_dashboard'),
    path('frontdesk/appointments/', views.frontdesk_appointments, name='frontdesk_appointments'),
    path('frontdesk/appointments/<int:appointment_id>/', views.frontdesk_appointment_detail, name='frontdesk_appointment_detail'),
    path('frontdesk/book-appointment/', views.frontdesk_book_appointment, name='frontdesk_book_appointment'),
    path('frontdesk/appointment/confirmation/<int:appointment_id>/', views.frontdesk_appointment_confirmation, name='frontdesk_appointment_confirmation'),
    path('frontdesk/api/available-slots/', views.frontdesk_get_available_slots, name='frontdesk_get_available_slots'),
    path('frontdesk/api/search-patient/', views.frontdesk_search_patient, name='frontdesk_search_patient'),
    path('frontdesk/today-appointments/', views.frontdesk_today_appointments, name='frontdesk_today_appointments'),
    path('frontdesk/quick-checkin/<int:appointment_id>/', views.frontdesk_quick_checkin, name='frontdesk_quick_checkin'),
    path('frontdesk/check-in/', views.frontdesk_patient_checkin, name='frontdesk_patient_checkin'),
    path('frontdesk/patients/', views.frontdesk_patients_list, name='frontdesk_patients_list'),
    path('frontdesk/patients/<int:patient_id>/', views.frontdesk_patients_detail, name='frontdesk_patients_detail'),
    path('frontdesk/patients/<int:patient_id>/edit/', views.frontdesk_patients_edit, name='frontdesk_patients_edit'),
    path('frontdesk/doctors/', views.frontdesk_doctors_list, name='frontdesk_doctors_list'),
    path('frontdesk/doctors/<int:doctor_id>/', views.frontdesk_doctor_detail, name='frontdesk_doctor_detail'),
    path('frontdesk/payments/', views.frontdesk_payments, name='frontdesk_payments'),
    path('frontdesk/payments/<int:payment_id>/', views.frontdesk_payment_detail, name='frontdesk_payment_detail'),
    path('frontdesk/reports/', views.frontdesk_reports, name='frontdesk_reports'),
    path('frontdesk/settings/', views.frontdesk_settings, name='frontdesk_settings'),
    
    path('doctor/appointment/<int:appointment_id>/reschedule/', views.doctor_reschedule_appointment, name='doctor_reschedule_appointment'),
    
    
    path('frontdesk/', views.frontdesk_dashboard, name='frontdesk_dashboard'),
    path('frontdesk/appointments/', views.frontdesk_appointments, name='frontdesk_appointments'),
    path('frontdesk/appointments/<int:appointment_id>/', views.frontdesk_appointment_detail, name='frontdesk_appointment_detail'),
    path('frontdesk/book-appointment/', views.frontdesk_book_appointment, name='frontdesk_book_appointment'),
    path('frontdesk/appointment/confirmation/<int:appointment_id>/', views.frontdesk_appointment_confirmation, name='frontdesk_appointment_confirmation'),
    path('frontdesk/api/available-slots/', views.frontdesk_get_available_slots, name='frontdesk_get_available_slots'),
    path('frontdesk/api/search-patient/', views.frontdesk_search_patient, name='frontdesk_search_patient'),
    path('frontdesk/today-appointments/', views.frontdesk_today_appointments, name='frontdesk_today_appointments'),
    path('frontdesk/quick-checkin/<int:appointment_id>/', views.frontdesk_quick_checkin, name='frontdesk_quick_checkin'),
    path('frontdesk/check-in/', views.frontdesk_patient_checkin, name='frontdesk_patient_checkin'),
    path('frontdesk/patients/', views.frontdesk_patients_list, name='frontdesk_patients_list'),
    path('frontdesk/patients/<int:patient_id>/', views.frontdesk_patients_detail, name='frontdesk_patients_detail'),
    path('frontdesk/patients/<int:patient_id>/edit/', views.frontdesk_patients_edit, name='frontdesk_patients_edit'),
    path('frontdesk/doctors/', views.frontdesk_doctors_list, name='frontdesk_doctors_list'),
    path('frontdesk/doctors/<int:doctor_id>/', views.frontdesk_doctor_detail, name='frontdesk_doctor_detail'),
    path('frontdesk/payments/', views.frontdesk_payments, name='frontdesk_payments'),
    path('frontdesk/payments/<int:payment_id>/', views.frontdesk_payment_detail, name='frontdesk_payment_detail'),
    path('frontdesk/reports/', views.frontdesk_reports, name='frontdesk_reports'),
    path('frontdesk/settings/', views.frontdesk_settings, name='frontdesk_settings'),
    
    path('doctor/appointment/<int:appointment_id>/reschedule/', views.doctor_reschedule_appointment, name='doctor_reschedule_appointment'),
    # Lab test booking URLs for front desk
    path('frontdesk/book-lab-test/', views.frontdesk_book_lab_test, name='frontdesk_book_lab_test'),
    path('frontdesk/lab-test-confirmation/<int:booking_id>/', views.frontdesk_lab_test_confirmation, name='frontdesk_lab_test_confirmation'),
    path('frontdesk/lab-bookings/', views.frontdesk_lab_bookings, name='frontdesk_lab_bookings'),
    path('api/frontdesk/get-tests-by-lab/', views.frontdesk_get_tests_by_lab, name='frontdesk_get_tests_by_lab'),
    
    path('frontdesk/patients/add/',          views.frontdesk_add_patient,     name='frontdesk_add_patient'),   
    path('frontdesk/patients/<int:patient_id>/',       views.frontdesk_patients_detail, name='frontdesk_patients_detail'),
    path('frontdesk/patients/<int:patient_id>/edit/',  views.frontdesk_patients_edit,   name='frontdesk_patients_edit'),
    
    
    path('patient/lab-results/', 
     views.patient_lab_results, 
     name='patient_lab_results'),

    path('patient/lab-result/<int:result_id>/', 
        views.patient_lab_result_detail, 
        name='patient_lab_result_detail'),

    path('patient/lab-result/<int:result_id>/download/', 
        views.download_lab_result_pdf, 
        name='download_lab_result_pdf'),
    
    path('lab/booking/<int:booking_id>/', views.lab_booking_detail, name='lab_booking_detail'),
    path(
        'frontdesk/lab-bookings/',
        views.frontdesk_lab_bookings,
        name='frontdesk_lab_bookings',
    ),
    path(
        'frontdesk/lab-test-confirmation/<int:booking_id>/',
        views.frontdesk_lab_test_confirmation,
        name='frontdesk_lab_test_confirmation',
    ),
    
]