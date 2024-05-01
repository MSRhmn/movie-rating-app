import requests

# Define base URL
base_url = "http://localhost:5000"


while True:
    # Sample user data
    print("\nMovie Rating Application Menu:")
    print(" 1. Add user data")
    print(" 2. Get movies list")
    print(" 3. Get movies list by ID")
    print(" 4. Add movies to DB")
    print(" 5. Rate a movie")
    choice = input("Enter your choice: ")

    if choice == "1":
        user_data = {
            "email": "john_doe@gmail.com",
            "password": "pass1",
        }

        # Login endpoint
        login_response = requests.post(f"{base_url}/login", json=user_data)
        print(login_response.json())  # Print the response
    elif choice == "2":
        # Get movies endpoint
        movies_response = requests.get(f"{base_url}/movies")
        print(movies_response.json())  # Print the response
    elif choice == "3":
        # Get movie by ID endpoint
        movie_id = 1  # Change the ID as needed
        movie_response = requests.get(f"{base_url}/movies/{movie_id}")
        print(movie_response.json())  # Print the response
    elif choice == "4":
        # Add movie endpoint
        new_movie_data = {
            "name": "The Wizard of Oz",
            "genre": "Fantasy",
            "rating": "PG-13",
            "release_date": "25-09-1939",
        }
        add_movie_response = requests.post(f"{base_url}/movies", json=new_movie_data)
        print(add_movie_response.json())  # Print the response
    elif choice == "5":
        # Rate movie endpoint
        rate_movie_data = {"rating": 4.5}
        rate_movie_id = 1  # Change the ID as needed
        rate_movie_response = requests.post(
            f"{base_url}/movies/{rate_movie_id}/rate", json=rate_movie_data
        )
        print(rate_movie_response.json())  # Print the response
    elif choice == "6":
        print("\nLogging out from the 'Movie Rating App'")
        break
    else:
        print("Please choice between '1, 2, 3, 4, 5, or 6'")
