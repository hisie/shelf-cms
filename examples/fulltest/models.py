#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask.ext.security import UserMixin, RoleMixin
from flask.ext.sqlalchemy import SQLAlchemy

from shelf.plugins.library import PictureModelMixin, RemoteFileModelMixin
from shelf.plugins.preview import PreviewableModelMixin
from shelf.plugins.i18n import LocalizedModelMixin
from shelf.plugins.workflow import WorkflowModelMixin, WORKFLOW_STATES
from shelf.plugins.page import PageModelMixin

db = SQLAlchemy()


#classe utilitaires

class LocalizedString(db.Model, LocalizedModelMixin):
    __tablename__ = "localized_string"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    lang = db.Column(db.String(2))
    translations = db.relationship('LocalizedString', lazy="joined", backref=db.backref("parent", remote_side=[id]))
    parent_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))

    def __unicode__(self):
        return self.value


class LocalizedText(db.Model, LocalizedModelMixin):
    __tablename__ = "localized_text"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text)
    lang = db.Column(db.String(2))
    translations = db.relationship('LocalizedText', lazy="joined", backref=db.backref("parent", remote_side=[id]))
    parent_id = db.Column(db.Integer, db.ForeignKey('localized_text.id'))


class Picture(db.Model, PictureModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))


class RemoteFile(db.Model, RemoteFileModelMixin):
    __tablename__ = "remote_file"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))

    def __unicode__(self):
        return self.path


#classes necessaire à flask-security et shelf
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


#classes de l'application

post_tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    name_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))
    name = db.relationship('LocalizedString', foreign_keys=(name_id,))

    posts = db.relationship(
        "Post", secondary=post_tags,
        backref=db.backref('tags', lazy='joined'))

    def __unicode__(self):
        return unicode(self.name)


class Post(db.Model, WorkflowModelMixin, PreviewableModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())

    publication_date = db.Column(db.Date)
    state = db.Column(db.Enum(*WORKFLOW_STATES))

    title_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))
    title = db.relationship('LocalizedString', foreign_keys=(title_id,))

    abstract_id = db.Column(db.Integer, db.ForeignKey('localized_text.id'))
    abstract = db.relationship('LocalizedText', foreign_keys=(abstract_id,))

    text_id = db.Column(db.Integer, db.ForeignKey('localized_text.id'))
    text = db.relationship('LocalizedText', foreign_keys=(text_id,))

    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    picture = db.relationship("Picture")

    attachment_id = db.Column(db.Integer, db.ForeignKey('remote_file.id'))
    attachment = db.relationship("RemoteFile")


class Page(db.Model, PreviewableModelMixin, PageModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    l_title_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))
    l_title = db.relationship('LocalizedString', foreign_keys=(l_title_id,))

    l_description_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))
    l_description = db.relationship('LocalizedString', foreign_keys=(l_description_id,))

    __mapper_args__ = {
        'polymorphic_on': name,
        'polymorphic_identity': 'page'
    }


class IndexPage(Page):
    intro_id = db.Column(db.Integer, db.ForeignKey('localized_string.id'))
    intro = db.relationship('LocalizedString', foreign_keys=(intro_id,))
    __mapper_args__ = {
        'polymorphic_identity': 'index'
    }


class ContactPage(Page):
    text_id = db.Column(db.Integer, db.ForeignKey('localized_text.id'))
    text = db.relationship('LocalizedText', foreign_keys=(text_id,))

    __mapper_args__ = {
        'polymorphic_identity': 'contact'
    }