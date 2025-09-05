import requests

def main():
    url = "https://vilni-zl.edus.school/api/user/login/"

    login_data = {
        "login": "Любомир",
        "password": "36JA85"
    }
    dummy_file = {
        'upload_field_name': ('my_dummy_file.txt', b'Dummy content.', 'text/plain')
    }
    
    response = requests.post(url, data=login_data, files=dummy_file)

    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

if __name__ == "__main__":
    main()
