# encoding: utf-8

import sqlalchemy as sa
from datetime import datetime
import ckan.model as model
import uuid

requests_table = sa.Table('requests', model.meta.metadata,
    sa.Column('id', sa.types.Integer, primary_key=True, autoincrement=True),
    sa.Column('package_id', sa.types.Text, primary_key=False, nullable=False),
    sa.Column('resource_id', sa.types.Text, primary_key=False, nullable=True),
    sa.Column('state', sa.types.Integer, primary_key=False, nullable=True),
    sa.Column('name', sa.types.Text, primary_key=False, nullable=True),
    sa.Column('email_address', sa.types.Text, primary_key=False, nullable=True),
    sa.Column('request_data', sa.types.Text, primary_key=False, nullable=False),
    sa.Column('token', sa.types.Text, primary_key=False, nullable=True),
    sa.Column('created', sa.types.TIMESTAMP, primary_key=False, default=datetime.now, nullable=False)
)
requests_table.create(checkfirst=True)

STATE_MAIL_SENT = 1
STATE_MAIL_UNSENT = 0

class Requests(model.DomainObject):

    def __init__(self, package_id, resource_id, state, name, email, request_data):
        self.package_id = package_id
        self.resource_id = resource_id
        self.state = state
        self.name = name
        self.email_address = email
        self.request_data = request_data
        self.token = uuid.uuid4()
        self.created = datetime.now()

    @classmethod
    def by_token(cls, token):
        return model.Session.query(cls) \
                .filter_by(token = token).first()

    @classmethod
    def by_dataset(cls, package_id, row, start):
        return model.Session.query(cls) \
            .filter_by(package_id = package_id) \
            .order_by(cls.created.desc()) \
            .limit(row) \
            .offset(start) \
            .all()

    @classmethod
    def request_count(cls, package_id):
        return model.Session.query(cls) \
                .filter_by(package_id = package_id) \
                .count()

    def update_status(self):
        self.state = STATE_MAIL_SENT
        self.commit()

model.meta.mapper(Requests, requests_table)
