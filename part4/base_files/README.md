Ah! Got it 😅 I left placeholders, but you want the actual paths to the images you shared. Let’s update your README so it references your real images from `static/images/`. Here's the revised version:

---

# 🏠 HBnB - Holberton School Project Part 4

A simple accommodation booking platform built with **Flask**, **JavaScript**, **HTML5**, and **CSS3**. This project implements the **front-end part** of the HBnB app, featuring user authentication, dynamic place listings, detailed place pages, and a review system.

---

## 📋 Project Description

HBnB (Holberton BnB) allows users to:

* Login with authentication
* View a list of places and filter by price
* See detailed information for each place
* Submit reviews (authenticated users only)
* Enjoy a responsive design

---

## 🚀 Technologies Used

* **Backend:** Flask (Python)
* **Frontend:** HTML5, CSS3, **JavaScript**
* **API:** RESTful API with JWT authentication
* **Styling:** Custom CSS
* **Storage:** Cookie-based JWT token management

---

## 📁 Project Structure

```
hbnb/
├── app.py                  # Flask application and API routes
├── templates/              # HTML templates
│   ├── index.html          # List of places
│   ├── login.html          # Login form
│   ├── place.html          # Place details
│   └── add_review.html     # Add review form
├── static/                 # Static files
│   ├── styles.css          # Main stylesheet
│   ├── scripts.js          # JS functionality
│   └── images/             # Images (logo, places, icons, etc.)
└── README.md               # This file
```

---

## 🔧 Installation & Setup

### Prerequisites

* Python 3.8+
* Flask installed (`pip install flask`)

### Steps

1. **Clone the repository:**

```bash
git clone https://github.com/omarrui/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4/hbnb
```

2. **Install dependencies:**

```bash
pip install flask
```

3. **Run the Flask application:**

```bash
python app.py
```

4. **Open your browser:**

```
http://localhost:3000
```

---

## 🧪 How to Test

### 1. Login Page

**Steps:**

1. Go to `http://localhost:3000/login`
2. Enter email and password
3. Click "Login"

**Expected Results:**

* ✅ JWT token stored in browser cookie
* ✅ Redirected to homepage
* ✅ "Login" button replaced by "Logout"

**Screenshot:**
![Login Page](static/images/login.png)

---

### 2. Home / List of Places

**Steps:**

1. Navigate to `http://localhost:3000/`
2. **Expected Results:**

   * ✅ List of places displayed
   * ✅ Each card shows: image, name, price, host, "View Details" button
   * ✅ "Login" button visible if not logged in, "Logout" if logged in

**Screenshot:**
![Home Page](static/images/home.png)
![Place Card](static/images/palce\ card.png)

---

### 3. Place Details Page

**Steps:**

1. Click "View Details" on a place card

**Expected Results:**

* ✅ Place name, host, price, description displayed
* ✅ Amenities list shown
* ✅ Reviews displayed
* ✅ "Add Review" button visible if logged in

**Screenshots:**
![Place Details](static/images/image1.jpg)
![Amenities Icons](static/images/icon_bed.png)
![Amenities Icons](static/images/icon_bath.png)
![Amenities Icons](static/images/icon_wifi.png)

---

### 4. Add Review Page

**Steps:**

1. Click "Add Review" on a place details page
2. Fill form and submit

**Expected Results:**

* ✅ Success message: "Review submitted!"
* ✅ Redirect back to place details page
* ✅ Review appears in list

**Screenshot:**
![Add Review](static/images/review.png)

---

## 📊 API Endpoints

| Method | Endpoint              | Description                            |
| ------ | --------------------- | -------------------------------------- |
| POST   | `/api/v1/auth/login`  | Authenticate user and return JWT token |
| GET    | `/api/v1/places/`     | Get list of all places                 |
| GET    | `/api/v1/places/{id}` | Get details of a specific place        |
| POST   | `/api/v1/reviews/`    | Submit a new review                    |

---

## 🎨 Design Features

* Responsive layout
* Clear, simple UI
* Smooth animations for interactions
* Icons for amenities: `icon_bed.png`, `icon_bath.png`, `icon_wifi.png`

---

## 👨‍💻 Author

**Omar Rui**

* GitHub: [@omarrui](https://github.com/omarrui)
* Project: HolbertonSchool HBnB Part 4

---

## 📜 License

This project is part of the **Holberton School curriculum**.

---

## 🙏 Acknowledgments

* Holberton School project guidelines
* Flask and JavaScript documentation
* Inspiration from Airbnb design
