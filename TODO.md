# Expense Splitter - CS50 Final Project

## TODO List

### Day 1: Foundation & Core Logic
- [X] Set up Flask app structure
- [ ] Create database schema (users, groups, expenses, debts, payments)
- [X] Implement user registration/login
- [ ] Build expense splitting logic (equal split)
- [ ] Calculate who owes whom (minimize transactions algorithm)
- [ ] Basic routes: create group, add expense, view debts
- [ ] Test calculations with dummy data

### Day 2: UI/UX & Making It Pretty
- [ ] Set up Bootstrap/Tailwind CSS
- [ ] Design group dashboard page
- [ ] Create expense list with emoji categories
- [ ] Build add expense form with emoji selector
- [ ] Group creation page with themes
- [ ] Add "mark as paid" button
- [ ] Implement confetti animation on payment
- [ ] Color coding for debts (green = owed to you, red = you owe)
- [ ] Hover effects and transitions

### Day 3: Fun Features & Reminders
- [ ] Add timestamp tracking to debts
- [ ] Build reminder check system (3 days, 7 days)
- [ ] Integrate memegen.link API for friendly memes
- [ ] Personal dashboard with reminder memes
- [ ] Group feed pending payment notifications
- [ ] Payment streak/badge system
- [ ] Trip stats recap page
- [ ] Optional: leaderboard (fastest payer, etc.)
- [ ] Bug fixes and edge cases

### Day 4: Polish, Testing & README
- [ ] Test all user flows
- [ ] Fix bugs (negative amounts, duplicate payments, etc.)
- [ ] Mobile responsiveness
- [ ] Loading states and error messages
- [ ] Final UI polish
- [ ] Write full README.md (750+ words)
  - [ ] Project description
  - [ ] File structure explanation
  - [ ] Design choices
  - [ ] How to run locally
  - [ ] Technologies used

### Day 5: Video Production
- [ ] Script preparation
- [ ] Film demo (2 hours)
  - [ ] Opening with title card
  - [ ] Demo scenario walkthrough
  - [ ] Show reminder system
  - [ ] Code tour
- [ ] Edit video (1-1.5 hours)
- [ ] Upload to YouTube (unlisted)
- [ ] Update README with video URL
- [ ] Submit with submit50

---

## Dependencies to Install

### Python Packages
```bash
pip install flask
pip install flask-session
pip install cs50  # for SQL convenience (optional)
# OR
pip install flask-sqlalchemy  # if using SQLAlchemy instead
```

### Frontend (CDN - no install needed, just link in HTML)
- Bootstrap CSS: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css`
- Confetti.js: `https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js`
- Font Awesome (for icons): `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`

### Optional
```bash
pip install requests  # if making API calls to memegen.link server-side
pip install python-dotenv  # for environment variables
pip install werkzeug  # for password hashing (usually comes with Flask)
```

### Requirements.txt
Create this file for easy installation:
```
Flask==3.0.0
Flask-Session==0.5.0
cs50==9.2.0
requests==2.31.0
python-dotenv==1.0.0
```

Then install all at once:
```bash
pip install -r requirements.txt
```

---

## Quick Setup Commands
```bash
# Create project directory
mkdir expense-splitter
cd expense-splitter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create basic structure
mkdir templates static
touch app.py schema.sql README.md

# Initialize database
python
>>> from app import init_db
>>> init_db()
>>> exit()

# Run app
flask run
```

---

## File Structure (Plan)
```
expense-splitter/
├── app.py              # Main Flask application
├── schema.sql          # Database schema
├── expenses.db         # SQLite database (created on first run)
├── requirements.txt    # Python dependencies
├── README.md          # Final project documentation
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── group.html
│   ├── add_expense.html
│   └── dashboard.html
└── static/
    ├── styles.css
    └── script.js
```

---

## Notes & Ideas
- memegen.link API format: `https://api.memegen.link/images/custom/{top_text}/{bottom_text}.jpg?background={image_url}`
- Splitting algorithm: use greedy approach to minimize transactions
- Reminder logic: check `datetime.now() - debt.created_at` for days
- Emoji categories: 🍔 Food, 🚕 Transport, 🎉 Fun, 🏨 Lodging, 🛒 Shopping, 💊 Health

---

## Design Decisions to Document Later
- Why Flask over Django? (simpler, faster for small projects)
- Why SQLite? (easy setup, no server needed)
- Splitting algorithm choice
- Reminder timing (3 days, 7 days)
- Meme integration approach

---

## Video Script Outline
1. Intro card (name, project, date)
2. Problem statement (splitting bills is annoying)
3. Demo: create group
4. Demo: add expenses
5. Demo: view debts & visualization
6. Demo: reminder system (time-lapse)
7. Demo: settle payment with confetti
8. Code walkthrough (brief)
9. Conclusion

---

## Submission Checklist
- [ ] All code files in `project/` directory
- [ ] README.md with video URL
- [ ] Video uploaded to YouTube (unlisted)
- [ ] Video under 3 minutes
- [ ] Run `submit50 cs50/problems/2025/x/project`
- [ ] Check gradebook at cs50.me/cs50x
- [ ] Claim certificate before Jan 1, 2026



## What you should submit to CS50:

Based on your current structure, you need:

**Keep these:**
- ✅ `app.py` - Your main Flask app
- ✅ `README.md` - Your final documentation (not TODO.md)
- ✅ `templates/` folder (you'll create this)
- ✅ `static/` folder (you'll create this)
- ✅ Any `.db` or `schema.sql` files you create

**DON'T submit these:**
- ❌ `venv/` - Virtual environment (too large, unnecessary)
- ❌ `__pycache__/` - Python cache files
- ❌ `.gitignore` - Not required for CS50
- ❌ `TODO.md` - Your working notes (keep separate)

## For CS50 submission:

When you're ready to submit to CS50, your folder should look like:
```
project/
├── app.py
├── schema.sql
├── expenses.db
├── README.md
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── group.html
│   ├── add_expense.html
│   └── dashboard.html
└── static/
    ├── styles.css
    └── script.js