from flask import Blueprint
from flask import request
from services import render
from models.comment import Comment
from services import identity
import json
from datetime import datetime

module = Blueprint('api.comment', __name__)

@module.route('/<string:topic_id>', methods=['GET'])
def view_by_topic(topic_id):
    comments = Comment.objects()
    return render.json(json.loads(comments.to_json()))

@module.route('/', methods=['POST'])
@identity.permission_required(1)
def create():
    try:
        data = request.form.to_dict()
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        comment = Comment.objects.create(**data)
        return render.json(json.loads(comment.to_json()))
    except Exception, e:
        return render.json("Bad request"), 400

@module.route('/<string:id>', methods=['PUT'])
@identity.permission_required(1)
def update(id):
    try:
        def todo():
            data = request.form.to_dict()
            if data['content'] is None or len(str(data['content']).strip()) == 0:
                return render.json("Bad request"), 400 
            update_map={}
            update_map['set__content'] = data['content']
            update_map['set__updated_at'] = datetime.utcnow
            comment = Comment.objects.get(id=id)
            comment.update(**update_map)
            comment.reload()
            return render.json(json.loads(comment.to_json()))

        current_userId = json.loads(session.get('user')).get('_id').get('$oid')
        comment = Comment.objects.get(id=comment_id)
        if comment is None:
            return render.json("Bad request"), 400
        user_of_topic = User.objects.get(id=comment.userId)
        if user_of_topic is None:
            return render.json("Bad request"), 400
        if str(user_of_topic.id) == str(current_userId):
            return todo()
        if json.loads(g.user).get('permission', 1) > user_of_topic.permission:
            return todo()
        return render.json("permission deny"), 403

    except Exception, e:
        return render.json("Bad request"), 400  


@module.route('/<string:topic_id>', methods=['DELETE'])
@identity.permission_required(1)
def delete(topic_id):
    try:
        def todo():
            comment = Comment.objects.get(id=topic_id)
            comment.delete()
            return render.json("OK"), 200

        current_userId = json.loads(session.get('user')).get('_id').get('$oid')
        comment = Comment.objects.get(id=comment_id)
        if comment is None:
            return render.json("Bad request"), 400
        user_of_topic = User.objects.get(id=comment.userId)
        if user_of_topic is None:
            return render.json("Bad request"), 400
        if str(user_of_topic.id) == str(current_userId):
            return todo()
        if json.loads(g.user).get('permission', 1) > user_of_topic.permission:
            return todo()
        return render.json("permission deny"), 403

    except Exception, e:
        return render.json("Bad request"), 400