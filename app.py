from flask import Flask, render_template, request, redirect, url_for
from db import get_conn
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


def get_gemini_client():
    try:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            print("GEMINI_API_KEY not set in environment")
            return None

        genai.configure(api_key=key)
        print("Gemini client configured")
        return genai

    except Exception as e:
        print("Failed to initialize Gemini:", e)
        return None

def call_gemini(prompt):
    client = get_gemini_client()
    if client:
        try:
            # Updated model version
            model = client.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            # Robust handling: text or content
            ai_insights = getattr(response, "text", None) or getattr(response, "content", None) or "No response from AI"
            return ai_insights.strip()
        except Exception as e:
            print("Gemini API error:", e)
            return "AI insights not available due to API error."
    return "AI insights not available (client not initialized)."


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/incidents")
def view_incidents():
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM incidents")
        incidents = cur.fetchall()
    except Exception as e:
        print("DB error:", e)
        incidents = []
    finally:
        cur.close()
        conn.close()
    return render_template("view.html", incidents=incidents)

@app.route("/create", methods=["GET", "POST"])
def create_incident():
    if request.method == "POST":
        service = request.form.get("service_name", "N/A")
        severity = request.form.get("severity", "N/A")
        desc = request.form.get("description", "N/A")
        error = request.form.get("error", "N/A")
        logs = request.form.get("logs", "N/A")
        impact = request.form.get("impact", "N/A")

        # ----- Prepare concise AI prompt -----
        prompt = f"""
An incident occurred in production. Keep the response very short, clean, and in bullet points:
Service: {service}
Error: {error}
Logs: {logs}
Impact: {impact}
Severity: {severity}
Description: {desc}

Provide:
- summary of the problem
- Top 2 possible root causes
- 2-3 troubleshooting steps
- Suggested fixes (1-2 points)
- Preventive measures (1-2 points)

Return only bullet points, no extra explanation.
"""

        # ----- Call Gemini API -----
        ai_insights = call_gemini(prompt)

        # Optional: split by lines to remove empty lines
        ai_insights = "\n".join([line.strip() for line in ai_insights.splitlines() if line.strip()])

        # ----- Save incident + AI insights -----
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO incidents(service_name,severity,description,status,ai_insights) "
                "VALUES (%s,%s,%s,%s,%s)",
                (service, severity, desc, "Open", ai_insights)
            )
            conn.commit()
        except Exception as e:
            print("DB insert error:", e)
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("view_incidents"))

    return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_incident(id):
    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        if request.method == "POST":
            status = request.form.get("status", "Open")
            severity = request.form.get("severity", "N/A")
            description = request.form.get("description", "N/A")

            cur.execute(
                "UPDATE incidents SET status=%s, severity=%s, description=%s WHERE incident_id=%s",
                (status, severity, description, id)
            )
            conn.commit()
            return redirect(url_for("view_incidents"))

        cur.execute("SELECT * FROM incidents WHERE incident_id=%s", (id,))
        incident = cur.fetchone()
    except Exception as e:
        print("DB error:", e)
        incident = None
    finally:
        cur.close()
        conn.close()

    return render_template("update.html", incident=incident)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_incident(id):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM incidents WHERE incident_id=%s", (id,))
        conn.commit()
    except Exception as e:
        print("DB delete error:", e)
    finally:
        cur.close()
        conn.close()
    return redirect(url_for("view_incidents"))

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)