import json
import names
import lorem
import random
import glob
import os
import datetime
import psycopg2
import environ
import numpy as np
from dateutil.relativedelta import relativedelta

env = environ.Env()
environ.Env.read_env('tutorbook_django/.env')

# Establish local DB connection
connection = psycopg2.connect(
    database=env('DB_NAME'), user=env('DB_USER'), password=env('DB_PASSWORD'), host=env('HOST'), port=env('PORT')
)
cursor = connection.cursor()
cursor.execute('''SELECT id FROM tutorbook_subject;''')
# Get the available id's for the Subject, Level and Location
subjects = np.array(cursor.fetchall()).flatten().tolist()
cursor.execute('''SELECT id FROM tutorbook_level;''')
levels = np.array(cursor.fetchall()).flatten().tolist()
cursor.execute('''SELECT id FROM tutorbook_location;''')
locations = np.array(cursor.fetchall()).flatten().tolist()


def generate_about_me_text(int):
    text = ''
    if int <= 0:
        int = 1
    for i in range(int):
        para = lorem.paragraph()
        text = f'{text}/n{para}'
    return text

def generate_random_email(first_name, last_name):
    domains = ['hotmail.com', 'gmail.com', 'aol.com',
               'mail.com', 'mail.kz', 'yahoo.com']
    random_domain = random.choice(domains)
    return f'{first_name}.{last_name}@{random_domain}'


def generate_placeholder_avatar():
    pic_number = random.randint(1, 70)
    return f'https://i.pravatar.cc/150?img={pic_number}'


def create_user_record_dict(pk):
    random_user_type = random.choice([1, 2])
    random_first_name = names.get_first_name()
    random_last_name = names.get_last_name()
    record_dict = {
        'model': 'tutorbook.user',
        'pk': pk,
        'fields': {
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


def create_tutor_record(pk, user_id):
    is_published = random.choice([True, False])
    subscription_expires_at = None
    published_at = None
    number_of_paragraphs = random.randint(0, 5)
    if is_published:
        published_at = str(datetime.datetime.now(datetime.timezone.utc))
        subscription_expires_at = str(datetime.datetime.now(
            datetime.timezone.utc) + relativedelta(years=1))

    locations_covered = random.choices(
        locations, k=random.randint(1, len(locations)))
    subjects_covered = random.choices(
        subjects, k=random.randint(1, len(subjects)))
    levels_covered = random.choices(levels, k=random.randint(1, len(levels)))
    record_dict = {
        'model': 'tutorbook.tutor',
        'pk': pk,
        'fields': {
            'published': is_published,
            'looking_for_assignment': random.choice([True, False]),
            'about_me': generate_about_me_text(number_of_paragraphs),
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'updated_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'published_at': published_at,
            'subscription_expires_at': subscription_expires_at,
            'user': user_id,
            'locations': locations_covered,
            'levels': levels_covered,
            'subjects': subjects_covered,
        }
    }
    return record_dict

def create_assignment_record(pk, user_id):
    is_published = random.choice([True, False])
    is_filled = False
    published_at = None
    number_of_paragraphs = random.randint(1, 3)
    if is_published:
        published_at = str(datetime.datetime.now(datetime.timezone.utc))
        is_filled = random.choice([True, False])

    record_dict = {
        'model': 'tutorbook.assignment',
        'pk': pk,
        'fields': {
            'published': is_published,
            'title': lorem.sentence(),
            'filled': is_filled,
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'updated_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'published_at': published_at,
            'description': generate_about_me_text(number_of_paragraphs),
            'user': user_id,
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
    # Clear the old tables in the database
    cursor.execute('''DELETE FROM tutorbook_tutor_levels;''')
    cursor.execute('''DELETE FROM tutorbook_tutor_locations;''')
    cursor.execute('''DELETE FROM tutorbook_tutor_subjects;''')
    cursor.execute('''DELETE FROM tutorbook_tutor;''')
    cursor.execute('''DELETE FROM tutorbook_message;''')
    cursor.execute('''DELETE FROM tutorbook_thread;''')
    cursor.execute('''DELETE FROM tutorbook_review;''')
    cursor.execute('''DELETE FROM tutorbook_assignment;''')
    cursor.execute('''DELETE FROM tutorbook_user;''')
    connection.commit()
    connection.close()
    # Create the user_seed.json files
    json_objects = []
    created_users_objects = []
    for record in range(records):
        record = create_user_record_dict(record + 1)
        json_objects.append(record)
        created_users_objects.append(record)
    # Create tutors and assignments
    tutor_pk = 1
    assignment_pk = 1
    for user in created_users_objects:
        if user['fields']['user_type'] == 2:
            record = create_tutor_record(tutor_pk, user['pk'])
            json_objects.append(record)
            tutor_pk += 1
        if user['fields']['user_type'] == 1:
            posted_assignment = random.choice([True, False])
            if posted_assignment:
                record = create_assignment_record(assignment_pk, user['pk'])
                json_objects.append(record)
                assignment_pk += 1

    # Write everything to a json file
    with open('tutorbook/fixtures/seed_data.json', 'w') as file:
        file.write(json.dumps(json_objects))


if __name__ == "__main__":
    main()
