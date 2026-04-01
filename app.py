from flask import Flask, request, render_template_string
import csv
import os
from datetime import datetime, timedelta
def now_kst():
    return datetime.utcnow() + timedelta(hours=9)

app = Flask(__name__)

# ---------------- 시간 설정 ----------------
START_TIME = datetime(2026, 4, 1, 9, 0)
DEADLINE = datetime(2026, 4, 5, 23, 59)

# ---------------- 파일 설정 ----------------
CSV_FILE = "survey.csv"

# ---------------- 문항별 과목 목록 ----------------
# 선택13: 모두 3학점, 총 12학점이 되도록 선택
subjects_q1 = [
    ("문학과 영상", 3),
    ("미적분II", 3),
    ("세계 문화와 영어", 3),
    ("동아시아 역사 기행", 3),
    ("정치", 3),
    ("윤리와 사상", 3),
    ("여행지리", 3),
    ("역사로 탐구하는 현대 세계", 3),
    ("윤리문제 탐구", 3),
    ("역학과 에너지", 3),
    ("전자기와 양자", 3),
    ("물질과 에너지", 3),
    ("화학 반응의 세계", 3),
    ("세포와 물질대사", 3),
    ("생물의 유전", 3),
    ("지구시스템과학", 3),
    ("행성우주과학", 3)
]

# 선택14: 모두 3학점, 총 12학점이 되도록 선택
subjects_q2 = [
    ("문학과 영상", 3),
    ("인공지능 수학", 3),
    ("세계 문화와 영어", 3),
    ("동아시아 역사 기행", 3),
    ("정치", 3),
    ("윤리와 사상", 3),
    ("여행지리", 3),
    ("역사로 탐구하는 현대 세계", 3),
    ("윤리문제 탐구", 3),
    ("과학의 역사와 문화", 3),
    ("기후변화와 환경생태", 3),
    ("융합과학 탐구", 3),
]

# 선택15: 최대 2개, 총 4학점이 되도록 선택
subjects_q3 = [
    ("데이터 과학", 4),
    ("심화 중국어", 4),
    ("심화 일본어", 4),
    ("논리와 사고", 2),
    ("인간과 심리", 2),
    ("교육의 이해", 2),
    ("보건", 2),
    ("인간과 경제활동", 2),
    ("논술", 2),
]

# 선택16: 최대 2개, 총 4학점이 되도록 선택
subjects_q4 = [
    ("소프트웨어와 생활", 4),
    ("중국 문화", 4),
    ("일본 문화", 4),
    ("논리와 사고", 2),
    ("인간과 심리", 2),
    ("교육의 이해", 2),
    ("보건", 2),
    ("인간과 경제활동", 2),
    ("논술", 2),
]

subject_credit_q1 = {name: credit for name, credit in subjects_q1}
subject_credit_q2 = {name: credit for name, credit in subjects_q2}
subject_credit_q3 = {name: credit for name, credit in subjects_q3}
subject_credit_q4 = {name: credit for name, credit in subjects_q4}

# ---------------- 과목별 정원 설정 ----------------
subject_limit = {
    "문학과 영상": 300,
    "미적분II": 300,
    "세계 문화와 영어": 300,
    "동아시아 역사 기행": 300,
    "정치": 300,
    "윤리와 사상": 300,
    "여행지리": 300,
    "역사로 탐구하는 현대 세계": 300,
    "윤리문제 탐구": 300,
    "역학과 에너지":300,
    "전자기와 양자":300,
    "물질과 에너지":300,
    "화학 반응의 세계":300,
    "세포와 물질대사":300,
    "생물의 유전":300,
    "지구시스템과학":300,
    "행성우주과학":300,

    "문학과 영상": 300,
    "인공지능 수학": 300,
    "세계 문화와 영어": 300,
    "동아시아 역사 기행": 300,
    "정치": 300,
    "윤리와 사상": 300,
    "여행지리": 300,
    "역사로 탐구하는 현대 세계": 300,
    "윤리문제 탐구": 300,
    "과학의 역사와 문화":300,
    "기후변화와 환경생태":300,
    "융합과학 탐구":300,
   
    "데이터 과학": 300,
    "심화 중국어": 300,
    "심화 일본어": 300,
    "논리와 사고": 300,
    "인간과 심리": 300,
    "교육의 이해": 300,
    "보건": 300,
    "인간과 경제활동": 300,
    "논술": 300,

    "소프트웨어와 생활": 300,
    "중국 문화": 300,
    "일본 문화": 300,
    "논리와 사고": 300,
    "인간과 심리": 300,
    "교육의 이해": 300,
    "보건": 300,
    "인간과 경제활동": 300,
    "논술": 300
}

# ---------------- CSV 파일 생성 ----------------
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "학번", "비밀번호",
            "선택13 선택과목", "선택13 총학점",
            "선택14 선택과목", "선택14 총학점",
            "선택15 선택과목", "선택15 총학점",
            "선택16 선택과목", "선택16 총학점",
            "제출시간"
        ])

# ---------------- HTML ----------------
html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>수요조사</title>
  <style>
    .closed {
      color: gray;
    }
  </style>
</head>
<body>
  <h2>2027학년도 3학년 선택과목 수요조사(1차)</h2>
  <p>시작 시간: {{ start_time }}</p>
  <p>마감 시간: {{ deadline }}</p>

  {% if message %}
    <p><strong>{{ message }}</strong></p>
  {% endif %}

  <form method="post" onsubmit="return checkForm()">
    학번: <input type="text" name="student_id" value="{{ student_id }}" required>
    <br><br>

    비밀번호(숫자 4자리):
    <input type="password" name="password" value="{{ password }}" maxlength="4" required>
    <button type="submit" name="action" value="load">불러오기</button>
    <br><br>

    <h3>선택13 (총 4개 선택)</h3>
    {% for sub, credit in subjects_q1 %}
      <label class="{% if disabled_subjects[sub] and sub not in selected_q1 %}closed{% endif %}">
        <input
          type="checkbox"
          name="q1_subject"
          value="{{ sub }}"
          data-credit="{{ credit }}"
          {% if sub in selected_q1 %}checked{% endif %}
          {% if disabled_subjects[sub] and sub not in selected_q1 %}disabled{% endif %}
        >
        {{ sub }} ({{ credit }}학점 /
        {% if remaining[sub] > 0 %}
          남은 자리: {{ remaining[sub] }}
        {% else %}
          <strong>마감</strong>
        {% endif %}
        )
      </label><br>
    {% endfor %}

    <br>
    <h3>선택14 (총 4개 선택)</h3>
    {% for sub, credit in subjects_q2 %}
      <label class="{% if disabled_subjects[sub] and sub not in selected_q2 %}closed{% endif %}">
        <input
          type="checkbox"
          name="q2_subject"
          value="{{ sub }}"
          data-credit="{{ credit }}"
          {% if sub in selected_q2 %}checked{% endif %}
          {% if disabled_subjects[sub] and sub not in selected_q2 %}disabled{% endif %}
        >
        {{ sub }} ({{ credit }}학점 /
        {% if remaining[sub] > 0 %}
          남은 자리: {{ remaining[sub] }}
        {% else %}
          <strong>마감</strong>
        {% endif %}
        )
      </label><br>
    {% endfor %}

    <br>
    <h3>선택15 (최대 2개, 총 4학점이 되어야 함)</h3>
    {% for sub, credit in subjects_q3 %}
      <label class="{% if disabled_subjects[sub] and sub not in selected_q3 %}closed{% endif %}">
        <input
          type="checkbox"
          name="q3_subject"
          value="{{ sub }}"
          data-credit="{{ credit }}"
          {% if sub in selected_q3 %}checked{% endif %}
          {% if disabled_subjects[sub] and sub not in selected_q3 %}disabled{% endif %}
        >
        {{ sub }} ({{ credit }}학점 /
        {% if remaining[sub] > 0 %}
          남은 자리: {{ remaining[sub] }}
        {% else %}
          <strong>마감</strong>
        {% endif %}
        )
      </label><br>
    {% endfor %}

    <br>
    <h3>선택16 (최대 2개, 총 4학점이 되어야 함)</h3>
    {% for sub, credit in subjects_q4 %}
      <label class="{% if disabled_subjects[sub] and sub not in selected_q4 %}closed{% endif %}">
        <input
          type="checkbox"
          name="q4_subject"
          value="{{ sub }}"
          data-credit="{{ credit }}"
          {% if sub in selected_q4 %}checked{% endif %}
          {% if disabled_subjects[sub] and sub not in selected_q4 %}disabled{% endif %}
        >
        {{ sub }} ({{ credit }}학점 /
        {% if remaining[sub] > 0 %}
          남은 자리: {{ remaining[sub] }}
        {% else %}
          <strong>마감</strong>
        {% endif %}
        )
      </label><br>
    {% endfor %}

    <br>
    <button type="submit" name="action" value="save">제출 / 수정</button>
  </form>

  <script>
    function sumCredits(name) {
      let total = 0;
      let checked = document.querySelectorAll('input[name="' + name + '"]:checked');
      checked.forEach(box => {
        total += parseInt(box.dataset.credit);
      });
      return total;
    }

    function countChecked(name) {
      return document.querySelectorAll('input[name="' + name + '"]:checked').length;
    }

    function checkForm() {
      const activeElement = document.activeElement;
      const studentId = document.querySelector('input[name="student_id"]').value.trim();
      const password = document.querySelector('input[name="password"]').value.trim();

      if (studentId === "") {
        alert("학번을 입력하세요!");
        return false;
      }

      if (!/^\\d{4}$/.test(password)) {
        alert("비밀번호는 숫자 4자리로 입력하세요!");
        return false;
      }

      if (activeElement && activeElement.value === "load") {
        return true;
      }

      let q1Total = sumCredits("q1_subject");
      let q2Total = sumCredits("q2_subject");
      let q3Total = sumCredits("q3_subject");
      let q4Total = sumCredits("q4_subject");

      let q3Count = countChecked("q3_subject");
      let q4Count = countChecked("q4_subject");

      if (q1Total !== 12) {
        alert("선택13은 4개를 선택해야 합니다!");
        return false;
      }

      if (q2Total !== 12) {
        alert("선택14는 4개를 선택해야 합니다!");
        return false;
      }

      if (q3Count === 0) {
        alert("선택15에서 최소 1개는 선택하세요!");
        return false;
      }

      if (q4Count === 0) {
        alert("선택16에서 최소 1개는 선택하세요!");
        return false;
      }

      if (q3Total !== 4) {
        alert("선택15의 총 학점이 4학점이 되어야 합니다!");
        return false;
      }

      if (q4Total !== 4) {
        alert("선택16의 총 학점이 4학점이 되어야 합니다!");
        return false;
      }

      if (q3Count > 2) {
        alert("선택15는 최대 2개까지만 선택 가능합니다!");
        return false;
      }

      if (q4Count > 2) {
        alert("선택16은 최대 2개까지만 선택 가능합니다!");
        return false;
      }

      return true;
    }
  </script>
</body>
</html>
"""

# ---------------- CSV 전체 읽기 ----------------
def read_all_rows():
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 11:
                    rows.append(row)
    return rows

# ---------------- CSV 전체 저장 ----------------
def write_all_rows(rows):
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "학번", "비밀번호",
            "선택13 선택과목", "선택13 총학점",
            "선택14 선택과목", "선택14 총학점",
            "선택15 선택과목", "선택15 총학점",
            "선택16 선택과목", "선택16 총학점",
            "제출시간"
        ])
        writer.writerows(rows)

# ---------------- 특정 학번 찾기 ----------------
def find_student(student_id):
    rows = read_all_rows()
    for i, row in enumerate(rows):
        if row[0] == student_id:
            return i, row, rows
    return None, None, rows

# ---------------- 총학점 계산 ----------------
def calculate_total(selected_subjects, credit_dict):
    total = 0
    for subject in selected_subjects:
        total += credit_dict.get(subject, 0)
    return total

# ---------------- 비밀번호 검사 ----------------
def is_valid_password(password):
    return password.isdigit() and len(password) == 4

# ---------------- 현재 과목별 신청 인원 계산 ----------------
def get_subject_counts(rows):
    counts = {subject: 0 for subject in subject_limit.keys()}

    for row in rows:
        q1_list = [s.strip() for s in row[2].split(",") if s.strip()] if row[2] else []
        q2_list = [s.strip() for s in row[4].split(",") if s.strip()] if row[4] else []
        q3_list = [s.strip() for s in row[6].split(",") if s.strip()] if row[6] else []
        q4_list = [s.strip() for s in row[8].split(",") if s.strip()] if row[8] else []

        for subject in q1_list + q2_list + q3_list + q4_list:
            if subject in counts:
                counts[subject] += 1

    return counts

# ---------------- 남은 자리 계산 ----------------
def get_remaining_seats(rows):
    counts = get_subject_counts(rows)
    remaining = {}

    for subject, limit in subject_limit.items():
        remaining[subject] = max(0, limit - counts.get(subject, 0))

    return remaining

# ---------------- 비활성화 여부 계산 ----------------
def get_disabled_subjects(rows, selected_subjects_all=None):
    if selected_subjects_all is None:
        selected_subjects_all = []

    remaining = get_remaining_seats(rows)
    disabled = {}

    for subject in subject_limit.keys():
        disabled[subject] = (remaining[subject] <= 0 and subject not in selected_subjects_all)

    return disabled

# ---------------- 정원 초과 검사 ----------------
def check_subject_limit(rows, old_selected_all, new_selected_all):
    counts = get_subject_counts(rows)

    for subject in old_selected_all:
        if subject in counts:
            counts[subject] -= 1

    full_subjects = []
    for subject in new_selected_all:
        if subject in subject_limit and counts.get(subject, 0) >= subject_limit[subject]:
            full_subjects.append(subject)
        else:
            counts[subject] = counts.get(subject, 0) + 1

    return full_subjects

# ---------------- 메인 페이지 ----------------
@app.route("/", methods=["GET", "POST"])
def survey():
    now = now_kst()

    if now < START_TIME:
        return f"⏳ 아직 설문 시작 전입니다.<br>시작 시간: {START_TIME}"

    if now > DEADLINE:
        return f"⛔ 설문이 마감되었습니다.<br>마감 시간: {DEADLINE}"

    student_id = ""
    password = ""
    selected_q1 = []
    selected_q2 = []
    selected_q3 = []
    selected_q4 = []
    message = ""

    rows = read_all_rows()
    selected_all = selected_q1 + selected_q2 + selected_q3 + selected_q4
    remaining = get_remaining_seats(rows)
    disabled_subjects = get_disabled_subjects(rows, selected_all)

    if request.method == "POST":
        action = request.form.get("action")
        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "").strip()

        if not student_id:
            message = "학번을 입력하세요."
            return render_template_string(
                html,
                student_id=student_id,
                password=password,
                selected_q1=selected_q1,
                selected_q2=selected_q2,
                selected_q3=selected_q3,
                selected_q4=selected_q4,
                message=message,
                start_time=START_TIME,
                deadline=DEADLINE,
                subjects_q1=subjects_q1,
                subjects_q2=subjects_q2,
                subjects_q3=subjects_q3,
                subjects_q4=subjects_q4,
                remaining=remaining,
                disabled_subjects=disabled_subjects
            )

        if not is_valid_password(password):
            message = "비밀번호는 숫자 4자리로 입력하세요."
            return render_template_string(
                html,
                student_id=student_id,
                password=password,
                selected_q1=selected_q1,
                selected_q2=selected_q2,
                selected_q3=selected_q3,
                selected_q4=selected_q4,
                message=message,
                start_time=START_TIME,
                deadline=DEADLINE,
                subjects_q1=subjects_q1,
                subjects_q2=subjects_q2,
                subjects_q3=subjects_q3,
                subjects_q4=subjects_q4,
                remaining=remaining,
                disabled_subjects=disabled_subjects
            )

        index, row, rows = find_student(student_id)

        if action == "load":
            if row:
                saved_password = row[1].replace("'", "")
                if password != saved_password:
                    message = "비밀번호가 일치하지 않습니다."
                    return render_template_string(
                        html,
                        student_id=student_id,
                        password="",
                        selected_q1=[],
                        selected_q2=[],
                        selected_q3=[],
                        selected_q4=[],
                        message=message,
                        start_time=START_TIME,
                        deadline=DEADLINE,
                        subjects_q1=subjects_q1,
                        subjects_q2=subjects_q2,
                        subjects_q3=subjects_q3,
                        subjects_q4=subjects_q4,
                        remaining=remaining,
                        disabled_subjects=disabled_subjects
                    )

                selected_q1 = row[2].split(",") if row[2] else []
                selected_q2 = row[4].split(",") if row[4] else []
                selected_q3 = row[6].split(",") if row[6] else []
                selected_q4 = row[8].split(",") if row[8] else []

                message = f"기존 제출 내용을 불러왔습니다. 마지막 제출 시간: {row[10]}"
            else:
                message = "기존 제출 내용이 없습니다. 현재 입력한 비밀번호로 새 제출이 저장됩니다."

            selected_all = selected_q1 + selected_q2 + selected_q3 + selected_q4
            remaining = get_remaining_seats(rows)
            disabled_subjects = get_disabled_subjects(rows, selected_all)

            return render_template_string(
                html,
                student_id=student_id,
                password=password,
                selected_q1=selected_q1,
                selected_q2=selected_q2,
                selected_q3=selected_q3,
                selected_q4=selected_q4,
                message=message,
                start_time=START_TIME,
                deadline=DEADLINE,
                subjects_q1=subjects_q1,
                subjects_q2=subjects_q2,
                subjects_q3=subjects_q3,
                subjects_q4=subjects_q4,
                remaining=remaining,
                disabled_subjects=disabled_subjects
            )

        if action == "save":
            selected_q1 = request.form.getlist("q1_subject")
            selected_q2 = request.form.getlist("q2_subject")
            selected_q3 = request.form.getlist("q3_subject")
            selected_q4 = request.form.getlist("q4_subject")

            q1_total = calculate_total(selected_q1, subject_credit_q1)
            q2_total = calculate_total(selected_q2, subject_credit_q2)
            q3_total = calculate_total(selected_q3, subject_credit_q3)
            q4_total = calculate_total(selected_q4, subject_credit_q4)

            if q1_total != 12:
                message = "❌ 선택13은 4개를 선택해야 합니다."
            elif q2_total != 12:
                message = "❌ 선택14는 4개를 선택해야 합니다."
            elif len(selected_q3) == 0:
                message = "❌ 선택15에서 최소 1개는 선택하세요."
            elif len(selected_q4) == 0:
                message = "❌ 선택16에서 최소 1개는 선택하세요."
            elif q3_total != 4:
                message = "❌ 선택15의 총 학점이 4학점이 되어야 합니다."
            elif q4_total != 4:
                message = "❌ 선택16의 총 학점이 4학점이 되어야 합니다."
            elif len(selected_q3) > 2:
                message = "❌ 선택15는 최대 2개까지만 선택 가능합니다."
            elif len(selected_q4) > 2:
                message = "❌ 선택16은 최대 2개까지만 선택 가능합니다."
            else:
                old_selected_all = []
                if row:
                    saved_password = row[1].replace("'", "")
                    if password != saved_password:
                        message = "비밀번호가 일치하지 않아 수정할 수 없습니다."
                        return render_template_string(
                            html,
                            student_id=student_id,
                            password="",
                            selected_q1=[],
                            selected_q2=[],
                            selected_q3=[],
                            selected_q4=[],
                            message=message,
                            start_time=START_TIME,
                            deadline=DEADLINE,
                            subjects_q1=subjects_q1,
                            subjects_q2=subjects_q2,
                            subjects_q3=subjects_q3,
                            subjects_q4=subjects_q4,
                            remaining=remaining,
                            disabled_subjects=disabled_subjects
                        )

                    old_q1 = row[2].split(",") if row[2] else []
                    old_q2 = row[4].split(",") if row[4] else []
                    old_q3 = row[6].split(",") if row[6] else []
                    old_q4 = row[8].split(",") if row[8] else []
                    old_selected_all = old_q1 + old_q2 + old_q3 + old_q4

                new_selected_all = selected_q1 + selected_q2 + selected_q3 + selected_q4

                full_subjects = check_subject_limit(rows, old_selected_all, new_selected_all)
                if full_subjects:
                    message = "⚠️ 다음 과목은 정원이 마감되어 선택할 수 없습니다: " + ", ".join(full_subjects)
                    selected_all = new_selected_all
                    remaining = get_remaining_seats(rows)
                    disabled_subjects = get_disabled_subjects(rows, selected_all)
                    return render_template_string(
                        html,
                        student_id=student_id,
                        password=password,
                        selected_q1=selected_q1,
                        selected_q2=selected_q2,
                        selected_q3=selected_q3,
                        selected_q4=selected_q4,
                        message=message,
                        start_time=START_TIME,
                        deadline=DEADLINE,
                        subjects_q1=subjects_q1,
                        subjects_q2=subjects_q2,
                        subjects_q3=subjects_q3,
                        subjects_q4=subjects_q4,
                        remaining=remaining,
                        disabled_subjects=disabled_subjects
                    )

                submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [
                    student_id,
                    "'" + password,
                    ",".join(selected_q1), q1_total,
                    ",".join(selected_q2), q2_total,
                    ",".join(selected_q3), q3_total,
                    ",".join(selected_q4), q4_total,
                    submitted_at
                ]

                if row:
                    rows[index] = new_row
                    message = "✅ 기존 제출 내용이 수정되었습니다."
                else:
                    rows.append(new_row)
                    message = "✅ 제출이 완료되었습니다."

                write_all_rows(rows)
                rows = read_all_rows()
                selected_all = new_selected_all
                remaining = get_remaining_seats(rows)
                disabled_subjects = get_disabled_subjects(rows, selected_all)

            return render_template_string(
                html,
                student_id=student_id,
                password=password,
                selected_q1=selected_q1,
                selected_q2=selected_q2,
                selected_q3=selected_q3,
                selected_q4=selected_q4,
                message=message,
                start_time=START_TIME,
                deadline=DEADLINE,
                subjects_q1=subjects_q1,
                subjects_q2=subjects_q2,
                subjects_q3=subjects_q3,
                subjects_q4=subjects_q4,
                remaining=remaining,
                disabled_subjects=disabled_subjects
            )

    return render_template_string(
        html,
        student_id=student_id,
        password=password,
        selected_q1=selected_q1,
        selected_q2=selected_q2,
        selected_q3=selected_q3,
        selected_q4=selected_q4,
        message=message,
        start_time=START_TIME,
        deadline=DEADLINE,
        subjects_q1=subjects_q1,
        subjects_q2=subjects_q2,
        subjects_q3=subjects_q3,
        subjects_q4=subjects_q4,
        remaining=remaining,
        disabled_subjects=disabled_subjects
    )

# ---------------- 실행 ----------------
app.run(host="0.0.0.0", port=5000, debug=True)
