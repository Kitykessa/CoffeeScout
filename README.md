# CoffeeScout

#### Video Demo:  <URL HERE>

#### Description:
**CoffeeScout** is a web application created as the final project for the **CS50 course**.
Its goal is to help coffee lovers discover great coffee beans available in local stores, explore detailed information about each coffee, and share their own tasting experiences.

---

## Project Idea

While living in Ireland, I visited several local coffee shops and collected information about interesting coffee bean varieties available in stores.
Each coffee was carefully added to a database with details such as:

- origin
- roast level
- bean type
- description
- stores where it can be purchased

CoffeeScout allows users not only to browse this data, but also to **rate coffees, leave reviews, and build a personal coffee profile**.

---

## Features

- Browse and filter coffee beans by name, roast, origin, beans, and store
- View detailed coffee pages with images and descriptions
- Leave ratings, comments, tasting notes, and flavor profiles
- See average ratings and flavor statistics based on user reviews
- User authentication (register, login, change password)
- Responsive, coffee-themed design

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML, CSS
- JavaScript
- Jinja2

---

## How to Run

### 1. Clone or download the project

If the project is on GitHub:
```bash
git clone https://github.com/Kitykessa/CoffeeScout.git
cd coffeescout
```
Or download the project files and unzip them.

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare the database

The coffee data is stored in an Excel file (coffee.xlsx).

> 1. Convert Excel data to JSON:
>```bash
>python convert.py
>```
> 2. Initialize the SQLite database:
>```bash
>python init_db.py
>```
This will create coffee.db and populate it with coffee data and sample users.

### 5. Run the application
```bash
flask run
```
