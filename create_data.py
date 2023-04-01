import os
from app import db, create_app
from app.models import User, Role, Permission

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# delete the current database and populate it with the records below
with app.app_context():
    db.drop_all()
    db.create_all()

    # create the roles
    role1 = Role(name='user')
    role2 = Role(name='author')
    role3 = Role(name='editor')
    role4 = Role(name='admin')

    # create the permissions
    p1 = Permission(name='write_article')
    p2 = Permission(name='edit_article')
    p3 = Permission(name='delete_article')
    p4 = Permission(name='change_role')
    p5 = Permission(name='delete_user')
    p6 = Permission(name='create_user')
    p7 = Permission(name='admin')

    # add permissions to roles
    role2.permissions.append(p1)
    role3.permissions.extend([p1,p2,p3])
    role4.permissions.extend([p1,p2,p3,p4,p5,p6,p7])

    # create the admin
    u1 = User(username='admin', password='admin', email='bpker@pm.me', role_id=4, confirmed=True)

    db.session.add_all([role1,role2,role3,role4])
    db.session.add_all([p1,p2,p3,p4,p5,p6,p7])
    db.session.add(u1)
    db.session.commit()