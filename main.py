import requests
# import json
from dotenv import load_dotenv
from os import getenv

def main():

    # Base variables
    base_url: str = "https://vilni-zl.edus.school/api"
    url_auth: str = base_url + '/user/login/'

    # Class definitions -->
    class User:
        def __init__(self, uuid, access, refresh):
            self.uuid: str = uuid
            self.access: str = access
            self.refresh: str = refresh
            self.header_auth: dict = { "Authorization": f'Bearer {self.access}' }
            self.url = Url(self)
        #     self.class_id = self.get_class_id()
        # def get_class_id(self):
        #     request = requests.get(self.url.account, headers=self.header_auth)
        #     json = request.json()
        #     class_id = json["class_id"]
        #     return class_id
        def get_homework(self):
            request = requests.get(self.url.homework, headers=self.header_auth)
            homework_json = request.json()
            return homework_json
        def pretty_homework(self):
            print()
            json = self.get_homework()
            prev_date = ""
            
            for e in json["next"]:
                if e["prepare_till"] != prev_date:
                    print("## " + e["prepare_till"] + "\n")

                print("### " + e["lesson"]["name"], e["theme"]["name"] + "\n", sep=" - ")
                lesson_id = e["theme"]["id"]

                is_files: bool = False
                for task in e["homework_tasks"]:
                    if task["is_files"]:
                        is_files = True
                        if e["class_group_id"]:
                            lesson_url = base_url + f'/teacher/lesson-planning-theme/details/{lesson_id}/?filter_class_group={e["class_group_id"]}&is_student=true'
                        else:
                            lesson_url = base_url + f'/teacher/lesson-planning-theme/details/{lesson_id}/?filter_class={e["class_id"]}&is_student=true'
                        request = requests.get(lesson_url, headers=self.header_auth)
                        json = request.json()
                        for material in json["materials"]:
                            if material["type"] == 2:
                                if material["files"]:
                                    files = []
                                    for file in material["files"]:
                                        if file["file_url"]:
                                            files.append(file["file_url"])
                                        if file["external_url"]:
                                            files.append(file["external_url"])
                                    files_string = ", ".join(files)
                                    print("- [ ] " + material["description"] + ":", files_string)
                                else:
                                    print("- [ ] " + material["description"])
                prev_date = e["prepare_till"]
                if is_files:
                    print()
                    continue
                else:
                    for task in e["homework_tasks"]:
                        print("- [ ] " + task["title"])        
    
                print()
                        
    class Url:
        def __init__(self, user):
            self.homework = base_url + f'/student/homework-tasks/{user.uuid}/active/'
            self.notifications = base_url + f'/user/notification/?user={user.uuid}'
            self.grades = base_url + f'/journal/student-scores/{user.uuid}/'
            self.rewards = base_url + f'/student/reward/{user.uuid}/'
            self.account = base_url + f'/student/account/{user.uuid}/'
    # <-- End of class definitions

    # AUTH -->
    load_dotenv()
    login = getenv("LOGIN")
    password = getenv("PASSWORD")
    login_data = {
        "login": login,
        "password": password
    }

    dummy_file = {
        'upload_field_name': ('my_dummy_file.txt', b'Dummy content.', 'text/plain')
    }
    
    res_auth = requests.post(url_auth, data=login_data, files=dummy_file)  
    auth_json = res_auth.json()
    # End of AUTH

    user = User(auth_json["uuid"], auth_json["access"], auth_json["refresh"])

    # res_homework = requests.get(user.url.homework, headers=user.header_auth)
    # homework_json = res_homework.json()

    # with open("output/homework.json", "w") as homework_file:
    #     homework_file.write(json.dumps(homework_json, indent=2, ensure_ascii=False))
        
    # print(json.dumps(homework_json["next"][1], indent=2, ensure_ascii=False))
    user.pretty_homework()
if __name__ == "__main__":
    main()
