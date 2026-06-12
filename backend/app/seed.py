from .extensions import db
from .models import Appeal, Curriculum, CurriculumCourse, Grade, Student
from .services.curriculum_service import create_curriculum


def seed_demo_data():
    if Student.query.first():
        return

    students = [
        Student(student_no="20240001", name="张明", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240002", name="李雨", major="软件工程", class_name="软工2402"),
        Student(student_no="20240003", name="王佳", major="数据科学", class_name="数科2401"),
    ]
    db.session.add_all(students)
    db.session.flush()

    grades = [
        Grade(student=students[0], course_code="CS101", course_name="程序设计基础", credit=4, score=92, semester="2025-2026-1", teacher="陈老师"),
        Grade(student=students[0], course_code="MA101", course_name="高等数学", credit=5, score=86, semester="2025-2026-1", teacher="周老师"),
        Grade(student=students[1], course_code="SE201", course_name="软件工程导论", credit=3, score=78, semester="2025-2026-1", teacher="刘老师"),
        Grade(student=students[1], course_code="CS102", course_name="数据结构", credit=4, score=83, semester="2025-2026-2", teacher="陈老师"),
        Grade(student=students[2], course_code="DS101", course_name="数据分析基础", credit=3, score=88, semester="2025-2026-1", teacher="赵老师"),
    ]
    db.session.add_all(grades)
    db.session.flush()

    db.session.add(
        Appeal(
            grade=grades[2],
            student_no=students[1].student_no,
            reason="期末大题第三题步骤分可能漏算，申请复核。",
            status="pending",
        )
    )
    db.session.flush()

    if not Curriculum.query.first():
        create_curriculum(
            major="计算机科学与技术",
            total_required_credit=140,
            description="计算机科学与技术专业本科培养方案（2024级）",
            courses=[
                {"courseCode": "MA101", "courseName": "高等数学", "credit": 5, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA102", "courseName": "线性代数", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA103", "courseName": "概率论与数理统计", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "CS101", "courseName": "程序设计基础", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "CS102", "courseName": "数据结构", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "CS103", "courseName": "计算机组成原理", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "CS104", "courseName": "操作系统", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "CS105", "courseName": "计算机网络", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "CS106", "courseName": "数据库原理", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "CS107", "courseName": "编译原理", "credit": 3, "courseType": "required", "semesterSuggested": "2027-2028-1"},
                {"courseCode": "CS108", "courseName": "软件工程", "credit": 3, "courseType": "required", "semesterSuggested": "2027-2028-1"},
                {"courseCode": "CS109", "courseName": "算法设计与分析", "credit": 3, "courseType": "required", "semesterSuggested": "2027-2028-2"},
                {"courseCode": "EL201", "courseName": "人工智能导论", "credit": 3, "courseType": "elective", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "EL202", "courseName": "机器学习", "credit": 3, "courseType": "elective", "semesterSuggested": "2027-2028-1"},
                {"courseCode": "EL203", "courseName": "图形学", "credit": 2, "courseType": "elective", "semesterSuggested": "2027-2028-2"},
            ],
        )

        create_curriculum(
            major="软件工程",
            total_required_credit=140,
            description="软件工程专业本科培养方案（2024级）",
            courses=[
                {"courseCode": "MA101", "courseName": "高等数学", "credit": 5, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA102", "courseName": "线性代数", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA103", "courseName": "概率论与数理统计", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "CS101", "courseName": "程序设计基础", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "CS102", "courseName": "数据结构", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "SE201", "courseName": "软件工程导论", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "SE202", "courseName": "软件需求工程", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "SE203", "courseName": "软件设计与体系结构", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "SE204", "courseName": "软件测试与质量保证", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "CS106", "courseName": "数据库原理", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "CS104", "courseName": "操作系统", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "CS105", "courseName": "计算机网络", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "EL201", "courseName": "人工智能导论", "credit": 3, "courseType": "elective", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "EL204", "courseName": "DevOps与持续集成", "credit": 2, "courseType": "elective", "semesterSuggested": "2027-2028-1"},
                {"courseCode": "EL205", "courseName": "微服务架构", "credit": 3, "courseType": "elective", "semesterSuggested": "2027-2028-2"},
            ],
        )

        create_curriculum(
            major="数据科学",
            total_required_credit=140,
            description="数据科学专业本科培养方案（2024级）",
            courses=[
                {"courseCode": "MA101", "courseName": "高等数学", "credit": 5, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA102", "courseName": "线性代数", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "MA103", "courseName": "概率论与数理统计", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "MA104", "courseName": "数学分析", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-2"},
                {"courseCode": "CS101", "courseName": "程序设计基础", "credit": 4, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "DS101", "courseName": "数据分析基础", "credit": 3, "courseType": "required", "semesterSuggested": "2025-2026-1"},
                {"courseCode": "DS102", "courseName": "数据挖掘", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "DS103", "courseName": "机器学习", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "DS104", "courseName": "深度学习", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "DS105", "courseName": "大数据处理技术", "credit": 4, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "DS106", "courseName": "统计学方法", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "CS106", "courseName": "数据库原理", "credit": 3, "courseType": "required", "semesterSuggested": "2026-2027-1"},
                {"courseCode": "EL201", "courseName": "人工智能导论", "credit": 3, "courseType": "elective", "semesterSuggested": "2026-2027-2"},
                {"courseCode": "EL206", "courseName": "自然语言处理", "credit": 3, "courseType": "elective", "semesterSuggested": "2027-2028-1"},
                {"courseCode": "EL207", "courseName": "计算机视觉", "credit": 3, "courseType": "elective", "semesterSuggested": "2027-2028-2"},
            ],
        )

    db.session.commit()
