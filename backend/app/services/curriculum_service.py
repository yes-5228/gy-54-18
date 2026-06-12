from ..extensions import db
from ..models import Curriculum, CurriculumCourse, Grade, Student


def get_curriculum_by_major(major):
    return Curriculum.query.filter_by(major=major).first()


def list_curricula():
    return Curriculum.query.order_by(Curriculum.major.asc()).all()


def create_curriculum(major, total_required_credit, description="", courses=None):
    curriculum = Curriculum(
        major=major,
        total_required_credit=total_required_credit,
        description=description or "",
    )
    db.session.add(curriculum)
    db.session.flush()

    if courses:
        for course_data in courses:
            course = CurriculumCourse(
                curriculum=curriculum,
                course_code=course_data["courseCode"],
                course_name=course_data["courseName"],
                credit=float(course_data["credit"]),
                course_type=course_data.get("courseType", "required"),
                semester_suggested=course_data.get("semesterSuggested", ""),
            )
            db.session.add(course)

    db.session.commit()
    return curriculum


def get_curriculum_progress(student_no):
    student = Student.query.filter_by(student_no=student_no).first()
    if not student:
        return None

    curriculum = get_curriculum_by_major(student.major)
    if not curriculum:
        return {
            "student": student.to_dict(),
            "curriculum": None,
            "progress": None,
        }

    student_grades = Grade.query.filter_by(student_id=student.id).all()
    passed_grades = [g for g in student_grades if g.score >= 60]
    passed_course_codes = {g.course_code for g in passed_grades}

    required_courses = [c for c in curriculum.courses if c.course_type == "required"]
    completed_required = []
    missing_required = []
    completed_required_credit = 0.0

    for course in required_courses:
        matched_grade = next((g for g in passed_grades if g.course_code == course.course_code), None)
        if matched_grade:
            completed_required.append({
                **course.to_dict(),
                "score": matched_grade.score,
                "semester": matched_grade.semester,
                "completed": True,
            })
            completed_required_credit += course.credit
        else:
            missing_required.append({
                **course.to_dict(),
                "completed": False,
            })

    total_required_credit = sum(c.credit for c in required_courses)
    missing_required_credit = max(0.0, total_required_credit - completed_required_credit)

    progress_percentage = 0.0
    if total_required_credit > 0:
        progress_percentage = round((completed_required_credit / total_required_credit) * 100, 1)

    total_elective_credit = sum(c.credit for c in curriculum.courses if c.course_type == "elective")
    completed_elective = []
    completed_elective_credit = 0.0
    for g in passed_grades:
        matched = next((c for c in curriculum.courses if c.course_code == g.course_code and c.course_type == "elective"), None)
        if matched:
            completed_elective.append({
                **matched.to_dict(),
                "score": g.score,
                "semester": g.semester,
                "completed": True,
            })
            completed_elective_credit += matched.credit
    missing_elective_credit = max(0.0, total_elective_credit - completed_elective_credit)

    overall_completed_credit = completed_required_credit + completed_elective_credit
    overall_total_credit = sum(c.credit for c in curriculum.courses)
    overall_missing_credit = max(0.0, overall_total_credit - overall_completed_credit)
    overall_percentage = 0.0
    if overall_total_credit > 0:
        overall_percentage = round((overall_completed_credit / overall_total_credit) * 100, 1)

    return {
        "student": student.to_dict(),
        "curriculum": {
            "id": curriculum.id,
            "major": curriculum.major,
            "totalRequiredCredit": curriculum.total_required_credit,
            "description": curriculum.description,
        },
        "progress": {
            "overall": {
                "totalCredit": overall_total_credit,
                "completedCredit": overall_completed_credit,
                "missingCredit": overall_missing_credit,
                "percentage": overall_percentage,
            },
            "required": {
                "totalCourses": len(required_courses),
                "completedCourses": len(completed_required),
                "missingCourses": len(missing_required),
                "totalCredit": total_required_credit,
                "completedCredit": completed_required_credit,
                "missingCredit": missing_required_credit,
                "percentage": progress_percentage,
                "completedList": completed_required,
                "missingList": missing_required,
            },
            "elective": {
                "totalCredit": total_elective_credit,
                "completedCredit": completed_elective_credit,
                "missingCredit": missing_elective_credit,
                "completedList": completed_elective,
            },
        },
    }
