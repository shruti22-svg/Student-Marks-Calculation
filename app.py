import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_results(sub1, sub2, sub3):
    total = round(sub1 + sub2 + sub3, 2)
    average = round(total / 3.0, 2)
    percentage = round((total / 300.0) * 100.0, 2)

    # Determine status and grade
    if sub1 < 35 or sub2 < 35 or sub3 < 35:
        status = "Failed"
        grade = "F"
    elif average >= 90:
        status = "Passed"
        grade = "A+"
    elif average >= 80:
        status = "Passed"
        grade = "A"
    elif average >= 70:
        status = "Passed"
        grade = "B"
    elif average >= 60:
        status = "Passed"
        grade = "C"
    elif average >= 50:
        status = "Passed"
        grade = "D"
    else:
        status = "Passed"
        grade = "E"

    return {
        "sub1": sub1,
        "sub2": sub2,
        "sub3": sub3,
        "total": total,
        "average": average,
        "percentage": percentage,
        "grade": grade,
        "status": status
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    student_name = ""
    sub1_val = ""
    sub2_val = ""
    sub3_val = ""

    if request.method == "POST":
        student_name = request.form.get("student_name", "").strip()
        sub1_str = request.form.get("sub1", "").strip()
        sub2_str = request.form.get("sub2", "").strip()
        sub3_str = request.form.get("sub3", "").strip()

        sub1_val = sub1_str
        sub2_val = sub2_str
        sub3_val = sub3_str

        try:
            if not sub1_str or not sub2_str or not sub3_str:
                raise ValueError("All three subject marks are required.")
            
            sub1 = float(sub1_str)
            sub2 = float(sub2_str)
            sub3 = float(sub3_str)

            if not (0 <= sub1 <= 100 and 0 <= sub2 <= 100 and 0 <= sub3 <= 100):
                raise ValueError("Marks must be between 0 and 100.")

            result = calculate_results(sub1, sub2, sub3)
            result["student_name"] = student_name or "Student"
        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        student_name=student_name,
        sub1=sub1_val,
        sub2=sub2_val,
        sub3=sub3_val
    )

@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    data = request.get_json(force=True, silent=True) or request.form
    try:
        sub1 = float(data.get("sub1"))
        sub2 = float(data.get("sub2"))
        sub3 = float(data.get("sub3"))
        if not (0 <= sub1 <= 100 and 0 <= sub2 <= 100 and 0 <= sub3 <= 100):
            return jsonify({"success": False, "error": "Marks must be between 0 and 100."}), 400
        res = calculate_results(sub1, sub2, sub3)
        res["success"] = True
        return jsonify(res), 200
    except (TypeError, ValueError) as e:
        return jsonify({"success": False, "error": f"Invalid input: {str(e)}"}), 400

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "Student Marks Calculation"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
