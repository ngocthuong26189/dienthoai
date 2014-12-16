from flask import Blueprint
from flask import request, abort, redirect, session, make_response
from services import render
from models.like import Like
from services import identity
import json
from datetime import datetime

module = Blueprint('api.like', __name__)

@module.route('/<string:topic_id>', methods=['GET'])
def view_by_topic(topic_id):
    like = Like.objects()
    return render.json(json.loads(like.to_json()))

@module.route('/<string:topic_id>', methods=['POST'])
@identity.permission_required(1)
def like(topic_id):
    try:
        userId = json.loads(session.get('user')).get('_id').get('$oid')
        like = Like.objects(topic=topic_id,user=userId)
        if like:
            return render.json("Liked"), 400
        data = {'topic':topic_id,'user':userId}
        Like.objects.create(**data)
        return render.json("Created"), 201
    except Exception, e:
        return render.json("Bad request"), 400

@module.route('/<string:topic_id>', methods=['DELETE'])
@identity.permission_required(1)
def dislike(topic_id):
    try:
        userId = json.loads(session.get('user')).get('_id').get('$oid')
        Like.objects(topic=topic_id,user=userId).delete()
        return render.json("OK"), 200
    except Exception, e:
        return render.json("Bad request"), 400