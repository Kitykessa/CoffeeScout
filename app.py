import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db_connection
from helpers import login_required

# ===== INIT APP =====
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# ===== CURRENT USER HELPER =====
@app.context_processor
def inject_user():
    if "user_id" in session:
        db = get_db_connection()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
        db.close()
        return dict(current_user=user)
    return dict(current_user=None)

# ===== ROUTES =====
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ----- REGISTER -----
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or password != confirmation:
            flash("Invalid input!")
            return redirect("/register")

        db = get_db_connection()
        existing = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            flash("Username exists")
            db.close()
            return redirect("/register")

        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, hash_pw))
        db.commit()
        user_id = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
        db.close()

        session["user_id"] = user_id
        flash("Registered!")
        return redirect("/")
    return render_template("register.html")

# ----- LOGIN -----
@app.route("/login", methods=["GET","POST"])
def login():
    session.clear()
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db_connection()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        db.close()
        if not user or not check_password_hash(user["password"], password):
            flash("Invalid credentials")
            return redirect("/login")
        session["user_id"] = user["id"]
        flash("Logged in!")
        return redirect("/")
    return render_template("login.html")

# ----- LOGOUT -----
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect("/")

# ----- COFFEES LIST -----
@app.route("/coffees")
def coffees():
    db = get_db_connection()

    # Read filters
    q = request.args.get("q", "")
    roast = request.args.get("roast", "")
    store = request.args.get("store", "")
    origin = request.args.get("origin", "")
    beans = request.args.get("beans", "")

    query = """
        SELECT DISTINCT c.*
        FROM coffee c
        LEFT JOIN coffee_store cs ON c.id = cs.coffee_id
        LEFT JOIN store s ON s.id = cs.store_id
        WHERE 1=1
    """

    params = []

    # ---- FILTERS ----
    if q:
        query += " AND c.name LIKE ?"
        params.append(f"%{q}%")

    if roast:
        query += " AND c.roast = ?"
        params.append(roast)

    if origin:
        query += " AND c.origin = ?"
        params.append(origin)

    if beans:
        query += " AND c.beans = ?"
        params.append(beans)

    if store:
        query += " AND s.store = ?"
        params.append(store)

    coffees = db.execute(query, params).fetchall()

    # ---- DATA FOR SELECTS ----
    roasts = [r["roast"] for r in db.execute("SELECT DISTINCT roast FROM coffee")]
    origins = [o["origin"] for o in db.execute("SELECT DISTINCT origin FROM coffee")]
    beans_types = [b["beans"] for b in db.execute("SELECT DISTINCT beans FROM coffee")]
    stores_list = [s["store"] for s in db.execute("SELECT DISTINCT store FROM store")]

    db.close()

    return render_template(
        "coffees.html",
        coffees=coffees,
        roasts=roasts,
        origins=origins,
        beans_types=beans_types,
        stores=stores_list
    )


# ----- COFFEE DETAIL -----
@app.route("/coffee/<int:coffee_id>")
def coffee_detail(coffee_id):
    db = get_db_connection()
    coffee = db.execute("SELECT * FROM coffee WHERE id=?", (coffee_id,)).fetchone()
    if not coffee:
        db.close()
        return "Coffee not found", 404

    stores = db.execute("""
        SELECT s.store
        FROM store s
        JOIN coffee_store cs ON s.id = cs.store_id
        WHERE cs.coffee_id=?
    """,(coffee_id,)).fetchall()

    reviews = db.execute("""
        SELECT r.*, u.username
        FROM reviews r
        LEFT JOIN users u ON r.user_id=u.id
        WHERE r.coffee_id=?
        ORDER BY r.created_at DESC
    """,(coffee_id,)).fetchall()

    avg_rating = None
    if reviews:
        ratings = [r["rating"] for r in reviews if r["rating"]]
        if ratings:
            avg_rating = sum(ratings)/len(ratings)

    def avg_field(field):
        vals = [r[field] for r in reviews if r[field] is not None]
        return round(sum(vals)/len(vals),1) if vals else 0

    avg_values = {f: avg_field(f) for f in ["aroma","acidity","bitterness","body","finish","roast"]}

    # ======= Notes from users
    notes_list = []
    note_counts = {}
    for r in reviews:
        if r["notes"]:
            try:
                import json
                n = json.loads(r["notes"])
                if isinstance(n, list):
                    notes = n
                else:
                    notes = [str(n)]
            except:
                notes = [x.strip() for x in r["notes"].split(",")]

            for note in notes:
                notes_list.append(note)
                note_counts[note] = note_counts.get(note, 0) + 1

    unique_notes = list(note_counts.keys())

    db.close()
    return render_template(
        "coffee_detail.html",
        coffee=coffee,
        stores=stores,
        reviews=reviews,
        avg_rating=avg_rating,
        avg_values=avg_values,
        avg_notes=unique_notes,
        note_counts=note_counts
    )


# ----- ADD REVIEW -----
@app.route("/coffee/<int:coffee_id>/review", methods=["POST"])
@login_required
def add_review(coffee_id):
    db = get_db_connection()
    user_id = session["user_id"]

    rating = request.form.get("rating")
    aroma = request.form.get("aroma")
    acidity = request.form.get("acidity")
    bitterness = request.form.get("bitterness")
    body = request.form.get("body")
    finish = request.form.get("finish")
    roast = request.form.get("roast")
    notes = request.form.get("notes")
    comment = request.form.get("comment")

    if comment and not rating:
        flash("Please provide rating with comment")
        db.close()
        return redirect(url_for("coffee_detail", coffee_id=coffee_id))

    db.execute("""
        INSERT INTO reviews
        (coffee_id,user_id,rating,aroma,acidity,bitterness,body,finish,roast,notes,comment)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """,(
        coffee_id,user_id,
        int(rating) if rating else None,
        int(aroma) if aroma else None,
        int(acidity) if acidity else None,
        int(bitterness) if bitterness else None,
        int(body) if body else None,
        int(finish) if finish else None,
        int(roast) if roast else None,
        notes,comment
    ))
    db.commit()
    db.close()
    flash("Saved successfully!")
    return redirect(url_for("coffee_detail", coffee_id=coffee_id))




# ----- USER PROFILE -----
@app.route("/user/<int:user_id>")
@login_required
def user_profile(user_id):
    db = get_db_connection()
    
    # User
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        db.close()
        return "User not found", 404

    # Users reviews
    reviews = db.execute("""
        SELECT r.*, c.name AS coffee_name
        FROM reviews r
        JOIN coffee c ON r.coffee_id = c.id
        WHERE r.user_id = ?
        ORDER BY r.created_at DESC
    """, (user_id,)).fetchall()

    db.close()
    
    return render_template("user.html", user=user, reviews=reviews)


# --- CHANGE PASSWORD ---
@app.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    if session.get("user_id") != user_id:
        flash("You can edit only your own profile.", "danger")
        return redirect(url_for("user_profile", user_id=session.get("user_id")))

    db = get_db_connection()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # --- Checks ---
        if not old_password or not new_password or not confirm_password:
            flash("Please fill in all fields.", "warning")
        elif new_password != confirm_password:
            flash("New passwords do not match.", "danger")
        elif not check_password_hash(user["password"], old_password):
            flash("Incorrect current password.", "danger")
        else:
            hashed = generate_password_hash(new_password)
            db.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))
            db.commit()
            db.close()
            flash("Password updated successfully!", "success")
            return redirect(url_for("user_profile", user_id=user_id))

    db.close()
    return render_template("edit_profile.html", user=user)



if __name__=="__main__":
    app.run(debug=True)
