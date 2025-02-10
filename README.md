# Library Book Borrowing Management System
## Project Description
This project aims to develop an online management system for a library's book borrowing process. The current manual system is outdated and inefficient, relying on paper records for tracking books, borrowings, users, and payments. Our goal is to create a fully functional API that will streamline the library's operations, enhance user experience, and provide real-time inventory management.

## Key Features
- User Management: Allow users to register, log in, and manage their profiles.
- Book Inventory Management: Enable administrators to add, update, and remove books from the library's inventory.
- Borrowing System: Implement a system for users to borrow books, specifying the duration of the borrowing period.
- Return Tracking: Automatically track the return status of borrowed books, notifying users of due dates and overdue items.
- Search Functionality: Allow users to search for books by title, author, genre, or availability status.
- Admin Dashboard: Provide administrators with an interface to view borrowing statistics, overdue books, and user activity.

## Technologies Used
- Backend Framework: Django
- Database: PostgreSQL
- API Documentation: Swagger
- Authentication: JWT

## Installation
- Clone the repository:
    - git clone https://github.com/Serhii-Chubur/drf-library-practice
    - cd library-management-system
- Install dependencies:
    - pip install -r requirements.txt
- Set up the database:
    - [Insert database setup instructions]
- Run the application:
    - [Insert command to run the application]

## API Endpoints
### Books Service:
- POST:        books/           - add new 
- GET:         books/           - get a list of books
- GET:         books/\<id\>/      - get book detail info 
- PUT/PATCH:   books/\<id\>/      - update book
- DELETE:      books/\<id\>/      - delete book
### Users Service:
- POST:        users/                  - register a new user 
- POST:        users/token/            - get JWT tokens 
- POST:        users/token/refresh/    - refresh JWT token 
- GET:         users/me/               - get my profile info 
- PUT/PATCH:   users/me/               - update profile info 
### Borrowings Service:
- POST:        borrowings/   		                  - add new borrowing
- GET:         borrowings/?user_id=...&is_active=...  - get borrowings by user id and whether is borrowing still active or not.
- GET:         borrowings/\<id\>/  		  - get specific borrowing 
- POST: 	   borrowings/\<id\>/return/  - set actual return date

## Library Notifications System
The Notifications System is an integral part of the Library Book Borrowing Management System. This service is designed to send real-time notifications via Telegram. It will notify you about new borrowings and overdue borrowings. The service utilize Django Celery for handling background tasks in a parallel process.

## Contributing
Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature/YourFeature).
- Make your changes and commit them (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/YourFeature).
- Open a pull request.

By implementing this Library Book Borrowing Management System, we aim to modernize the library's operations, making it easier for both users and administrators to manage book borrowings efficiently.