import { BookCheck, Search, CheckCircle2, XCircle } from "lucide-react";
import { useState } from "react";
import { api } from "../api/client";
import Notice from "../components/Notice";

export default function CurriculumPage() {
  const [studentNo, setStudentNo] = useState("20240001");
  const [progress, setProgress] = useState(null);
  const [notice, setNotice] = useState(null);

  const search = async (event) => {
    event.preventDefault();
    try {
      setProgress(await api.getCurriculumProgress(studentNo));
      setNotice(null);
    } catch (error) {
      setProgress(null);
      setNotice({ type: "error", message: error.message });
    }
  };

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <h1>培养计划进度</h1>
          <p>按专业查看必修课完成情况、选修课完成情况和缺失学分。</p>
        </div>
        <form className="search-bar" onSubmit={search}>
          <input value={studentNo} onChange={(event) => setStudentNo(event.target.value)} placeholder="输入学号" />
          <button type="submit">
            <Search size={18} />
            查询
          </button>
        </form>
      </header>

      <Notice notice={notice} />

      {progress && (
        <>
          {!progress.curriculum ? (
            <div className="panel">
              <div className="panel-head">
                <h2>暂无培养计划</h2>
              </div>
              <p style={{ padding: "1rem" }}>
                该学生（{progress.student.name}，专业：{progress.student.major || "未设置"}）暂无对应的培养方案数据。
              </p>
            </div>
          ) : (
            <>
              <div className="metric-grid">
                <div className="metric">
                  <span>学生</span>
                  <strong>{progress.student.name}</strong>
                </div>
                <div className="metric">
                  <span>专业</span>
                  <strong>{progress.curriculum.major}</strong>
                </div>
                <div className="metric">
                  <span>总学分要求</span>
                  <strong>{progress.progress.overall.totalCredit}</strong>
                </div>
                <div className="metric">
                  <span>已完成学分</span>
                  <strong>{progress.progress.overall.completedCredit}</strong>
                </div>
                <div className="metric">
                  <span>缺失学分</span>
                  <strong className="danger">{progress.progress.overall.missingCredit}</strong>
                </div>
                <div className="metric">
                  <span>完成进度</span>
                  <strong>{progress.progress.overall.percentage}%</strong>
                </div>
              </div>

              <div className="panel">
                <div className="panel-head">
                  <h2>整体进度</h2>
                </div>
                <div style={{ padding: "1rem" }}>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${Math.min(progress.progress.overall.percentage, 100)}%` }}
                    />
                  </div>
                  <p style={{ marginTop: "0.75rem", fontSize: "0.9rem", color: "var(--muted)" }}>
                    {progress.curriculum.description}
                  </p>
                </div>
              </div>

              <div className="split-grid">
                <div className="panel">
                  <div className="panel-head">
                    <h2>
                      <CheckCircle2 size={18} style={{ color: "var(--success)", marginRight: "0.5rem" }} />
                      必修课完成情况
                    </h2>
                    <span className="tag success">
                      {progress.progress.required.completedCourses}/{progress.progress.required.totalCourses} 门 ·{" "}
                      {progress.progress.required.completedCredit}/{progress.progress.required.totalCredit} 学分
                    </span>
                  </div>
                  {progress.progress.required.completedList.length > 0 ? (
                    <table className="data-table compact">
                      <thead>
                        <tr>
                          <th>课程代码</th>
                          <th>课程名称</th>
                          <th>学分</th>
                          <th>成绩</th>
                          <th>修读学期</th>
                        </tr>
                      </thead>
                      <tbody>
                        {progress.progress.required.completedList.map((course) => (
                          <tr key={course.id} className="row-success">
                            <td>{course.courseCode}</td>
                            <td>{course.courseName}</td>
                            <td>{course.credit}</td>
                            <td>{course.score}</td>
                            <td>{course.semester}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p style={{ padding: "1rem", color: "var(--muted)" }}>暂无已完成的必修课</p>
                  )}
                </div>

                <div className="panel">
                  <div className="panel-head">
                    <h2>
                      <XCircle size={18} style={{ color: "var(--danger)", marginRight: "0.5rem" }} />
                      必修课缺失（需补修）
                    </h2>
                    <span className="tag danger">
                      {progress.progress.required.missingCourses} 门 ·{" "}
                      {progress.progress.required.missingCredit} 学分
                    </span>
                  </div>
                  {progress.progress.required.missingList.length > 0 ? (
                    <table className="data-table compact">
                      <thead>
                        <tr>
                          <th>课程代码</th>
                          <th>课程名称</th>
                          <th>学分</th>
                          <th>建议学期</th>
                        </tr>
                      </thead>
                      <tbody>
                        {progress.progress.required.missingList.map((course) => (
                          <tr key={course.id} className="row-danger">
                            <td>{course.courseCode}</td>
                            <td>{course.courseName}</td>
                            <td>{course.credit}</td>
                            <td>{course.semesterSuggested || "—"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p style={{ padding: "1rem", color: "var(--success)" }}>所有必修课已完成！</p>
                  )}
                </div>
              </div>

              {progress.progress.elective.totalCredit > 0 && (
                <div className="panel">
                  <div className="panel-head">
                    <h2>
                      <BookCheck size={18} style={{ color: "var(--accent)", marginRight: "0.5rem" }} />
                      选修课完成情况
                    </h2>
                    <span className="tag accent">
                      已完成 {progress.progress.elective.completedCredit}/
                      {progress.progress.elective.totalCredit} 学分 · 还需{" "}
                      {progress.progress.elective.missingCredit} 学分
                    </span>
                  </div>
                  {progress.progress.elective.completedList.length > 0 ? (
                    <table className="data-table compact">
                      <thead>
                        <tr>
                          <th>课程代码</th>
                          <th>课程名称</th>
                          <th>学分</th>
                          <th>成绩</th>
                          <th>修读学期</th>
                        </tr>
                      </thead>
                      <tbody>
                        {progress.progress.elective.completedList.map((course) => (
                          <tr key={course.id}>
                            <td>{course.courseCode}</td>
                            <td>{course.courseName}</td>
                            <td>{course.credit}</td>
                            <td>{course.score}</td>
                            <td>{course.semester}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  ) : (
                    <p style={{ padding: "1rem", color: "var(--muted)" }}>暂无已完成的选修课</p>
                  )}
                </div>
              )}
            </>
          )}
        </>
      )}
    </section>
  );
}
