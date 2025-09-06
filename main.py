import requests
import json

def main():

    class User:
        def __init__(self, uuid, access, refresh):
            self.uuid: str = uuid
            self.access: str = access
            self.refresh: str = refresh
    
    url = "https://vilni-zl.edus.school/api"

    login_data = {
        "login": "Любомир",
        "password": "36JA85"
    }
    dummy_file = {
        'upload_field_name': ('my_dummy_file.txt', b'Dummy content.', 'text/plain')
    }
    
    res_auth = requests.post(url + "/user/login/", data=login_data, files=dummy_file)

    print(f"Status Code: {res_auth.status_code}")
    auth_json = res_auth.json()

    user = User(auth_json["uuid"], auth_json["access"], auth_json["refresh"])
    header_auth = { "Authorization": f'Bearer {user.access}' }
    print(f'access = {user.access}')
    print(f'refresh = {user.refresh}')
    print(f'uuid = {user.uuid}')

    res_homework = requests.get(url + f'/student/homework-tasks/{user.uuid}/active/', headers=header_auth)
    homework_json = res_homework.json()

    print(homework_json)

if __name__ == "__main__":
    main()
