# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from dotenv import load_dotenv
# import os, random, time, json
# from serpapi import GoogleSearch

# # ------------------ Configuration ------------------
# load_dotenv()
# app = Flask(__name__, template_folder='templates', static_folder='static')
# app.secret_key = os.getenv('SECRET_KEY', 'devsecret')

# API_KEY = os.getenv("SERPAPI_KEY", "5631e86172890797ad72020452808fc97b38020c37b0e440e2e67b5a3ef5a40d")
# DATA_FILE = "users.json"

# # ------------------ Helper Functions ------------------
# def load_users():
#     """Load users from JSON file"""
#     if not os.path.exists(DATA_FILE):
#         return {}
#     with open(DATA_FILE, "r") as f:
#         return json.load(f)

# def save_users(users):
#     """Save users to JSON file"""
#     with open(DATA_FILE, "w") as f:
#         json.dump(users, f, indent=4)

# # ------------------ Authentication Routes ------------------
# @app.route("/", methods=["GET", "POST"])
# def login():
#     users = load_users()

#     if request.method == "POST":
#         form_type = request.form.get("form_type")

#         # ----- SIGNUP -----
#         if form_type == "signup":
#             username = request.form.get("name").strip()
#             email = request.form.get("email").strip().lower()
#             password = request.form.get("password").strip()

#             if not username or not email or not password:
#                 flash("All fields are required!", "error")
#             elif email in users:
#                 flash("Email already registered!", "error")
#             else:
#                 users[email] = {"name": username, "password": password}
#                 save_users(users)
#                 flash("Signup successful! Please log in.", "success")

#         # ----- LOGIN -----
#         elif form_type == "login":
#             email = request.form.get("email").strip().lower()
#             password = request.form.get("password").strip()

#             if email in users and users[email]["password"] == password:
#              session["user"] = {
#              "name": users[email]["name"],
#              "email": email
#              }
#              flash(f"Welcome back, {session['user']['name']}!", "success")
#              return redirect(url_for("home"))
#             else:
#                 flash("Invalid email or password!", "error")

#     return render_template("login.html")


# @app.route("/logout")
# def logout():
#     session.pop("user", None)
#     flash("Logged out successfully!", "info")
#     return redirect(url_for("login"))


# # ------------------ Helper Logic ------------------
# def mock_intent(query):
#     """Simple keyword-based intent detection"""
#     q = (query or "").lower()
#     if "plumb" in q: return "plumber"
#     if "tutor" in q or "teach" in q: return "tutor"
#     if "mechanic" in q or "car" in q: return "mechanic"
#     if "gym" in q or "trainer" in q: return "trainer"
#     return "general"


# def mock_providers(service, limit=6):
#     """Fallback dummy provider data"""
#     logos = [
#         "/static/images/placeholder.png",
#         "/static/images/plumber.jpg",
#         "/static/images/tutor.jpg",
#         "/static/images/mechanic.jpg"
#     ]
#     providers = []
#     for i in range(limit):
#         providers.append({
#             "id": f"{service}_{i+1}",
#             "name": f"{service.title()} Expert {i+1}",
#             "rating": round(3.6 + random.random() * 1.4, 1),
#             "cost": random.choice([250, 399, 499, 699, 999]),
#             "contact": f"+91-9{random.randint(10000000, 99999999)}",
#             "distance": f"{round(random.uniform(0.5, 8.2), 1)} km",
#             "image": random.choice(logos),
#             "tags": ["Trusted", "Verified"] if i % 2 == 0 else ["Fast", "Local"]
#         })
#     return providers


# def serpapi_providers(query, city, country, limit=6):
#     """Fetch real business data using SerpAPI"""
#     try:
#         params = {
#             "engine": "google_maps",
#             "q": query,
#             "location": f"{city}, {country}",
#             "type": "search",
#             "num": str(limit),
#             "api_key": API_KEY,
#         }

#         search = GoogleSearch(params)
#         results = search.get_dict()
#         providers = []

#         for person in results.get("local_results", [])[:limit]:
#             providers.append({
#                 "name": person.get("title"),
#                 "address": person.get("address", "No address"),
#                 "rating": person.get("rating", "N/A"),
#                 "reviews": person.get("reviews", "No reviews"),
#                 "phone": person.get("phone", "No phone listed"),
#                 "snippet": person.get("snippet", "No description"),
#                 "maps_link": person.get("gps_coordinates", "N/A"),
#                 "tags": [person.get("type", "Local Business")],
#                 "cost": "N/A",
#                 "contact": person.get("phone", "No phone listed"),
#                 "image": person.get("thumbnail", "/static/images/placeholder.png"),
#             })
#         return providers

#     except Exception as e:
#         print("Error fetching from SerpAPI:", e)
#         return []


# # ------------------ Main Routes ------------------
# @app.route("/home")
# def home():
#     if "user" not in session:
#         flash("Please log in to continue.", "info")
#         return redirect(url_for("login"))

#     services = [
#         "plumber", "tutor", "mechanic", "gym trainer",
#         "electrician", "carpenter", "cleaning", "beautician"
#     ]
#     return render_template("home.html", services=services, user=session.get("user"))


# @app.route("/results")
# def results():
#     q = request.args.get("q", "").strip()
#     city = request.args.get("city", "Delhi").strip()
#     country = request.args.get("country", "India").strip()

#     if not q:
#         flash("Enter a query to search (e.g., 'Find a plumber near me').", "info")
#         return redirect(url_for("home"))

#     guest = "user" not in session
#     limit = 3 if guest else 8

#     service = mock_intent(q)
#     providers = serpapi_providers(q, city, country, limit=limit)

#     if not providers:
#         providers = mock_providers(service, limit=limit)

#     return render_template(
#         "results.html",
#         query=q,
#         providers=providers,
#         guest=guest,
#         service=service,
#         user=session.get("user"),
#     )


# @app.route("/services")
# def services():
#     return render_template("services.html", user=session.get("user"))


# @app.route("/about")
# def about():
#     return render_template("about.html", user=session.get("user"))


# @app.route("/book/<provider_id>", methods=["POST"])
# def book(provider_id):
#     name = request.form.get("name", "").strip()
#     contact = request.form.get("contact", "").strip()
#     slot = request.form.get("slot", "").strip()
#     q = request.form.get("q", "")

#     if not (name and contact):
#         flash("Name and contact are required to book.", "danger")
#         return redirect(url_for("results", q=q))

#     booking_id = f"BKG{int(time.time())}{random.randint(10,99)}"
#     flash(f"Booking confirmed — {booking_id}", "success")
#     return redirect(url_for("results", q=q))


# # ------------------ Run the App ------------------
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os, random, time, json
from serpapi import GoogleSearch

# ------------------ Configuration ------------------
load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'devsecret')

API_KEY = os.getenv("SERPAPI_KEY", "5631e86172890797ad72020452808fc97b38020c37b0e440e2e67b5a3ef5a40d")
DATA_FILE = "users.json"

# ------------------ Helper Functions ------------------
def load_users():
    """Load users from JSON file"""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save users to JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ------------------ Authentication Routes ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    users = load_users()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # ----- SIGNUP -----
        if form_type == "signup":
            username = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "").strip()

            if not username or not email or not password:
                flash("All fields are required!", "error")
            elif email in users:
                flash("Email already registered!", "error")
            else:
                users[email] = {"name": username, "password": password}
                save_users(users)
                flash("Signup successful! Please log in.", "success")

        # ----- LOGIN -----
        elif form_type == "login":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "").strip()

            if email in users and users[email]["password"] == password:
                session["user"] = {
                    "name": users[email]["name"],
                    "email": email
                }
                flash(f"Welcome back, {session['user']['name']}!", "success")
                return redirect(url_for("home"))
            else:
                flash("Invalid email or password!", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# ------------------ Helper Logic ------------------
def mock_intent(query):
    """Simple keyword-based intent detection"""
    q = (query or "").lower()
    if "plumb" in q: return "plumber"
    if "tutor" in q or "teach" in q: return "tutor"
    if "mechanic" in q or "car" in q: return "mechanic"
    if "gym" in q or "trainer" in q: return "trainer"
    return "general"

def mock_providers(service, limit=6):
    """Fallback dummy provider data"""
    logos = [
        "/static/images/placeholder.png",
        "/static/images/plumber.jpg",
        "/static/images/tutor.jpg",
        "/static/images/mechanic.jpg"
    ]
    providers = []
    for i in range(limit):
        providers.append({
            "id": f"{service}_{i+1}",
            "name": f"{service.title()} Expert {i+1}",
            "rating": round(3.6 + random.random() * 1.4, 1),
            "cost": random.choice([250, 399, 499, 699, 999]),
            "contact": f"+91-9{random.randint(10000000, 99999999)}",
            "distance": f"{round(random.uniform(0.5, 8.2), 1)} km",
            "image": random.choice(logos),
            "tags": ["Trusted", "Verified"] if i % 2 == 0 else ["Fast", "Local"],
            "address": f"Mock Address {i+1}",
            "maps_link": "N/A"
        })
    return providers

def serpapi_providers(query, city, country, limit=6):
    """Fetch real business data using SerpAPI"""
    try:
        params = {
            "engine": "google_maps",
            "q": query,
            "location": f"{city}, {country}",
            "type": "search",
            "num": str(limit),
            "api_key": API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        providers = []

        for i, person in enumerate(results.get("local_results", [])[:limit]):
            providers.append({
                "id": f"serp_{i}",
                "name": person.get("title"),
                "address": person.get("address", "No address"),
                "rating": person.get("rating", "N/A"),
                "reviews": person.get("reviews", "No reviews"),
                "phone": person.get("phone", "No phone listed"),
                "snippet": person.get("snippet", "No description"),
                "maps_link": person.get("gps_coordinates", "N/A"),
                "tags": [person.get("type", "Local Business")],
                "cost": "N/A",
                "contact": person.get("phone", "No phone listed"),
                "image": person.get("thumbnail", "/static/images/placeholder.png"),
                "distance": person.get("distance", "N/A")
            })
        return providers

    except Exception as e:
        print("Error fetching from SerpAPI:", e)
        return []

# ------------------ Main Routes ------------------
@app.route("/home")
def home():
    if "user" not in session:
        flash("Please log in to continue.", "info")
        return redirect(url_for("login"))

    services = [
        "plumber", "tutor", "mechanic", "gym trainer",
        "electrician", "carpenter", "cleaning", "beautician"
    ]
    return render_template("home.html", services=services, user=session.get("user"))

@app.route("/results")
def results():
    q = request.args.get("q", "").strip()
    city = request.args.get("city", "Delhi").strip()
    country = request.args.get("country", "India").strip()

    if not q:
        flash("Enter a query to search (e.g., 'Find a plumber near me').", "info")
        return redirect(url_for("home"))

    guest = "user" not in session
    limit = 3 if guest else 8

    service = mock_intent(q)
    providers = serpapi_providers(q, city, country, limit=limit)

    if not providers:
        providers = mock_providers(service, limit=limit)

    return render_template(
        "results.html",
        query=q,
        providers=providers,
        guest=guest,
        service=service,
        user=session.get("user"),
    )

@app.route("/services")
def services():
    services_list = [
        "plumber", "tutor", "mechanic", "gym trainer",
        "electrician", "carpenter", "cleaning", "beautician"
    ]
    return render_template("services.html", user=session.get("user"), services=services_list)

@app.route("/about")
def about():
    return render_template("about.html", user=session.get("user"))

@app.route("/book/<provider_id>", methods=["POST"])
def book(provider_id):
    name = request.form.get("name", "").strip()
    contact = request.form.get("contact", "").strip()
    slot = request.form.get("slot", "").strip()
    q = request.form.get("q", "")

    if not (name and contact):
        flash("Name and contact are required to book.", "danger")
        return redirect(url_for("results", q=q))

    booking_id = f"BKG{int(time.time())}{random.randint(10,99)}"
    flash(f"Booking confirmed — {booking_id}", "success")
    return redirect(url_for("results", q=q))

# ------------------ Run the App ------------------
if __name__ == "__main__":
    app.run(debug=True)