from db.db_utils import SessionLocal, User, Role
import os
from dotenv import load_dotenv

# Load environment variables from kaas.env file
load_dotenv(dotenv_path='kaas.env')

NO_OF_ADMINS = int(os.getenv('NO_OF_ADMINS'))
print(f"NO_OF_ADMINS: {NO_OF_ADMINS}")

def get_password_hash(password):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def create_super_admin():
    db = SessionLocal()
    try:
        # First check if any user with Admin role exists
        admin_role = db.query(Role).filter(Role.name == 'Admin').first()
        if admin_role:
            admin_count = db.query(User).filter(User.role_id == admin_role.id).count()
            print(f"Number of admin users in the system: {admin_count}")
            if admin_count >= NO_OF_ADMINS:
                print("An admin user already exists in the system.")
                db.close()
                return

        # Get credentials from environment variables or input
        admin_email = os.getenv('ADMIN_EMAIL') or input(
            "Enter admin email: "
        )

        # Check if email already exists
        existing_user = db.query(User).filter(User.email == admin_email).first()
        if existing_user:
            raise ValueError(f"User with email {admin_email} already exists. Please use a different email.")

        admin_password = os.getenv('ADMIN_PASSWORD') or input(
            "Enter admin password: "
        )

        # Create admin role if it doesn't exist
        if not admin_role and admin_count < NO_OF_ADMINS:
            admin_role = Role(name='Admin')
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        # Create super admin user
        admin_user = User(
            name="Admin",
            email=admin_email,
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
    finally:
        db.close()

if __name__ == "__main__":
    create_super_admin()