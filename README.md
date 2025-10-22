# 🧠 Backend Wizards – Stage 1 Task: String Analyzer API

*A RESTful API that analyzes strings, computes their properties, and supports advanced filtering.*

---

## 🚀 Overview

This project is part of the **Backend Wizards Program (Stage 1)**.
It’s a **Python/Django REST Framework API** that analyzes strings, stores their computed properties, and provides endpoints to retrieve, filter, and delete them.

Each analyzed string is uniquely identified by its **SHA-256 hash** and includes various computed attributes like palindrome check, character frequency, and word count.

---

## 🎯 Core Features

✅ Analyze strings and compute detailed properties
✅ Automatically detect **palindromes** (case-insensitive)
✅ Store and retrieve analyzed strings from the database
✅ Filter results with query parameters and natural language
✅ Delete specific strings
✅ Fully REST-compliant API with proper HTTP status codes

---

## 🧩 API Endpoints

### 1️⃣ **Analyze / Create a String**

**POST** `/strings`

**Request Body:**

```json
{
  "value": "racecar"
}
```

**Success Response (201 Created):**

```json
{
  "id": "af5b1a...sha256...",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "af5b1a...",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-22T20:30:00Z"
}
```

**Error Responses:**

* `409 Conflict` – String already exists
* `400 Bad Request` – Missing or invalid `"value"` field
* `422 Unprocessable Entity` – `"value"` is not a string

---

### 2️⃣ **Get a Specific String**

**GET** `/strings/{string_value}`

**Success Response (200 OK):**

```json
{
  "id": "sha256_hash",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "abc123...",
    "character_frequency_map": { ... }
  },
  "created_at": "2025-10-22T20:00:00Z"
}
```

**Error Response:**
`404 Not Found` – String does not exist

---

### 3️⃣ **Get All Strings with Filters**

**GET** `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a`

**Success Response (200 OK):**

```json
{
  "data": [ /* matching strings */ ],
  "count": 3,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "max_length": 20,
    "word_count": 2,
    "contains_character": "a"
  }
}
```

**Error Response:**
`400 Bad Request` – Invalid or conflicting filter parameters

---

### 4️⃣ **Natural Language Filtering**

**GET** `/strings/filter-by-natural-language?query=all single word palindromic strings`

**Success Response (200 OK):**

```json
{
  "data": [ /* matching strings */ ],
  "count": 2,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

**Error Response:**
`400 Bad Request` – Unrecognized natural language query

---

### 5️⃣ **Delete a String**

**DELETE** `/strings/{string_value}`

**Success Response:**
`204 No Content` – String successfully deleted

**Error Response:**
`404 Not Found` – String not found in the system

---

## 🧮 String Properties Computed

| Property                  | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| `length`                  | Total number of characters                                     |
| `is_palindrome`           | True if the string reads the same backwards (case-insensitive) |
| `unique_characters`       | Number of distinct characters                                  |
| `word_count`              | Number of words (split by whitespace)                          |
| `sha256_hash`             | SHA-256 hash used as a unique ID                               |
| `character_frequency_map` | Object mapping each character to its frequency                 |

---

## ⚙️ Tech Stack

* **Language:** Python 🐍
* **Framework:** Django + Django REST Framework
* **Database:** SQLite (Development) / PostgreSQL (Production)
* **Deployment:** Koyeb ☁️
* **Hashing:** Python’s `hashlib`
* **Timestamps:** UTC in ISO 8601 format

---

## 🧰 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<yourusername>/string-analyzer-api.git
cd string-analyzer-api
```

### 2️⃣ Create a virtual environment

```bash
python -m venv env
source env/bin/activate   # (On Windows: env\Scripts\activate)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py migrate
```

### 5️⃣ Run the server

```bash
python manage.py runserver
```

### 6️⃣ Access locally

Go to → [http://127.0.0.1:8000/strings](http://127.0.0.1:8000/strings)

---

## ☁️ Deployment on Koyeb (Step-by-Step Guide)

### 🪄 1. Prepare your repository

Make sure your project has the following files:

```
Procfile
requirements.txt
runtime.txt
manage.py
```

**Procfile**

```
web: gunicorn string_analyzer.wsgi
```

**runtime.txt**

```
python-3.12.2
```

---

### 🧱 2. Push your project to GitHub

```bash
git add .
git commit -m "Initial commit for Koyeb deployment"
git push origin main
```

---

### ⚙️ 3. Create a Koyeb account

* Visit [https://www.koyeb.com](https://www.koyeb.com)
* Log in with GitHub
* Click **"Create App"**

---

### 🚀 4. Connect your GitHub repo

* Choose your **GitHub repository**
* Select **main** branch
* Koyeb will detect it’s a **Python app**
* Add your build command:

  ```
  pip install -r requirements.txt
  python manage.py migrate
  ```

---

### 🔐 5. Add environment variables

| Variable        | Example                                   | Description                        |
| --------------- | ----------------------------------------- | ---------------------------------- |
| `SECRET_KEY`    | `django-insecure-xyz123...`               | Django secret key                  |
| `DEBUG`         | `False`                                   | Disable debug in production        |
| `ALLOWED_HOSTS` | `.koyeb.app`                              | Allow Koyeb domain                 |
| `DATABASE_URL`  | `postgresql://user:pass@host:port/dbname` | Database URL (if using PostgreSQL) |

---

### 🌍 6. Deploy!

Click **Deploy**.
Koyeb will:

* Install your dependencies
* Run your migrations
* Start your app with `gunicorn`
* Give you a public URL like:
  👉 `https://string-analyzer.koyeb.app/`

---

## 🧪 Testing

Use **Postman** or **curl** to test the endpoints.

Example:

```bash
curl -X POST https://string-analyzer.koyeb.app/strings \
     -H "Content-Type: application/json" \
     -d '{"value": "racecar"}'
```

---

## 📚 What I Learned

💡 How to design and structure RESTful APIs in Django
💡 The importance of data validation and HTTP status codes
💡 Integrating hashing and string analysis logic
💡 Handling errors and writing clean, reusable utility functions
💡 Using query parameters and natural language parsing for smart filtering
💡 Hosting and deploying production-ready Django APIs

---

## 🧩 Challenges Faced

🚧 Handling malformed JSON inputs gracefully
🚧 Designing efficient filtering logic for multiple parameters
🚧 Configuring production deployment (Koyeb and static files)
🚧 Making sure status codes match the spec (201, 400, 404, 409, etc.)

---

## 🙌 Author

**👨‍💻 Name:** Okonkwo Emmanuel
**📧 Email:** [okonkwoemmanuel348@gmail.com](mailto:okonkwoemmanuel348@gmail.com)
**💼 Stack:** Python / Django / REST APIs
**🌐 GitHub:** [github.com/okonkwo348](https://github.com/okonkwo348)
**🔗 LinkedIn:** [linkedin.com/in/okonkwoemmanuel348](#)

---

## 🏁 Acknowledgements

Special thanks to the **Backend Wizards** program for creating this exciting challenge that helped me sharpen my backend skills and deepen my understanding of API architecture.

>>>>>>> 95fd2ce (Prepare project for Koyeb deployment)
