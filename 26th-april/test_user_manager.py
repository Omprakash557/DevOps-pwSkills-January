"""
Test suite for User Management System

Tests cover:
- User creation and validation
- UserManager operations
- Error handling
- Edge cases
- Integration scenarios
"""

import pytest
from datetime import datetime
from user_manager import User, UserManager, ValidationError


# ============================================================================
# USER CLASS TESTS
# ============================================================================

class TestUserCreation:
    """Test User creation and initialization"""

    def test_user_creation_success(self):
        """Test creating a valid user"""
        user = User(
            user_id=1,
            username="john_doe",
            email="john@example.com",
            password="SecurePass123"
        )

        assert user.user_id == 1
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.password == "SecurePass123"
        assert user.is_active is True
        assert user.last_login is None

    def test_user_creation_with_full_name(self):
        """Test creating user with first and last name"""
        user = User(
            user_id=1,
            username="jane_doe",
            email="jane@example.com",
            password="SecurePass123",
            first_name="Jane",
            last_name="Doe"
        )

        assert user.first_name == "Jane"
        assert user.last_name == "Doe"
        assert user.get_full_name() == "Jane Doe"

    def test_user_creation_timestamp(self):
        """Test that user creation sets timestamp"""
        before = datetime.now()
        user = User(
            user_id=1,
            username="test_user",
            email="test@example.com",
            password="SecurePass123"
        )
        after = datetime.now()

        assert before <= user.created_at <= after


class TestUsernameValidation:
    """Test username validation"""

    @pytest.mark.parametrize("username", [
        "valid_user",
        "user123",
        "John_Doe",
        "a_b",
        "test",
    ])
    def test_valid_usernames(self, username):
        """Test valid username formats"""
        user = User(
            user_id=1,
            username=username,
            email="test@example.com",
            password="SecurePass123"
        )
        assert user.username == username

    @pytest.mark.parametrize("username", [
        "ab",              # Too short
        "a" * 21,          # Too long
        "user@name",       # Invalid character
        "user-name",       # Invalid character
        "user name",       # Space not allowed
                           # Empty string
        "123!@#",          # Special characters
    ])
    def test_invalid_usernames(self, username):
        """Test invalid username formats"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username=username,
                email="test@example.com",
                password="SecurePass123"
            )

    def test_username_not_string(self):
        """Test username must be string"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username=123,
                email="test@example.com",
                password="SecurePass123"
            )


class TestEmailValidation:
    """Test email validation"""

    @pytest.mark.parametrize("email", [
        "user@example.com",
        "test.user@example.co.uk",
        "john+filter@domain.com",
        "a@b.co",
        "name123@test-domain.com",
    ])
    def test_valid_emails(self, email):
        """Test valid email formats"""
        user = User(
            user_id=1,
            username="testuser",
            email=email,
            password="SecurePass123"
        )
        assert user.email == email

    @pytest.mark.parametrize("email", [
        "invalid",                      # No @
        "user@",                        # No domain
        "@example.com",                 # No user
        "user@.com",                    # No domain name
        "user@example",                 # No TLD
        "user @example.com",            # Space
        "user@exam ple.com",            # Space in domain
    ])
    def test_invalid_emails(self, email):
        """Test invalid email formats"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username="testuser",
                email=email,
                password="SecurePass123"
            )

    def test_email_not_string(self):
        """Test email must be string"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username="testuser",
                email=123,
                password="SecurePass123"
            )


class TestPasswordValidation:
    """Test password validation"""

    @pytest.mark.parametrize("password", [
        "SecurePass123",
        "MyPassword456",
        "Test1234",
        "VerySecure999",
    ])
    def test_valid_passwords(self, password):
        """Test valid password formats"""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password=password
        )
        assert user.password == password

    @pytest.mark.parametrize("password", [
        "short1A",              # Too short (but has requirements)
        "nouppercase123",       # No uppercase
        "NOLOWERCASE123",       # No lowercase
        "NoDigits",             # No digit
        "Pass",                 # Too short
    ])
    def test_invalid_passwords(self, password):
        """Test invalid password formats"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username="testuser",
                email="test@example.com",
                password=password
            )

    def test_password_not_string(self):
        """Test password must be string"""
        with pytest.raises(ValidationError):
            User(
                user_id=1,
                username="testuser",
                email="test@example.com",
                password=123
            )


class TestUserMethods:
    """Test User instance methods"""

    @pytest.fixture
    def user(self):
        """Provide a user instance"""
        return User(
            user_id=1,
            username="test_user",
            email="test@example.com",
            password="SecurePass123",
            first_name="Test",
            last_name="User"
        )

    def test_deactivate_user(self, user):
        """Test deactivating a user"""
        assert user.is_active is True
        user.deactivate()
        assert user.is_active is False

    def test_activate_user(self, user):
        """Test activating a user"""
        user.deactivate()
        assert user.is_active is False
        user.activate()
        assert user.is_active is True

    def test_record_login(self, user):
        """Test recording user login"""
        assert user.last_login is None

        before = datetime.now()
        user.record_login()
        after = datetime.now()

        assert user.last_login is not None
        assert before <= user.last_login <= after

    def test_get_full_name_with_name(self, user):
        """Test getting full name when name is provided"""
        assert user.get_full_name() == "Test User"

    def test_get_full_name_without_name(self):
        """Test getting full name when name is not provided"""
        user = User(
            user_id=1,
            username="john_doe",
            email="john@example.com",
            password="SecurePass123"
        )
        assert user.get_full_name() == "john_doe"

    def test_to_dict(self, user):
        """Test converting user to dictionary"""
        user_dict = user.to_dict()

        assert user_dict["user_id"] == 1
        assert user_dict["username"] == "test_user"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["first_name"] == "Test"
        assert user_dict["last_name"] == "User"
        assert user_dict["full_name"] == "Test User"
        assert user_dict["is_active"] is True
        assert user_dict["last_login"] is None


# ============================================================================
# USER MANAGER TESTS
# ============================================================================

class TestUserManagerCreation:
    """Test UserManager creation and user operations"""

    @pytest.fixture
    def manager(self):
        """Provide a UserManager instance"""
        return UserManager()

    def test_manager_initialization(self, manager):
        """Test UserManager initializes correctly"""
        assert manager.get_user_count() == 0

    def test_create_user_success(self, manager):
        """Test creating a user successfully"""
        user = manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123",
            first_name="Alice",
            last_name="Smith"
        )

        assert user.user_id == 1
        assert user.username == "alice"
        assert manager.get_user_count() == 1

    def test_create_multiple_users(self, manager):
        """Test creating multiple users"""
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        manager.create_user(
            username="bob",
            email="bob@example.com",
            password="SecurePass123"
        )

        assert manager.get_user_count() == 2

    def test_create_duplicate_email(self, manager):
        """Test that duplicate email is rejected"""
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )

        with pytest.raises(ValidationError, match="Email already registered"):
            manager.create_user(
                username="alice2",
                email="alice@example.com",
                password="SecurePass123"
            )

    def test_create_duplicate_username(self, manager):
        """Test that duplicate username is rejected"""
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )

        with pytest.raises(ValidationError, match="Username already taken"):
            manager.create_user(
                username="alice",
                email="alice2@example.com",
                password="SecurePass123"
            )

    def test_create_user_with_invalid_data(self, manager):
        """Test creating user with invalid data"""
        with pytest.raises(ValidationError):
            manager.create_user(
                username="ab",  # Too short
                email="test@example.com",
                password="SecurePass123"
            )


class TestUserManagerRetrieval:
    """Test UserManager retrieval methods"""

    @pytest.fixture
    def manager_with_users(self):
        """Provide UserManager with test users"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123",
            first_name="Alice"
        )
        manager.create_user(
            username="bob",
            email="bob@example.com",
            password="SecurePass123",
            first_name="Bob"
        )
        manager.create_user(
            username="charlie",
            email="charlie@example.com",
            password="SecurePass123",
            first_name="Charlie"
        )
        return manager

    def test_get_user_by_id(self, manager_with_users):
        """Test retrieving user by ID"""
        user = manager_with_users.get_user(1)
        assert user is not None
        assert user.username == "alice"

    def test_get_nonexistent_user_by_id(self, manager_with_users):
        """Test getting nonexistent user returns None"""
        user = manager_with_users.get_user(999)
        assert user is None

    def test_get_user_by_username(self, manager_with_users):
        """Test retrieving user by username"""
        user = manager_with_users.get_user_by_username("bob")
        assert user is not None
        assert user.email == "bob@example.com"

    def test_get_user_by_username_not_found(self, manager_with_users):
        """Test getting nonexistent user by username returns None"""
        user = manager_with_users.get_user_by_username("unknown")
        assert user is None

    def test_get_user_by_email(self, manager_with_users):
        """Test retrieving user by email"""
        user = manager_with_users.get_user_by_email("charlie@example.com")
        assert user is not None
        assert user.username == "charlie"

    def test_get_user_by_email_not_found(self, manager_with_users):
        """Test getting nonexistent user by email returns None"""
        user = manager_with_users.get_user_by_email("notfound@example.com")
        assert user is None


class TestUserManagerDeletion:
    """Test UserManager deletion methods"""

    @pytest.fixture
    def manager_with_users(self):
        """Provide UserManager with test users"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        manager.create_user(
            username="bob",
            email="bob@example.com",
            password="SecurePass123"
        )
        return manager

    def test_delete_user_success(self, manager_with_users):
        """Test deleting an existing user"""
        assert manager_with_users.get_user_count() == 2

        result = manager_with_users.delete_user(1)

        assert result is True
        assert manager_with_users.get_user_count() == 1
        assert manager_with_users.get_user(1) is None

    def test_delete_nonexistent_user(self, manager_with_users):
        """Test deleting nonexistent user returns False"""
        result = manager_with_users.delete_user(999)
        assert result is False
        assert manager_with_users.get_user_count() == 2


class TestUserManagerUpdate:
    """Test UserManager update methods"""

    @pytest.fixture
    def manager_with_user(self):
        """Provide UserManager with a user"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        return manager

    def test_update_first_name(self, manager_with_user):
        """Test updating user's first name"""
        updated_user = manager_with_user.update_user(1, first_name="Alice")

        assert updated_user is not None
        assert updated_user.first_name == "Alice"

    def test_update_last_name(self, manager_with_user):
        """Test updating user's last name"""
        updated_user = manager_with_user.update_user(1, last_name="Smith")

        assert updated_user is not None
        assert updated_user.last_name == "Smith"

    def test_update_is_active(self, manager_with_user):
        """Test updating user's active status"""
        updated_user = manager_with_user.update_user(1, is_active=False)

        assert updated_user is not None
        assert updated_user.is_active is False

    def test_update_multiple_fields(self, manager_with_user):
        """Test updating multiple fields at once"""
        updated_user = manager_with_user.update_user(
            1,
            first_name="Alice",
            last_name="Smith",
            is_active=False
        )

        assert updated_user is not None
        assert updated_user.first_name == "Alice"
        assert updated_user.last_name == "Smith"
        assert updated_user.is_active is False

    def test_update_nonexistent_user(self, manager_with_user):
        """Test updating nonexistent user returns None"""
        result = manager_with_user.update_user(999, first_name="Test")
        assert result is None


class TestUserManagerAuthentication:
    """Test UserManager authentication"""

    @pytest.fixture
    def manager_with_user(self):
        """Provide UserManager with a user"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        return manager

    def test_authenticate_success(self, manager_with_user):
        """Test successful authentication"""
        user = manager_with_user.authenticate("alice", "SecurePass123")

        assert user is not None
        assert user.username == "alice"
        assert user.last_login is not None

    def test_authenticate_wrong_password(self, manager_with_user):
        """Test authentication with wrong password"""
        user = manager_with_user.authenticate("alice", "WrongPassword123")
        assert user is None

    def test_authenticate_nonexistent_user(self, manager_with_user):
        """Test authentication with nonexistent user"""
        user = manager_with_user.authenticate("unknown", "SecurePass123")
        assert user is None

    def test_authenticate_inactive_user(self, manager_with_user):
        """Test authentication with inactive user"""
        manager_with_user.update_user(1, is_active=False)

        user = manager_with_user.authenticate("alice", "SecurePass123")
        assert user is None


class TestUserManagerStatistics:
    """Test UserManager statistics and queries"""

    @pytest.fixture
    def manager_with_mixed_users(self):
        """Provide UserManager with active and inactive users"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        manager.create_user(
            username="bob",
            email="bob@example.com",
            password="SecurePass123"
        )
        manager.create_user(
            username="charlie",
            email="charlie@example.com",
            password="SecurePass123"
        )
        manager.update_user(2, is_active=False)
        return manager

    def test_get_user_count(self, manager_with_mixed_users):
        """Test getting total user count"""
        count = manager_with_mixed_users.get_user_count()
        assert count == 3

    def test_get_active_users(self, manager_with_mixed_users):
        """Test getting all active users"""
        active_users = manager_with_mixed_users.get_active_users()
        assert len(active_users) == 2
        assert all(user.is_active for user in active_users)

    def test_get_inactive_users(self, manager_with_mixed_users):
        """Test getting all inactive users"""
        inactive_users = manager_with_mixed_users.get_inactive_users()
        assert len(inactive_users) == 1
        assert all(not user.is_active for user in inactive_users)

    def test_get_active_user_count(self, manager_with_mixed_users):
        """Test getting count of active users"""
        count = manager_with_mixed_users.get_active_user_count()
        assert count == 2

    def test_search_users_by_username(self, manager_with_mixed_users):
        """Test searching users by username"""
        results = manager_with_mixed_users.search_users("ali")
        assert len(results) == 1
        assert results[0].username == "alice"

    def test_search_users_by_email(self, manager_with_mixed_users):
        """Test searching users by email"""
        results = manager_with_mixed_users.search_users("bob")
        assert len(results) == 1
        assert results[0].username == "bob"

    def test_search_users_multiple_results(self, manager_with_mixed_users):
        """Test search returning multiple results"""
        results = manager_with_mixed_users.search_users("a")
        assert len(results) >= 2

    def test_search_users_case_insensitive(self, manager_with_mixed_users):
        """Test that search is case-insensitive"""
        results_lower = manager_with_mixed_users.search_users("alice")
        results_upper = manager_with_mixed_users.search_users("ALICE")

        assert len(results_lower) == len(results_upper)
        assert results_lower[0].username == results_upper[0].username

    def test_search_users_no_results(self, manager_with_mixed_users):
        """Test search with no results"""
        results = manager_with_mixed_users.search_users("xyz")
        assert len(results) == 0


class TestUserManagerReset:
    """Test UserManager reset operations"""

    @pytest.fixture
    def manager_with_logged_in_users(self):
        """Provide UserManager with logged-in users"""
        manager = UserManager()
        manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123"
        )
        manager.create_user(
            username="bob",
            email="bob@example.com",
            password="SecurePass123"
        )
        manager.authenticate("alice", "SecurePass123")
        manager.authenticate("bob", "SecurePass123")
        return manager

    def test_reset_all_logins(self, manager_with_logged_in_users):
        """Test resetting all login times"""
        user1 = manager_with_logged_in_users.get_user(1)
        user2 = manager_with_logged_in_users.get_user(2)

        assert user1.last_login is not None
        assert user2.last_login is not None

        count = manager_with_logged_in_users.reset_all_logins()

        assert count == 2
        assert user1.last_login is None
        assert user2.last_login is None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple operations"""

    def test_complete_user_lifecycle(self):
        """Test complete user lifecycle"""
        manager = UserManager()

        # Create user
        user = manager.create_user(
            username="alice",
            email="alice@example.com",
            password="SecurePass123",
            first_name="Alice",
            last_name="Smith"
        )
        assert manager.get_user_count() == 1

        # Login
        authenticated = manager.authenticate("alice", "SecurePass123")
        assert authenticated is not None
        assert authenticated.last_login is not None

        # Update
        updated = manager.update_user(
            user.user_id,
            last_name="Johnson"
        )
        assert updated.last_name == "Johnson"

        # Get user
        retrieved = manager.get_user(user.user_id)
        assert retrieved.get_full_name() == "Alice Johnson"

        # Convert to dict
        user_dict = retrieved.to_dict()
        assert user_dict["full_name"] == "Alice Johnson"

        # Deactivate
        retrieved.deactivate()
        assert retrieved.is_active is False

        # Cannot login when inactive
        failed_auth = manager.authenticate("alice", "SecurePass123")
        assert failed_auth is None

        # Delete
        deleted = manager.delete_user(user.user_id)
        assert deleted is True
        assert manager.get_user_count() == 0

    def test_multi_user_operations(self):
        """Test operations with multiple users"""
        manager = UserManager()

        # Create multiple users
        users_data = [
            ("alice", "alice@example.com", "Alice", "Smith"),
            ("bob", "bob@example.com", "Bob", "Johnson"),
            ("charlie", "charlie@example.com", "Charlie", "Brown"),
        ]

        for username, email, first, last in users_data:
            manager.create_user(
                username=username,
                email=email,
                password="SecurePass123",
                first_name=first,
                last_name=last
            )

        # Verify all created
        assert manager.get_user_count() == 3

        # Authenticate all
        for username, _, _, _ in users_data:
            user = manager.authenticate(username, "SecurePass123")
            assert user is not None

        # Search
        results = manager.search_users("a")
        assert len(results) >= 2

        # Deactivate one
        manager.update_user(2, is_active=False)
        assert manager.get_active_user_count() == 2

        # Verify statistics
        assert len(manager.get_active_users()) == 2
        assert len(manager.get_inactive_users()) == 1
