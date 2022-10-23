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
    random_salt = random.randint(1, 20000)
    first_name_lower = first_name.lower()
    last_name_lower = last_name.lower()
    return f'{first_name_lower}.{last_name_lower}{random_salt}@{random_domain}'


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
        locations, k=random.randint(1, 5))
    subjects_covered = random.choices(
        subjects, k=random.randint(1, 5))
    levels_covered = random.choices(levels, k=random.randint(1, 5))
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


def create_review_record(pk, tutor_id, user_id):
    number_of_paragraphs = random.randint(0, 2)
    record_dict = {
        'model': 'tutorbook.review',
        'pk': pk,
        'fields': {
            'tutor': tutor_id,
            'user': user_id,
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'updated_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'rating': round(random.uniform(0, 5), 1),
            'review_text': generate_about_me_text(number_of_paragraphs),
        }
    }
    return record_dict

def create_thread_record(pk, tutor_id, user_id):
    record_dict = {
        'model': 'tutorbook.thread',
        'pk': pk,
        'fields': {
            'tutor': tutor_id,
            'user': user_id,
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'has_unread': random.choice([True, False]),
        }
    }
    return record_dict

def create_message_record(pk, tutor_id, user_id, thread_id):
    record_dict = {
        'model': 'tutorbook.message',
        'pk': pk,
        'fields': {
            'tutor': tutor_id,
            'user': user_id,
            'sender': random.choice(['u', 't']),
            'created_at': str(datetime.datetime.now(datetime.timezone.utc)),
            'thread_id': thread_id,
            'content': lorem.sentence(),
            'is_read': random.choice([True, False]),
        }
    }
    return record_dict

def main():
    print('How many user records would you like to generate?')
    records = int(input())
    print('How many reviews would you like to generate?')
    reviews = int(input())
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
    created_tutor_objects = []
    for user in created_users_objects:
        if user['fields']['user_type'] == 2:
            record = create_tutor_record(tutor_pk, user['pk'])
            json_objects.append(record)
            created_tutor_objects.append(record)
            tutor_pk += 1
        if user['fields']['user_type'] == 1:
            posted_assignment = random.choice([True, False])
            if posted_assignment:
                record = create_assignment_record(assignment_pk, user['pk'])
                json_objects.append(record)
                assignment_pk += 1
    # Create default user and tutor user pairs
    tutor_user_pairs = []
    for review in range(reviews):
        tutor_list = []
        user_list = []
        for user in created_users_objects:
            if user['fields']['user_type'] == 2:
                for tutor in created_tutor_objects:
                    if user['pk'] == tutor['fields']['user']:
                        tutor_list.append(tutor['pk'])
            if user['fields']['user_type'] == 1:
                user_list.append(user['pk'])
        tutor_user_pairs.append(
            [random.choice(tutor_list), random.choice(user_list)])

    # Create reviews based on pairs
    review_pk = 1
    for pair in tutor_user_pairs:
        record = create_review_record(review_pk, pair[0], pair[1])
        json_objects.append(record)
        review_pk += 1

    # Create threads and messages based on user pairs
    thread_pk = 1
    message_pk = 1
    for pair in tutor_user_pairs:
        number_of_messages = random.randint(0, 20)
        record = create_thread_record(thread_pk, pair[0], pair[1])
        json_objects.append(record)
        for message in range(number_of_messages):
            record = create_message_record(message_pk, pair[0], pair[1], thread_pk)
            json_objects.append(record)
            message_pk += 1
        thread_pk += 1

    # Write everything to a json file
    with open('tutorbook/fixtures/seed_data.json', 'w') as file:
        file.write(json.dumps(json_objects))


if __name__ == "__main__":
    main()
