# Social Media API

This project implements a user authentication system using Django Rest Framework (DRF). It provides functionality for user registration, login, and token-based authentication. The custom user model includes additional fields for bio, profile picture, and follower relationships.

---

## **Features**
- **User Registration:** Create a new user account.
- **User Login:** Authenticate users and provide access tokens.
- **Token Authentication:** Secure endpoints using DRF tokens.
- **Custom User Model:** Extends Django's `AbstractUser` to include:
  - Bio
  - Profile Picture
  - Followers (Many-to-Many relationship)

---

## **Setup Process**

### **1. Clone the Repository**
```bash
$ git clone <repository_url>
$ cd <repository_name>
```

### **2. Create and Activate a Virtual Environment**
 ensure you have poetry installed in your pc

### **3. Install Dependencies**
```bash
$ poetry install
```

### **4. Apply Migrations**
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### **5. Create a Superuser**
```bash
$ python manage.py createsuperuser
```

### **6. Run the Development Server**
```bash
$ python manage.py runserver
```

---

## **API Endpoints**

### **1. Register**
- **URL:** `POST /accounts/register/`
- **Request Body (JSON):**
  ```json
  {
      "username": "testuser",
      "password": "password123",
      "email": "test@example.com"
  }
  ```
- **Response:**
  ```json
  {
      "token": "generated_token_here"
  }
  ```

### **2. Login**
- **URL:** `POST /accounts/login/`
- **Request Body (JSON):**
  ```json
  {
      "username": "testuser",
      "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
      "token": "generated_token_here"
  }
  ```


## **Testing the API**

### **Using Django Rest Framework Interface:**
1. Start the server with `python manage.py runserver`.
2. Access the API endpoints using the browser or tools like Postman.

### **Using Postman:**
1. Register a user by sending a POST request to `/accounts/register/`.
2. Log in with the registered user credentials at `/accounts/login/`.
3. Use the token for authenticated requests like following/unfollowing users.

---

## **Contributing**
Feel free to fork this repository and submit pull requests for improvements or bug fixes.

---

## **License**
This project is licensed under the MIT License.

