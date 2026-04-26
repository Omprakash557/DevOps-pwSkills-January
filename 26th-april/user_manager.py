"""
User Management System Module

This module provides functionality for managing user accounts including
creation, validation, authentication, and profile management.
"""

import re
from typing import Optional, List, Dict
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class User:
    """
    Represents a user account with profile information and authentication.

    Attributes:
        user_id: Unique identifier for the user
        username: Username for login
        email: User's email address
        password: Hashed password (in real app, should be hashed)
        first_name: User's first name
        last_name: User's last name
        is_active: Whether user account is active
        created_at: Account creation timestamp
        last_login: Last login timestamp
    """

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = ""
    ):
        """
        Initialize a User instance.

        Args:
            user_id: Unique identifier
            username: Username (3-20 chars, alphanumeric + underscore)
            email: Valid email address
            password: Password (min 8 chars, must contain uppercase, lowercase, digit)
            first_name: First name (optional)
            last_name: Last name (optional)

        Raises:
            ValidationError: If any parameter is invalid
        """
        self.user_id = user_id
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.password = self._validate_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = True
        self.created_at = datetime.now()
        self.last_login: Optional[datetime] = None

    @staticmethod
    def _validate_username(username: str) -> str:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            Validated username

        Raises:
            ValidationError: If username is invalid
        """
        if not isinstance(username, str):
            raise ValidationError("Username must be a string")

        if len(username) < 3 or len(username) > 20:
            raise ValidationError("Username must be 3-20 characters")

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise ValidationError(
                "Username can only contain letters, numbers, and underscores"
            )

        return username

    @staticmethod
    def _validate_email(email: str) -> str:
        """
        Validate email format.

        Args:
            email: Email to validate

        Returns:
            Validated email

        Raises:
            ValidationError: If email is invalid
        """
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            raise ValidationError("Invalid email format")

        return email

    @staticmethod
    def _validate_password(password: str) -> str:
        """
        Validate password strength.

        Args:
            password: Password to validate

        Returns:
            Validated password

        Raises:
            ValidationError: If password is weak
        """
        if not isinstance(password, str):
            raise ValidationError("Password must be a string")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one digit")

        return password

    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False

    def activate(self) -> None:
        """Activate user account"""
        self.is_active = True

    def record_login(self) -> None:
        """Record the time of last login"""
        self.last_login = datetime.now()

    def get_full_name(self) -> str:
        """
        Get user's full name.

        Returns:
            Full name or username if name not provided
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username

    def to_dict(self) -> Dict:
        """
        Convert user to dictionary representation.

        Returns:
            Dictionary containing user information
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


class UserManager:
    """
    Manages a collection of users including CRUD operations and searching.

    Attributes:
        users: Dictionary of users keyed by user_id
    """

    def __init__(self):
        """Initialize UserManager with empty user collection"""
        self.users: Dict[int, User] = {}
        self._next_id = 1

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = ""
    ) -> User:
        """
        Create a new user.

        Args:
            username: Username
            email: Email address
            password: Password
            first_name: First name (optional)
            last_name: Last name (optional)

        Returns:
            Created User instance

        Raises:
            ValidationError: If email already exists or validation fails
        """
        if self._email_exists(email):
            raise ValidationError("Email already registered")

        if self._username_exists(username):
            raise ValidationError("Username already taken")

        user = User(
            user_id=self._next_id,
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        self.users[self._next_id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID to retrieve

        Returns:
            User instance or None if not found
        """
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username to search for

        Returns:
            User instance or None if not found
        """
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: Email to search for

        Returns:
            User instance or None if not found
        """
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update user information.

        Args:
            user_id: User ID to update
            **kwargs: Fields to update (first_name, last_name, is_active)

        Returns:
            Updated User instance or None if not found
        """
        user = self.get_user(user_id)
        if not user:
            return None

        if "first_name" in kwargs:
            user.first_name = kwargs["first_name"]
        if "last_name" in kwargs:
            user.last_name = kwargs["last_name"]
        if "is_active" in kwargs:
            user.is_active = kwargs["is_active"]

        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user.

        Args:
            username: Username
            password: Password (should be hashed in production)

        Returns:
            User instance if authentication successful, None otherwise
        """
        user = self.get_user_by_username(username)

        if user and user.is_active and user.password == password:
            user.record_login()
            return user

        return None

    def get_active_users(self) -> List[User]:
        """
        Get all active users.

        Returns:
            List of active User instances
        """
        return [user for user in self.users.values() if user.is_active]

    def get_inactive_users(self) -> List[User]:
        """
        Get all inactive users.

        Returns:
            List of inactive User instances
        """
        return [user for user in self.users.values() if not user.is_active]

    def search_users(self, query: str) -> List[User]:
        """
        Search users by username or email.

        Args:
            query: Search query

        Returns:
            List of matching User instances
        """
        query_lower = query.lower()
        results = []

        for user in self.users.values():
            if (query_lower in user.username.lower() or
                    query_lower in user.email.lower()):
                results.append(user)

        return results

    def get_user_count(self) -> int:
        """
        Get total number of users.

        Returns:
            Total user count
        """
        return len(self.users)

    def get_active_user_count(self) -> int:
        """
        Get count of active users.

        Returns:
            Active user count
        """
        return len(self.get_active_users())

    def reset_all_logins(self) -> int:
        """
        Reset last_login for all users.

        Returns:
            Number of users reset
        """
        count = 0
        for user in self.users.values():
            user.last_login = None
            count += 1
        return count
