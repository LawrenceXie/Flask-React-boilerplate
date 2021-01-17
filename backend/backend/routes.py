import time
import sys
import sqlite3
import os
import datetime
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from werkzeug.exceptions import abort
from backend import db
from backend.models import Items, Admin

bp = Blueprint("blog", __name__)

adminReset = [{'key': 'main_lazy_loading',
               'value': 'true',
               'format': 'text'},
              {'key': 'side_lazy_loading',
               'value': 'true',
               'format': 'text'},
              {'key': 'main_num_notes_to_render',
               'value': '10',
               'format': 'int'},
              {'key': 'side_num_notes_to_render',
               'value': '5',
               'format': 'int'},
              {'key': 'main_default_depth',
               'value': '3',
               'format': 'int'},
              {'key': 'side_default_depth',
               'value': '0',
               'format': 'int'},
              {'key': 'db_last_updated',
               'value': time.time(),
               'format': 'float'}]

itemsReset = [{'id': 'e83bcd2f',
          'date_created': int(time.time()),
          'date_updated': int(time.time()),
          'text': 'This is some text.'},
         {'id': '568d26da',
          'date_created': int(time.time()),
          'date_updated': int(time.time()),
          'text': 'Lorem ipsum and cats.'},
         {'id': '023adf31',
          'date_created': int(time.time()),
          'date_updated': int(time.time()),
          'text': 'In the beginning...'},
         {'id': 'a7cd35ae',
          'date_created': int(time.time()),
          'date_updated': int(time.time()),
          'text': 'And the last, at last.'}]


@bp.route('/')
def index():
  return ('<h1>Flask Backend</h1><p>See the repository for more information.</p>')


@bp.route('/admin', methods=['GET', 'POST'])
def admin():

  # if GET, return all admin keypairs
  if request.method == 'GET':
    adminItems = Admin.query.all()
    print(adminItems)
    adminItemsToReturn = []
    for item in adminItems:
      newAdminItem = {'id': item.id,
                      'key': item.key,
                      'value': item.value,
                      'format': item.format}
      adminItemsToReturn.append(newAdminItem)
    return jsonify(list(adminItemsToReturn))

  # if POST, handle the json data
  else:
    reqObj = request.json

    if (reqObj['method'] == 'CREATE'):
      adminItemToAdd = Admin(reqObj['key'], reqObj['value'], reqObj['format'])
      db.session.add(adminItemToAdd)
      db.session.commit()
      return jsonify({'operation':'CREATE', 'status': 'COMPLETE'})

    elif (reqObj['method'] == 'READ'):
      adminItemToRead = Admin.query.filter_by(key=reqObj['key']).first()
      return jsonify({'operation':'READ', 'adminItem': adminItemToRead})

    elif (reqObj['method'] == 'UPDATE'):
      adminItemToUpdate = Admin.query.filter_by(key=reqObj['key']).first()
      adminItemToUpdate.value = reqObj['value']
      adminItemToUpdate.format = reqObj['format']
      db.session.commit()
      return jsonify({'operation':'UPDATE', 'status': 'COMPLETE'})

    elif (reqObj['method'] == 'DELETE'):
      adminItemToDelete = Admin.query.filter_by(key=reqObj['key']).first()
      db.session.delete(adminItemToDelete)
      db.session.commit()
      return jsonify({'operation':'DELETE', 'status': 'COMPLETE'})


@bp.route('/items', methods=['GET', 'POST'])
def items():

  # if GET, return all admin keypairs
  if request.method == 'GET':
    items = Items.query.all()
    print(items)
    itemsToReturn = []
    for item in items:
      newItemToAdd = {'id': item.id,
                      'date_created': item.date_created,
                      'date_updated': item.date_updated,
                      'text': item.text}
      itemsToReturn.append(newItemToAdd)
    return jsonify(list(itemsToReturn))

  # if POST, handle the json data
  else:
    reqObj = request.json

    if (reqObj['method'] == 'CREATE'):
      itemToAdd = Items(reqObj['id'], reqObj['date_created'], reqObj['date_updated'], reqObj['text'])
      db.session.add(itemToAdd)
      db.session.commit()
      return jsonify({'operation':'CREATE', 'status': 'COMPLETE'})

    elif (reqObj['method'] == 'READ'):
      itemToRead = Items.query.filter_by(id=reqObj['id']).first()
      return jsonify({'operation':'READ', 'adminItem': itemToRead})

    elif (reqObj['method'] == 'UPDATE'):
      itemToUpdate = Items.query.filter_by(id=reqObj['id']).first()
      itemToUpdate.date_created = reqObj['date_created']
      itemToUpdate.date_updated = reqObj['date_updated']
      itemToUpdate.text = reqObj['text']
      db.session.commit()
      return jsonify({'operation':'UPDATE', 'status': 'COMPLETE'})

    elif (reqObj['method'] == 'DELETE'):
      itemToDelete = Items.query.filter_by(id=reqObj['id']).first()
      db.session.delete(itemToDelete)
      db.session.commit()
      return jsonify({'operation':'DELETE', 'status': 'COMPLETE'})


@bp.route('/admin/reset')
def admin_reset():
  global adminReset
  for keypair in adminReset:
    keyPairToAdd = Admin.query.filter_by(key=keypair['key']).first()
    if keyPairToAdd == None:
      keyPairToAdd = Admin(key=keypair['key'], value=keypair['value'], format=keypair['format'])
      db.session.add(keyPairToAdd)
      db.session.commit()
    else:
      keyPairToAdd.key = keypair['key']
      keyPairToAdd.value = keypair['value']
      keyPairToAdd.format = keypair['format']
      db.session.commit()

  return jsonify(adminReset)


@bp.route('/items/reset')
def items_reset():
  global itemsReset
  for item in itemsReset:
    itemToAdd = Items.query.filter_by(id=item['id']).first()

    if itemToAdd == None:
      itemToAdd = Items(id=item['id'], date_created=item['date_created'],
                        date_updated=item['date_updated'], text=item['text'])
      db.session.add(itemToAdd)
      db.session.commit()
    else:
      itemToAdd.id = item['id']
      itemToAdd.date_created = item['date_created']
      itemToAdd.date_updated = item['date_updated']
      itemToAdd.text = item['text']
      db.session.commit()

  return jsonify(itemsReset)


@bp.route('/backup')
def backup():
    os.system("sqlite3 backend/db/db.sqlite .dump > backend/db/dump.sql && sqlite3 backend/db/db.sqlite .schema > backend/db/schema.sql && git add backend/db && git commit -m 'Back up database'")
    return jsonify({'backup_status': 'SUCCESS'})


@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
