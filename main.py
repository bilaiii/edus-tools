import requests
import json

def main():

    class User:
        def __init__(self, uuid, access, refresh):
            self.uuid: str = uuid
            self.access: str = access
            self.refresh: str = refresh
            # self.url_homework = base_url + f'/student/homework-tasks/{self.uuid}/active/'
            # self.url_notifications = base_url + f'/user/notification/?user={self.uuid}'
            # self.url_grades = base_url + f'/journal/student-scores/{self.uuid}/'
            # self.url_rewards = base_url + f'/student/reward/{self.uuid}'
            self.url = Url(self)
    class Url:
        def __init__(self, user):
            self.homework = base_url + f'/student/homework-tasks/{user.uuid}/active/'
            self.notifications = base_url + f'/user/notification/?user={user.uuid}'
            self.grades = base_url + f'/journal/student-scores/{user.uuid}/'
            self.rewards = base_url + f'/student/reward/{user.uuid}/'
    
    base_url = "https://vilni-zl.edus.school/api"
    url_auth = base_url + '/user/login/'
    login_data = {
        "login": "Любомир",
        "password": "36JA85"
    }
    dummy_file = {
        'upload_field_name': ('my_dummy_file.txt', b'Dummy content.', 'text/plain')
    }
    
    res_auth = requests.post(url_auth, data=login_data, files=dummy_file)

    print(f"Status Code: {res_auth.status_code}")
    auth_json = res_auth.json()

    user = User(auth_json["uuid"], auth_json["access"], auth_json["refresh"])
    header_auth = { "Authorization": f'Bearer {user.access}' }
    # print(f'access = {user.access}')
    # print(f'refresh = {user.refresh}')
    # print(f'uuid = {user.uuid}')

    res_homework = requests.get(user.url.homework, headers=header_auth)
    homework_json = res_homework.json()

    with open("output/homework.json", "w") as homework_file:
        homework_file.write(json.dumps(homework_json, indent=2, ensure_ascii=False))
            
    print()
    prev_date = ""
    for e in homework_json["next"]:
        if e["prepare_till"] != prev_date:
            print("## " + e["prepare_till"] + "\n")
        print("### " + e["lesson"]["name"], e["theme"]["name"] + "\n", sep=" - ")
        for task in e["homework_tasks"]:
            print("- [ ] " + task["title"])
        prev_date = e["prepare_till"]
        print()
        
    # print(json.dumps(homework_json["next"][1], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
