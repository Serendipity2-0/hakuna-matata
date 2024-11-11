from db.db_utils import SessionLocal, User, Role
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import sys
from getpass import getpass

# Load environment variables from kaas.env file
load_dotenv(dotenv_path='kaas.env')

# Initialize CryptContext once
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get NO_OF_ADMINS with error handling
try:
    NO_OF_ADMINS = int(os.getenv('NO_OF_ADMINS'))
except (TypeError, ValueError):
    print("Error: 'NO_OF_ADMINS' is not set or is not a valid integer in the 'kaas.env' file.")
    sys.exit(1)

print(f"NO_OF_ADMINS: {NO_OF_ADMINS}")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_super_admin():
    """
    Create a super admin user.

    Raises:
        ValueError: If the admin email already exists or if the maximum number of admins is reached.
    """
    with SessionLocal() as db:
        try:
            # First check if Admin role exists
            admin_role = db.query(Role).filter(Role.name == 'Admin').first()
            if admin_role:
                admin_count = db.query(User).filter(User.role_id == admin_role.id).count()
                print(f"Number of admin users in the system: {admin_count}")
                if admin_count >= NO_OF_ADMINS:
                    print("The maximum number of admin users already exists in the system.")
                    return
            else:
                admin_count = 0  # Initialize admin_count when admin_role does not exist

            # Get credentials from environment variables or input
            admin_email = input("Enter admin email: ").strip()
            admin_phone_number = input("Enter admin phone number: ").strip()

            # Check if email already exists
            existing_user = db.query(User).filter(User.email == admin_email).first()
            if existing_user:
                raise ValueError(f"User with email {admin_email} already exists. Please use a different email.")

            # Use getpass to securely input the password
            admin_password = input("Enter admin password: ")

            # Create admin role if it doesn't exist and under admin limit
            if not admin_role and admin_count < NO_OF_ADMINS:
                admin_role = Role(name='Admin')
                db.add(admin_role)
                db.commit()
                db.refresh(admin_role)
                print("Admin role created.")

            # Create super admin user
            admin_user = User(
                name="Admin",
                email=admin_email,
                phone_number=admin_phone_number,
                password=get_password_hash(admin_password),
                role=admin_role
            )
            db.add(admin_user)
            db.commit()
            print("Super admin created successfully.")

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    create_super_admin()
