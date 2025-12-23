# CoffeeScout

#### Video Demo:  https://youtu.be/jFi8fiiFmEA

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

### 1. Get the project files

If the project is on GitHub:
```bash
git clone https://github.com/Kitykessa/CoffeeScout.git
cd coffeescout
```
Or download the project as a ZIP archive and extract it.

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

The initial coffee data is stored in an Excel file (coffee.xlsx).

> 1. Convert Excel data to JSON:
>```bash
>python convert.py
>```
> 2. Initialize the SQLite database:
>```bash
>python init_db.py
>```
This will create the coffee.db file and populate it with the initial coffee data.
This step only needs to be done once.

### 5. Run the application
```bash
flask run
```

### 6. Open in browser:
```bash
http://127.0.0.1:5000/
```

---

## Sample Users

The database is initialized with sample users for testing purposes:

- **Username:** admin  
  **Password:** adminpass  

- **Username:** user1  
  **Password:** coffee123  

These users can be used to explore reviews, ratings, and profile functionality.

---

## Future Improvements

- Add pagination for large coffee lists
- Allow users to upload their own coffee photos
- Add favorite coffees feature
- Improve review analytics and visual charts
- Expand the database with more local stores and coffee brands
