# 📚 Library Service

**Library Service** is a backend system built with Django and Django REST Framework that allows users to borrow books, return them, and handle payments through Stripe. The system also supports automatic notifications via Telegram.

## ⚙️ Technologies

- Python 3.11
- Django & DRF
- PostgreSQL
- Stripe API
- Telegram Bot API
- Docker / Docker Compose
- drf-spectacular (OpenAPI schema)
- JWT Authentication

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/library-service.git
cd library-service
```
### 2. Run with Docker
```bash
    docker-compose up --build
```
### 3. Apply migrations and create a superuser
```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
```
### 4. Access
- API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- Swagger Documentation: http://localhost:8000/api/schema/swagger-ui/

## 📦 Features

### 📘 Books
- CRUD for books (available only to staff)
- Fields: title, author, cover, inventory, daily_fee

### 🔄 Borrowings
- Users can borrow available books
- Inventory is automatically decreased when borrowed
- Books can be returned with validation to avoid double returns
- Telegram notifications for new borrowings and returns

### 💳 Payments
- Integrated with Stripe
- Payment sessions created for each borrowing
- Webhook support to update payment status
- Types: PAYMENT, FINE; Statuses: PENDING, PAID

### 🔐 Authentication
- JWT-based authentication. Users must include their token in the Authorization header for all protected endpoints.

### 📬 Integrations
- Stripe API — for payment sessions and webhooks
- Telegram Bot API — to send notifications about new borrowings or returns

### 📁 Project Structure
- book/ — book models, serializers, views
- borrowing/ — borrowings logic and views
- payment/ — Stripe integration
- library_service/ — core Django config
- telegram_helper.py — helper for Telegram notifications


## 🧑‍💻 Author
### Name: Nazarii Khalimonov
### GitHub: https://github.com/Carn1vor3
### Telegram: @Carn1vor3