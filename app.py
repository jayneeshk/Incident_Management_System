from flask import Flask, render_template, request, redirect, url_for
from db import get_conn

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/incidents")
def view_incidents():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM incidents")
    incidents = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("view.html", incidents=incidents)


@app.route("/create", methods=["GET", "POST"])
def create_incident():
    if request.method == "POST":
        service = request.form["service_name"]
        severity = request.form["severity"]
        desc = request.form["description"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO incidents(service_name,severity,description,status) VALUES (%s,%s,%s,%s)",
            (service, severity, desc, "Open")
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("view_incidents"))

    return render_template("create.html")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_incident(id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    if request.method == "POST":
        status = request.form["status"]
        severity = request.form["severity"]
        description = request.form["description"]

        cur.execute("""
            UPDATE incidents 
            SET status=%s, severity=%s, description=%s
            WHERE incident_id=%s
        """, (status, severity, description, id))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("view_incidents"))

    cur.execute("SELECT * FROM incidents WHERE incident_id=%s", (id,))
    incident = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("update.html", incident=incident)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_incident(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM incidents WHERE incident_id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("view_incidents"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
