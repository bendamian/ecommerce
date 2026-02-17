# Django 5 E-Commerce (PayPal)

A production-oriented e-commerce application built with **Django 5**, featuring a secure PayPal integration and transaction-safe order management.

## 🚀 Key Features
* **Secure Payment Flow:** PayPal JS SDK integration; orders are created only after successful payment capture.
* **Data Integrity:** Uses Django's `transaction.atomic` to ensure no partial or unpaid orders are saved.
* **Session Cart:** Full shopping cart functionality for both guest and logged-in users.
* **Order Management:** Automated status workflow (Created → Paid → Dispatched → Delivered).

## 🛠️ Tech Stack
* **Backend:** Django 5.x
* **Frontend:** Bootstrap, jQuery
* **Payments:** PayPal JavaScript SDK
* **Database:** SQLite (Development)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone[git@github.com:bendamian/ecommerce.git]
   cd your-repo

