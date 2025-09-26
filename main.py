import requests
import getpass
import json
import os
from rich import print

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
        def get_notifications(self):
            request = requests.get(self.url.notifications, headers=self.header_auth)
            notifications_json = request.json()
            return notifications_json
        def pretty_notifications(self):
            json = self.get_notifications()
            results = json["results"]
            gendered_words = {
                1: "Оцінив",
                2: "Оцінила"
            }
            for result in results:
                relation_type = result["relation_type"]
                relation_object = result["relation_object"]
                sender = result["from_user"]
                if relation_type == "journalscore":
                    subject = relation_object.get('lesson', {}).get('name')
                    score_type = relation_object.get('score_type', {}).get('name')
                    score = relation_object.get('score')
                    comment = relation_object.get('teacher_comment')
                    sender_gender = sender.get('gender')
                    sender_name = sender.get('username')
                    print(f'{subject} ({sender_name}) {gendered_words[sender_gender]} {score_type}: {score}, {comment}\n')
        def pretty_homework(self):
            json = self.get_homework()
            prev_date = ""
            
            for e in json["next"]:
                if e["prepare_till"] != prev_date:
                    print("[black]"+"-"*term_width())
                    print()
                    print("[red][bold]" + e["prepare_till"] + "\n")

                print("[magenta]"+ e["lesson"]["name"] +" [black]- "+ "[magenta]"+e["theme"]["name"] + "\n")
                lesson_id = e["theme"]["id"]

                is_files: bool = False
                for task in e["homework_tasks"]:
                    if task["is_files"]:
                        is_files = True
                        continue
                if is_files:
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
                                print("[yellow]- [ ] [/yellow]" + material["description"] + ":", files_string)
                            else:
                                print("[yellow]- [ ] [/yellow]" + material["description"])
                else:
                    for task in e["homework_tasks"]:
                        print("[yellow]- [ ] [/yellow]" + task["title"])        
                prev_date = e["prepare_till"]
                print()
                        
    class Url:
        def __init__(self, user):
            self.homework = base_url + f'/student/homework-tasks/{user.uuid}/active/'
            self.notifications = base_url + f'/user/notification/?user={user.uuid}'
            self.grades = base_url + f'/journal/student-scores/{user.uuid}/'
            self.rewards = base_url + f'/student/reward/{user.uuid}/'
            self.account = base_url + f'/student/account/{user.uuid}/'
    # <-- End of class definitions

    def login_function():
        # AUTH -->

        try:
            with open("passwords.json", "r") as file:
                login_data = json.load(file)
        except FileNotFoundError:
            print()
            print("--- please login ---")
            login = input("Your login (Name, Email): ")
            password = getpass.getpass("Your password: ")
            print()

            login_data = {
                "login": login,
                "password": password
            }

            with open("passwords.json", "w") as file:
                json.dump(login_data, file, ensure_ascii=False)
                            
        dummy_file = {
            'upload_field_name': ('my_dummy_file.txt', b'Dummy content.', 'text/plain')
        }
        print("Logging you in...")
        res_auth = requests.post(url_auth, data=login_data, files=dummy_file)  
        auth_json = res_auth.json()
        if res_auth.status_code == 200:
            print("Login successful!")
        else:
            print("[red]ERR: Login unsuccessful, no error handling has been implemented yet")
            quit()
        # End of AUTH

        return auth_json

    def term_width():
        try:
            size = os.get_terminal_size()
            return size.columns
        except OSError:
            return 80
    
    def menu():
        with open("logo.txt","r") as file:
            logo = file.read()
        print()
        print("[white]"+logo)
        inp = ""
        while "q" not in inp:
            print("[black]"+"-"*term_width())
            print()
            print("""What do you want to do today?
1. See my notifications
2. Get a list of my homework tasks
Or input "q" to quit\n""")
            inp = input("Choose: ")
            print()
            if "1" in inp:
                user.pretty_notifications()
            elif "2" in inp:
                user.pretty_homework()
    auth = login_function()
    user = User(auth["uuid"], auth["access"], auth["refresh"])
    menu()
    # res_homework = requests.get(user.url.homework, headers=user.header_auth)
    # homework_json = res_homework.json()

    # with open("output/homework.json", "w") as homework_file:
    #     homework_file.write(json.dumps(homework_json, indent=2, ensure_ascii=False))
        
    # print(json.dumps(homework_json["next"][1], indent=2, ensure_ascii=False))
    # user.pretty_homework()
    # print(json.dumps(user.get_notifications(), indent=2, ensure_ascii=False))
if __name__ == "__main__":
    main()
