# Expense Splitter

#### Video Demo: <URL HERE>

#### Description:

TODO

This project is a web-based expense splitting application built with Flask that helps groups of friends manage shared expenses and settle debts in a fun and engaging way. Unlike traditional expense trackers that can feel tedious and guilt-inducing, this application gamifies the experience with friendly reminders, celebratory animations, and entertaining visualizations.

**What the project does:**

The Expense Splitter allows users to create groups for trips, dinners, or any shared expense scenario. Users can add expenses with customizable splits (equal or custom amounts), and the application automatically calculates who owes whom while minimizing the number of transactions needed. The app features a friendly reminder system that gently nudges users who haven't settled their debts after 3 days with lighthearted memes, and provides group notifications after 7 days. When debts are paid, users are rewarded with confetti animations and positive reinforcement.

**Files in the project:**

- `app.py` - The main Flask application containing all routes, logic for expense splitting, debt calculation algorithms, reminder system checks, and database interactions. This is the heart of the application where all business logic resides.

- `schema.sql` - Defines the database structure with tables for users, groups, expenses, debts, and payments. Includes timestamp fields for tracking when debts were created to power the reminder system.

- `expenses.db` - SQLite database file that stores all application data (auto-generated on first run).

- `templates/layout.html` - Base template with navigation, Bootstrap integration, and the overall page structure that other templates extend.

- `templates/index.html` - Landing page explaining the app and encouraging users to sign up or log in.

- `templates/login.html` - User authentication page.

- `templates/register.html` - New user registration form.

- `templates/group.html` - Main group dashboard showing all expenses, current debts, and settlement status with color-coded debt cards.

- `templates/add_expense.html` - Form for adding new expenses with emoji category selection and custom split options.

- `templates/dashboard.html` - Personal user dashboard that displays all groups, outstanding debts, and shows friendly reminder memes when payments are overdue.

- `static/styles.css` - Custom CSS for styling, animations, color schemes for debt visualization (green for money owed to you, red for money you owe), and responsive design.

- `static/script.js` - JavaScript for interactive features including confetti animations using canvas-confetti library, emoji selection interface, and smooth UI transitions.

- `requirements.txt` - List of Python dependencies needed to run the application.

**Design choices:**

One of the biggest design decisions was choosing the debt minimization algorithm. Initially, I considered calculating direct debts between every pair of users, but this would result in too many transactions (if 5 people split expenses, that's potentially 10+ separate payments). Instead, I implemented a greedy algorithm that calculates net balances for each person and then matches creditors with debtors to minimize the total number of transactions needed. This makes settling up much simpler for users.

For the reminder system, I debated between email notifications versus in-app memes. I chose the meme approach because it's more engaging, keeps users returning to the app, and maintains the lighthearted tone. The timing (3 days for personal reminders, 7 days for group notifications) was chosen to be gentle enough that people don't feel harassed, but frequent enough to actually be effective.

I chose Flask over Django because the project scope didn't require Django's complexity, and Flask's lightweight nature allowed for faster development within the 3-day timeframe. SQLite was chosen over PostgreSQL for simplicity and portability - the database file can travel with the code, making setup and submission easier.

The emoji categorization system was added to make expense logging more fun and visual. Instead of dropdown menus with boring text categories, users can quickly tap 🍔 for food or 🚕 for transport, making the interface more intuitive and enjoyable.

For the debt visualization, I initially considered complex network graphs using D3.js, but opted for simpler color-coded cards to keep the scope manageable and ensure the interface remains fast and responsive. The confetti animation upon payment settlement was a must-have feature because it provides immediate positive feedback and makes the act of settling debts feel rewarding rather than obligatory.

The application uses Flask-Session for user authentication, ensuring that each user only sees their own groups and debts. Password hashing with Werkzeug provides basic security for user credentials.

**Future enhancements I considered but descoped:**

- Receipt photo uploads (would require cloud storage setup)
- Mobile app version (out of scope for this project)
- Integration with payment apps like Venmo/PayPal (API complexity)
- Multi-currency support (added complexity in calculations)
- Recurring expense tracking (nice-to-have but not essential)

This project taught me the importance of scope management - I had many ambitious ideas but learned to focus on core features that could be completed within the deadline while still delivering a polished, functional, and genuinely useful application.