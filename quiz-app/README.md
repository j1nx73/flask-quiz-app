# Flask Quiz App

A modern, interactive quiz application built with Flask and SQLAlchemy. Features a clean, responsive UI with an admin panel for question management.

## Features

### User Features
- **Interactive Quiz Interface**: Take quizzes with single-choice, multiple-choice, and short-answer questions
- **Progress Tracking**: Visual progress bar showing quiz completion
- **Modern UI**: Clean, responsive design with Bootstrap and FontAwesome icons
- **Results Analysis**: Detailed results with explanations for incorrect answers
- **Category-based Questions**: Questions organized by categories (Math, Science, Geography, etc.)

### Admin Features
- **Secure Admin Panel**: Login-protected admin interface (username: `admin`, password: `admin`)
- **Question Management**: Add new questions with multiple types and categories
- **Category Filtering**: View and filter questions by category
- **Database Management**: Full CRUD operations for quiz content

## Screenshots

### Home Page
- Modern card-based design with gradient background
- Admin login access
- Configurable number of questions

### Question Interface
- Progress bar showing quiz completion
- Interactive option selection with hover effects
- Support for multiple question types

### Results Page
- Visual feedback with icons based on performance
- Detailed explanations for incorrect answers
- Clean, organized layout

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd quiz-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5002`
   - Admin panel: Click "Admin Login" or go to `http://localhost:5002/admin/login`

## Usage

### Taking a Quiz
1. Visit the home page
2. Select the number of questions (1-20)
3. Click "Start Quiz"
4. Answer questions using the interactive interface
5. View your results and review incorrect answers

### Admin Panel
1. Click "Admin Login" on the home page
2. Use credentials: username `admin`, password `admin`
3. View all questions or filter by category
4. Add new questions using the "Add New Question" button

### Adding Questions
1. Log into the admin panel
2. Click "Add New Question"
3. Fill in the question details:
   - **Question Text**: The actual question
   - **Type**: Single choice, multiple choice, or short answer
   - **Difficulty**: Easy, medium, or hard
   - **Category**: Subject category (e.g., Math, Science)
   - **Options**: For choice questions, add 2-4 options with correct/incorrect flags
   - **Correct Answer**: For short answer questions
   - **Explanation**: Optional explanation for the answer

## Project Structure

```
quiz-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── home.html         # Home page
│   ├── question.html     # Question interface
│   ├── results.html      # Results page
│   ├── admin_login.html  # Admin login
│   ├── admin_dashboard.html  # Admin dashboard
│   └── admin_add_question.html  # Add question form
└── quiz.db              # SQLite database (created automatically)
```

## Database Schema

### Question Model
- `id`: Primary key
- `text`: Question text
- `type`: Question type (single_choice, multiple_choice, short_answer)
- `difficulty`: Difficulty level (easy, medium, hard)
- `category`: Question category
- `correct_answer`: Correct answer for short_answer questions
- `explanation`: Explanation for the answer

### Option Model
- `id`: Primary key
- `question_id`: Foreign key to Question
- `text`: Option text
- `is_correct`: Boolean flag for correct options

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Using Gunicorn (Recommended)
1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

#### Option 2: Using Docker
1. Create a Dockerfile:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. Build and run:
   ```bash
   docker build -t quiz-app .
   docker run -p 5000:5000 quiz-app
   ```

#### Option 3: Heroku Deployment
1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy to Heroku:
   ```bash
   heroku create your-quiz-app
   git push heroku main
   ```

### Environment Variables
For production, set these environment variables:
- `SECRET_KEY`: A secure secret key for Flask sessions
- `DATABASE_URL`: Database connection string (if using external database)

## Configuration

### Changing Admin Credentials
Edit the constants in `app.py`:
```python
ADMIN_USERNAME = 'your_username'
ADMIN_PASSWORD = 'your_secure_password'
```

### Database Configuration
The app uses SQLite by default. To use PostgreSQL or MySQL:
1. Update `SQLALCHEMY_DATABASE_URI` in `app.py`
2. Install the appropriate database driver
3. Update `requirements.txt`

## Security Considerations

- Change default admin credentials in production
- Use environment variables for sensitive data
- Implement proper session management
- Consider rate limiting for admin login
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Changelog

### Version 1.0.0
- Initial release
- Basic quiz functionality
- Admin panel
- Modern UI design
- Category-based questions 