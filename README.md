# Personal Budget & Expense Tracker API

A comprehensive Django REST Framework API for tracking personal finances, managing expenses, and setting savings goals.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Transaction Management**: Track income and expenses with categorization
- **Savings Goals**: Create and manage savings goals with progress tracking
- **Monthly Summaries**: Get detailed monthly financial summaries
- **Category Filtering**: Filter transactions by type, category, and date range
- **API Documentation**: Swagger/OpenAPI documentation included

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- JWT Authentication (djangorestframework-simplejwt)
- SQLite Database
- Swagger/OpenAPI Documentation

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd budget-tracker-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - User login
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/profile/` - Get user profile

### Transactions
- `GET /api/transactions/` - List all user transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Get specific transaction
- `PUT /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction
- `GET /api/summary/monthly/` - Get monthly summary
- `GET /api/transactions/stats/` - Get transaction statistics

### Savings Goals
- `GET /api/goals/` - List all savings goals
- `POST /api/goals/` - Create a new savings goal
- `GET /api/goals/{id}/` - Get specific goal
- `PUT /api/goals/{id}/` - Update goal
- `DELETE /api/goals/{id}/` - Delete goal
- `POST /api/goals/{id}/add/` - Add amount to goal
- `GET /api/goals/summary/` - Get goals summary

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123!",
    "password_confirm": "securepassword123!"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123!"
  }'
```

### Create a Transaction
```bash
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "amount": "50.00",
    "type": "expense",
    "category": "food",
    "description": "Lunch at restaurant"
  }'
```

### Create a Savings Goal
```bash
curl -X POST http://localhost:8000/api/goals/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Emergency Fund",
    "target_amount": "5000.00",
    "current_amount": "1000.00",
    "deadline": "2024-12-31"
  }'
```

### Get Monthly Summary
```bash
curl -X GET "http://localhost:8000/api/summary/monthly/?month=12&year=2024" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Models

### Transaction
- `user`: Foreign key to User
- `amount`: Decimal field for transaction amount
- `type`: Choice field ('income' or 'expense')
- `category`: Choice field (Food, Rent, Transport, etc.)
- `description`: Optional text description
- `date`: Date of transaction (auto-set to today)

### SavingsGoal
- `user`: Foreign key to User
- `title`: Goal title
- `target_amount`: Target amount to save
- `current_amount`: Current saved amount
- `deadline`: Optional deadline date
- `is_completed`: Auto-calculated completion status

## Filtering Options

### Transactions
- Filter by type: `?type=income` or `?type=expense`
- Filter by category: `?category=food`
- Filter by date range: `?start_date=2024-01-01&end_date=2024-01-31`

### Goals
- Filter by completion: `?completed=true` or `?completed=false`

## Testing

Run the test suite:
```bash
python manage.py test
```

## Security Features

- JWT-based authentication
- User-specific data access (users can only access their own data)
- Password validation
- CORS configuration for frontend integration

## Development

### Adding New Categories
To add new transaction categories, update the `CATEGORIES` choices in `transactions/models.py`:

```python
CATEGORIES = [
    ('food', 'Food'),
    ('rent', 'Rent'),
    ('transport', 'Transport'),
    ('entertainment', 'Entertainment'),
    ('health', 'Health'),
    ('utilities', 'Utilities'),
    ('shopping', 'Shopping'),  # New category
    ('other', 'Other'),
]
```

### Custom Settings
Create a `.env` file for environment-specific settings:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.
