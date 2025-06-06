import os

# File paths
USER_FILE = "users.txt"
MOVIE_FILE = "movies.txt"
BOOKING_FILE = "bookings.txt"

# Base User class with encapsulated attributes and authentication
class User:
    def __init__(self, username, password, role):
        self.__username = username
        self.__password = password
        self.role = role

    def authenticate(self, username, password):
        return self.__username == username and self.__password == password

    def get_username(self):
        return self.__username

# Admin class - inherits from User
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def add_movie(self):
        print("\n--- Add Movie ---")
        name = input("Enter movie name: ").strip()
        genre = input("Enter genre: ").strip()
        showtime = input("Enter showtime (e.g., 5:00 PM): ").strip()
        seats = input("Enter available seats: ").strip()

        # Enhanced validation
        if not name.replace(" ", "").isalpha():
            print("❌ Invalid movie name. Use alphabetic characters only.")
            return
        if not genre.replace(" ", "").isalpha():
            print("❌ Invalid genre. Use alphabetic characters only.")
            return
        if not showtime:
            print("❌ Showtime cannot be empty.")
            return
        if not seats.isdigit() or int(seats) <= 0:
            print("❌ Seats must be a positive integer.")
            return

        try:
            with open(MOVIE_FILE, "a") as f:
                f.write(f"{name},{genre},{showtime},{seats}\n")
            print("✅ Movie added successfully.")
        except Exception as e:
            print(f"❌ Error adding movie: {e}")

    def view_movies(self):
        try:
            with open(MOVIE_FILE, "r") as f:
                movies = f.readlines()
                if not movies:
                    print("❌ No movies available.")
                    return
                print("\n🎬 Available Movies:")
                for idx, movie in enumerate(movies):
                    print(f"{idx+1}. {movie.strip()}")
        except FileNotFoundError:
            print("❌ Movie list file not found.")

    def delete_movie(self):
        self.view_movies()
        try:
            movie_num = int(input("Enter movie number to delete: ").strip()) - 1
            with open(MOVIE_FILE, "r") as f:
                movies = f.readlines()
            if 0 <= movie_num < len(movies):
                movies.pop(movie_num)
                with open(MOVIE_FILE, "w") as f:
                    f.writelines(movies)
                print("✅ Movie deleted successfully.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error deleting movie: {e}")

    def view_bookings(self):
        try:
            with open(BOOKING_FILE, "r") as f:
                bookings = f.readlines()
                if bookings:
                    print("\n📖 All Bookings:")
                    for booking in bookings:
                        print(booking.strip())
                else:
                    print("❌ No bookings found.")
        except FileNotFoundError:
            print("❌ No bookings file found.")

    def search_movie(self):
        query = input("Enter movie name to search: ").strip().lower()
        try:
            with open(MOVIE_FILE, "r") as f:
                results = [line.strip() for line in f if query in line.lower()]
                if results:
                    print("\n🔍 Search Results:")
                    for i, m in enumerate(results):
                        print(f"{i+1}. {m}")
                else:
                    print("❌ No movies matched your search.")
        except FileNotFoundError:
            print("❌ Movie list not found.")

# Customer class - inherits from User
class Customer(User):
    def __init__(self, username, password):
        super().__init__(username, password, "customer")

    def view_movies(self):
        try:
            with open(MOVIE_FILE, "r") as f:
                movies = f.readlines()
                if movies:
                    print("\n🎬 Available Movies:")
                    for idx, movie in enumerate(movies):
                        print(f"{idx+1}. {movie.strip()}")
                else:
                    print("❌ No movies available.")
        except FileNotFoundError:
            print("❌ Movie list file not found.")

    def book_ticket(self):
        self.view_movies()
        try:
            movie_num = int(input("Enter movie number to book: ").strip()) - 1
            with open(MOVIE_FILE, "r") as f:
                movies = f.readlines()

            if 0 <= movie_num < len(movies):
                movie_data = movies[movie_num].strip().split(",")
                seats_available = int(movie_data[3])
                print(f"🪑 Seats Available: {seats_available}")
                seats_to_book = input("Enter number of seats to book: ").strip()

                if not seats_to_book.isdigit():
                    print("❌ Invalid seat input. Please enter a number.")
                    return

                seats_to_book = int(seats_to_book)

                if seats_to_book <= 0:
                    print("❌ Seat count must be greater than zero.")
                elif seats_to_book <= seats_available:
                    movie_data[3] = str(seats_available - seats_to_book)
                    movies[movie_num] = ",".join(movie_data) + "\n"
                    with open(MOVIE_FILE, "w") as f:
                        f.writelines(movies)
                    with open(BOOKING_FILE, "a") as f:
                        f.write(f"{self.get_username()},{movie_data[0]},{seats_to_book}\n")
                    print("✅ Booking successful.")
                else:
                    print("❌ Not enough seats available.")
            else:
                print("❌ Invalid movie selection.")
        except FileNotFoundError:
            print("❌ Movie list not found.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error booking ticket: {e}")

    def cancel_booking(self):
        try:
            with open(BOOKING_FILE, "r") as f:
                bookings = f.readlines()
            user_bookings = [b for b in bookings if b.startswith(self.get_username())]

            if not user_bookings:
                print("❌ You have no bookings to cancel.")
                return

            for idx, booking in enumerate(user_bookings):
                print(f"{idx+1}. {booking.strip()}")

            cancel_idx = int(input("Enter booking number to cancel: ").strip()) - 1

            if 0 <= cancel_idx < len(user_bookings):
                cancel_line = user_bookings[cancel_idx]
                bookings.remove(cancel_line)
                with open(BOOKING_FILE, "w") as f:
                    f.writelines(bookings)
                print("✅ Booking cancelled.")
            else:
                print("❌ Invalid selection.")
        except FileNotFoundError:
            print("❌ No booking records found. Please make a booking first.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"❌ Error cancelling booking: {e}")

    def search_movie(self):
        query = input("Enter movie name to search: ").strip().lower()
        try:
            with open(MOVIE_FILE, "r") as f:
                results = [line.strip() for line in f if query in line.lower()]
                if results:
                    print("\n🔍 Search Results:")
                    for i, m in enumerate(results):
                        print(f"{i+1}. {m}")
                else:
                    print("❌ No movies matched your search.")
        except FileNotFoundError:
            print("❌ Movie list not found.")

# Load users from file and return list of Admin or Customer objects
def load_users():
    users = []
    try:
        with open(USER_FILE, "r") as f:
            for line in f:
                username, password, role = line.strip().split(",")
                if role == "admin":
                    users.append(Admin(username, password))
                elif role == "customer":
                    users.append(Customer(username, password))
    except FileNotFoundError:
        pass
    return users

# Register new user
def register_user():
    print("\n---- Register ----")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (admin/customer): ").strip().lower()

    if role not in ["admin", "customer"]:
        print("❌ Invalid role. Please choose 'admin' or 'customer'.")
        return

    if not username or not password:
        print("❌ Username and password cannot be empty.")
        return

    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if line.strip().split(",")[0] == username:
                    print("❌ Username already exists.")
                    return

    try:
        with open(USER_FILE, "a") as f:
            f.write(f"{username},{password},{role}\n")
        print("✅ Registration successful! You can now log in.")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")

# Login existing user
def login(users):
    print("\n---- Login ----")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username == "admin" and password == "admin":
        print("✅ Logged in as admin.")
        return Admin("admin", "admin")

    for user in users:
        if user.authenticate(username, password):
            print(f"✅ Login successful as {user.role}.")
            return user
    print("❌ Login failed. Invalid username or password.")
    return None

# Show respective menu based on user role
def user_menu(user):
    while True:
        if isinstance(user, Admin):
            print("\n--- Admin Menu ---")
            print("1. Add Movie\n2. View Movies\n3. Delete Movie\n4. View Bookings\n5. Search Movie\n6. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                user.add_movie()
            elif choice == "2":
                user.view_movies()
            elif choice == "3":
                user.delete_movie()
            elif choice == "4":
                user.view_bookings()
            elif choice == "5":
                user.search_movie()
            elif choice == "6":
                print("👋 Logged out.")
                break
            else:
                print("❌ Invalid option.")
        elif isinstance(user, Customer):
            print("\n--- Customer Menu ---")
            print("1. View Movies\n2. Book Ticket\n3. Cancel Booking\n4. Search Movie\n5. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                user.view_movies()
            elif choice == "2":
                user.book_ticket()
            elif choice == "3":
                user.cancel_booking()
            elif choice == "4":
                user.search_movie()
            elif choice == "5":
                print("👋 Logged out.")
                break
            else:
                print("❌ Invalid option.")

# Program entry point
def main():
    while True:
        print("\n🎟️ Welcome to Movie Ticket Booking System 🎟️")
        print("1. Login\n2. Register\n3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            users = load_users()
            user = login(users)
            if user:
                user_menu(user)
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid input. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
