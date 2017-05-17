from flask import Flask, redirect
from flask_restful import reqparse
import functools


def get_base_mongo_model_class(db):
    from flask_mongoalchemy import MongoAlchemy
    assert isinstance(db, MongoAlchemy)

    class MappingModel(db.Document):
        path = db.StringField()
        target = db.StringField()
        i_path = db.Index().ascending('path').unique()

    return MappingModel


def get_base_sql_alchemy_model(db):
    from flask_sqlalchemy import SQLAlchemy
    assert isinstance(db, SQLAlchemy)

    class MappingModel(db.Model):
        path = db.Column(db.String(80), primary_key=True)
        target = db.Column(db.String(1024), nullable=False)

    return MappingModel


def __forwarder(path_mapper, default_url, path):
    target = path_mapper(path) or default_url
    return redirect(target)


def install_forwarder(app, rule, path_mapper, default_url=None):
    assert isinstance(app, Flask)
    assert callable(path_mapper)

    if not rule:
        rule = '/'
    if not rule.endswith('/'):
        rule += '/'

    if not default_url:
        default_url = rule
    partial = functools.partial(__forwarder, path_mapper, default_url)
    functools.update_wrapper(partial, __forwarder)
    app.route(rule + '<path:path>')(partial)


