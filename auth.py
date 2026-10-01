import bcrypt

from database import add_user, get_user_by_email


def hash_password(password):
    """Convert a plain-text password into a secure hash."""
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):
    """Check whether the entered password matches the stored hash."""
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def register_user(username, email, password):
    """Register a new user."""
    existing_user = get_user_by_email(email)

    if existing_user:
        return False, "Email is already registered."

    hashed_password = hash_password(password)

    success = add_user(
        username,
        email,
        hashed_password
    )

    if success:
        return True, "Account created successfully."

    return False, "Unable to create account."


def login_user(email, password):
    """Authenticate a user."""
    user = get_user_by_email(email)

    if not user:
        return False, None

    stored_password = user[3]

    if verify_password(password, stored_password):
        return True, user

    return False, None