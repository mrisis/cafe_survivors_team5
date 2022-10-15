import argparse
from cafe.models import Users
from cafe import db

parser = argparse.ArgumentParser(description='change to admin_user')

parser.add_argument('--phone', type=str, help='user_id')


args=parser.parse_args()

if args.phone:
    user = Users.query.filter_by(phone_number = args.phone).first()
    user.admin = True
    db.session.commit()
    print(f'User {user} is now admin')

