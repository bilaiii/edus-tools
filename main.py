import requests
import io

def main():
    url = "https://vilni-zl.edus.school/api/user/login/"

    login_data = {
        "login": "Любомир",
        "password": "36JA85"
    }

    dummy_content = b"This is some dummy content for the file."
    dummy_file_object = io.BytesIO(dummy_content)
    files = {
        'upload_field_name': ('my_dummy_file.txt', dummy_file_object, 'text/plain')
    }
    
    response = requests.post(url, data=login_data, files=files)

    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

if __name__ == "__main__":
    main()
