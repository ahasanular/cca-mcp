import datetime

from markdown_it.common.html_re import processing

from utils.enhancer import AIEnhancer

report = {
"heading":
"""# Project 'repo_session_h0q7zb0x' Summary
**25** file(s), **40** class(es), **10** function(s), **19** constant(s)
""",
"tree":
"""```
repo_session_h0q7zb0x/
├── /
│   └── manage.py
├── config/
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── config/mixin/
│   ├── __init__.py
│   └── TimeStampMixin.py (TimeStampMixin, ModelMixin)
├── scheduler/
│   ├── config_loader.py (ConfigLoader)
│   ├── models.py (OrmBaseModel, Department, Shift, Section, +6 more)
│   ├── __init__.py
│   ├── scheduleGenerator.py (ScheduleGenerator)
│   ├── tracker.py (Tracker)
│   ├── score.py (ScoreEngine)
│   └── validation.py (ConstraintCheckerEngine)
├── university/
│   ├── models.py (Department, Shift, Section, Room, +6 more)
│   ├── __init__.py
│   ├── apps.py (UniversityConfig)
│   ├── admin.py (DepartmentAdmin, TeacherAdmin, CourseAdmin, RoomAdmin, +6 more)
│   ├── tests.py
│   ├── urls.py
│   └── views.py (GenerateNewRoutineSet)
├── university/management/commands/
│   └── generate.py (Command)
└── university/templatetags/
    ├── custom_filters.py
    └── __init__.py
```""",
"details":
"""```
repo_session_h0q7zb0x/

├── Package:  (1 modules, 0 classes, 1 functions, 0 constants)
│   └── Module: manage.py
│       └── Functions (1):
│           └── main()
│               └── Run administrative tasks.

├── Package: config (5 modules, 0 classes, 0 functions, 18 constants)
│   ├── Module: asgi.py
│   ├── Module: __init__.py
│   ├── Module: settings.py
│   │   ├── Constants (18): BASE_DIR, SECRET_KEY, DEBUG, ALLOWED_HOSTS
│   │   ├──   ... and 14 more
│   ├── Module: urls.py
│   └── Module: wsgi.py

├── Package: config/mixin (2 modules, 2 classes, 0 functions, 0 constants)
│   ├── Module: __init__.py
│   └── Module: TimeStampMixin.py
│       └── Classes (2):
│   │   │   ├── TimeStampMixin (models.Model):
│           └── ModelMixin (TimeStampMixin):

├── Package: scheduler (7 modules, 15 classes, 0 functions, 0 constants)
│   ├── Module: config_loader.py
│   │   ├── Classes (1):
│   │   │   ├── ConfigLoader:
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── load(config_path)
│   ├── Module: models.py
│   │   ├── Classes (10):
│   │   │   ├── OrmBaseModel (BaseModel):
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── __hash__(self)
│   │   │   ├── Department (OrmBaseModel):
│   │   │   ├── Shift (OrmBaseModel):
│   │   │   ├── Section (OrmBaseModel):
│   │   │   ├── ... and 6 more classes
│   ├── Module: __init__.py
│   ├── Module: scheduleGenerator.py
│   │   ├── Classes (1):
│   │   │   ├── ScheduleGenerator:
│   │   │   │   ├── Methods (13):
│   │   │   │   │   ├── __init__(self, constrains, courses, teachers, rooms, time_slots, shift, sections)
│   │   │   │   │   ├── get_filtered_timeslots(self, time_slots, section, teacher)
│   │   │   │   │   ├── get_course_priority(course)
│   │   │   │   │   ├── generate(self)
│   │   │   │   │   ├── try_backtracking(self, unassigned_courses)
│   │   │   │   │   │   ├── Its try to backtrack to the assigned schedule for that section and find the blocking courses and try to Re-arrange the course to see if that can assign the unassigned course. pa...
│   │   │   │   │   ├── try_assign_course(self, course, section)
│   │   │   │   │   ├── get_sections_for_course(self, course)
│   │   │   │   │   ├── ... and 6 more methods
│   ├── Module: tracker.py
│   │   ├── Classes (1):
│   │   │   ├── Tracker:
│   │   │   │   ├── Methods (3):
│   │   │   │   │   ├── __init__(self)
│   │   │   │   │   ├── add_assignment(self, assignment)
│   │   │   │   │   ├── remove_assignment(self, assignment)
│   ├── Module: score.py
│   │   ├── Classes (1):
│   │   │   ├── ScoreEngine:
│   │   │   │   ├── Methods (6):
│   │   │   │   │   ├── __init__(self, constraints, slots, tracker)
│   │   │   │   │   ├── score_assignment(self, assignment, current_assignments)
│   │   │   │   │   ├── _score_minimize_teacher_slot_gap(self, assignment, current_assignments)
│   │   │   │   │   ├── _score_minimize_section_slot_gap(self, assignment, current_assignments)
│   │   │   │   │   ├── _score_load_balancing_between_teacher(self, assignment, current_assignments)
│   │   │   │   │   ├── _score_day_balancing_slots_allocation(self, assignment, current_assignments)
│   └── Module: validation.py
│       └── Classes (1):
│           └── ConstraintCheckerEngine:
│               └── Methods (5):
│   │   │   │   │   ├── __init__(self, constraints)
│   │   │   │   │   ├── is_valid_assignment(self, assignment, current_assignments)
│   │   │   │   │   ├── validate_teacher(self, assignment, current_assignments)
│   │   │   │   │   ├── validate_slot(self, assignment, current_assignments)
│                   └── validate_room(self, assignment, current_assignments)

├── Package: university (7 modules, 22 classes, 4 functions, 1 constants)
│   ├── Module: models.py
│   │   ├── Constants (1): DAYS
│   │   ├── Classes (10):
│   │   │   ├── Department (ModelMixin):
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── __str__(self)
│   │   │   ├── Shift (ModelMixin):
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── __str__(self)
│   │   │   ├── Section (ModelMixin):
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── __str__(self)
│   │   │   ├── Room (ModelMixin):
│   │   │   │   ├── Methods (1):
│   │   │   │   │   ├── __str__(self)
│   │   │   ├── ... and 6 more classes
│   ├── Module: __init__.py
│   ├── Module: apps.py
│   │   ├── Classes (1):
│   │   │   ├── UniversityConfig (AppConfig):
│   ├── Module: admin.py
│   │   ├── Classes (10):
│   │   │   ├── DepartmentAdmin (admin.ModelAdmin):
│   │   │   ├── TeacherAdmin (admin.ModelAdmin):
│   │   │   │   ├── Methods (2):
│   │   │   │   │   ├── get_queryset(self, request)
│   │   │   │   │   ├── get_distribution(self, obj)
│   │   │   ├── CourseAdmin (admin.ModelAdmin):
│   │   │   │   ├── Methods (2):
│   │   │   │   │   ├── get_queryset(self, request)
│   │   │   │   │   ├── get_total_assignment(self, obj)
│   │   │   ├── RoomAdmin (admin.ModelAdmin):
│   │   │   │   ├── Methods (2):
│   │   │   │   │   ├── get_queryset(self, request)
│   │   │   │   │   ├── get_total_assignment(self, obj)
│   │   │   ├── ... and 6 more classes
│   ├── Module: tests.py
│   ├── Module: urls.py
│   └── Module: views.py
│       └── Functions (4):
│   │   │   ├── routine_test_view(request)
│   │   │   ├── public_routine_view(request, shift_id)
│   │   │   ├── teacher_routine_view(request, *args, **kwargs)
│           └── generate_routine_pdf(request, shift_id)
│       └── Classes (1):
│           └── GenerateNewRoutineSet (View):
│               └── Django class-based view that runs a management command and redirects back to the referring URL.
│               └── Methods (1):
│                   └── get(self, request, *args, **kwargs)

├── Package: university/management/commands (1 modules, 1 classes, 0 functions, 0 constants)
│   └── Module: generate.py
│       └── Classes (1):
│           └── Command (BaseCommand):
│               └── Methods (5):
│   │   │   │   │   ├── clear_previous_assignments(shift)
│   │   │   │   │   │   ├── Reset assignment and assignment-related flags in all relevant models.
│   │   │   │   │   ├── add_arguments(self, parser)
│   │   │   │   │   ├── handle(self, *args, **options)
│   │   │   │   │   ├── save_routine(self, assignments)
│                   └── initialize_data(shift, *args, **kwargs)

├── Package: university/templatetags (2 modules, 0 classes, 5 functions, 0 constants)
│   ├── Module: custom_filters.py
│   │   ├── Functions (5):
│   │   │   ├── get_item(dictionary, key)
│   │   │   ├── match_slot(assignments, args)
│   │   │   │   ├── Return the first assignment matching semester and slot number.
│   │   │   ├── get_matched_assignment(assignments, semester, slot_number)
│   │   │   ├── times(number)
│   │   │   │   ├── Repeat filter for a given number.
│   │   │   ├── ... and 1 more functions
│   └── Module: __init__.py
```"""
}
start = datetime.datetime.now()
enhancer = AIEnhancer(model="deepseek-coder:6.7b")
enhanced = enhancer.enhance(report)
end = datetime.datetime.now()

processing_time = end - start

print(enhanced)
print("Type == ", type(enhanced))
print("Done processing >>> ", processing_time)