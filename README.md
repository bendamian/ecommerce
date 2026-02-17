🛒 Django E-Commerce (PayPal Integrated)

A Production-Ready Commerce Engine built with Django 5

This project demonstrates a robust, real-world commerce architecture focusing on data integrity and secure payment processing. By leveraging atomic transactions, the system ensures that orders are only finalized when payment is verified, preventing "ghost orders" or data inconsistencies.
🌟 Key Highlights

    Secure Payment-First Architecture: Orders are strictly generated after PayPal confirmation.

    Transaction-Safe: Database operations use atomic blocks to ensure data consistency.

    Flexible Checkout: Supports both guest users and authenticated members.

    Order Lifecycle: Built-in workflow management from Created to Delivered.

🛠️ Tech Stack
Component	Technology
Backend	Django 5.x (Python)
Frontend	Bootstrap 5, jQuery
Payments	PayPal JavaScript SDK
Database	SQLite (Dev) / PostgreSQL (Recommended for Prod)
💳 Payment & Order Logic

The application follows a rigorous sequence to protect the integrity of your sales data:

    Session Cart: Users manage items in a session-based cart.

    SDK Authorization: The PayPal JS SDK handles the UI and initial payment capture.

    Backend Verification: An AJAX request sends the capture data to Django.

    Atomic Creation:

        The backend validates the payment.

        Order and OrderItems are created within a database transaction.

        If any step fails, the transaction rolls back.

    Cleanup: The session cart is cleared only after successful DB persistence.

📊 Data Schema

The core logic relies on two primary models:

    Order: Stores customer details, shipping address, total amount paid, and the current lifecycle status.

    OrderItem: A many-to-one relationship capturing the specific price and quantity of products at the exact moment of purchase.

🚀 Getting Started

1. Clone & Environment
Bash

git clone https://github.com/yourusername/your-repo.git
cd your-repo
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install django requests

2. Configuration
Update your settings.py with your PayPal Client ID and Secret:
Python

PAYPAL_CLIENT_ID = 'your_id_here'
PAYPAL_SECRET = 'your_secret_here'

3. Database & Launch
Bash

python manage.py migrate
python manage.py runserver
