import json
import names
import lorem
import random
import glob
import os
import datetime
# from static_data import values_for_db

def generate_about_me_text(int):
    text = ''
    if int <= 0:
        int = 1
    for i in range(int):
        para = lorem.paragraph()
        text = f'{text}/n{para}'
    return text

def generate_random_email(first_name, last_name):
    domains = [ 'hotmail.com', 'gmail.com', 'aol.com', 'mail.com' , 'mail.kz', 'yahoo.com']
    random_domain = random.choice(domains)
    return f'{first_name}.{last_name}@{random_domain}'

def generate_placeholder_avatar():
    pic_number = random.randint(1, 70)
    return f'https://i.pravatar.cc/150?img={pic_number}'

def create_user_record_dict(pk):
    random_user_type = random.choice([1, 2])
    random_first_name = names.get_first_name()
    random_last_name =  names.get_last_name()
    record_dict = {
        'model': 'tutorbook.user',
        'pk': pk,
        'fields':{
            'first_name': random_first_name,
            'last_name': random_last_name,
            'email': generate_random_email(random_first_name, random_last_name),
            'user_type': random_user_type,
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'updated_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'profile_img_url': generate_placeholder_avatar()
        }
    }
    return record_dict

def main():
    print('How many records would you like to generate?')
    records = int(input())
    # Delete the current fixtures
    filelist = glob.glob('tutorbook/fixtures/*.json')
    for file in filelist:
        os.remove(file)
    # Create the json files and save them to fixtures
    json_object = []
    for record in range(records):
        json_object.append(create_user_record_dict(record + 1))
    with open('tutorbook/fixtures/seed_data.json', 'w') as file:
        file.write(json.dumps(json_object))

if __name__ == "__main__":
    main()