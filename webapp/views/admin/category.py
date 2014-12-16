# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request, abort
from models.category import Category
from services import render
from mongoengine import *
from services.paginate import Paginate
from services.cache import rebuilt_category_product


module = Blueprint('admin.category', __name__)

@module.route('/')
def index():
    categorys = Category.objects()
    return render.template('admin/category/index.html', categorys=categorys)

@module.route('/<string:category_id>', methods=['GET'])
def detail(category_id):
    try:
        category = Category.objects(id=str(category_id)).first()
        if category is None:
            return abort(404)
        return render.template('admin/category/detail.html', category = category)
    except Exception, e:
        abort(404)
    

@module.route('/', methods=['POST'])
def create():
    try:
        data = request.form.to_dict()
        if data.get('link'):
            data['link'] =  data['link'].encode('ascii', 'ignore')
            data['link'] = data['link'].replace(' ','-')
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        ancestorpath = []
        if "parent" in data:
            if data['parent'] == '':
                del data['parent']
            parent = Category.objects.get(id=data['parent'])
            ancestorpath = parent.ancestors
            ancestorpath.append(parent)
        data['ancestors'] = ancestorpath
        category = Category.objects.create(**data)
        return render.template('admin/category/detail.html', category = category), 201
    except NotUniqueError as e:
        abort(400, "Duplicated, category is existed") # Duplicate
    except ValidationError as ve:
        abort(400, "Validation Error")
    except DoesNotExist as dne:
        abort(400, "DoesNotExist Error")
    except Exception, e:
        abort(404)
@module.route('/<string:category_id>/update', methods=['POST'])
def update(category_id):
    try:
        data = request.form.to_dict()
        if data.get('link'):
            data['link'] =  data['link'].encode('ascii', 'ignore')
            data['link'] = data['link'].replace(' ','-')
        temp_data = data
        ancestorpath = []
        data = dict((k, v) for (k, v) in data.iteritems() if len(str(v).strip())>0)
        category = Category.objects.get(id=str(category_id)) # cha
        if category is None:
            return abort(400)
        update_map = dict([('set__' + key, value) for key, value in data.items()])
        if update_map.has_key('set__parent'):
            if update_map['set__parent'] == category_id:
                return abort(400)
            parent = Category.objects(id=str(update_map['set__parent'])).first() # con
            if parent is None:
                return abort(400)
            ancestorpath = parent.ancestors
            ancestorpath.append(parent)
            """
            Check category in child's ancestors when update a category with its parent is its descendant
            If category in child's ancestors return True
            else return False
            """
            def ancestors(parent, child):
                if parent.id == child.id:
                    return True
                if child.parent is None:
                    return False
                return ancestors(parent, child.parent)

            if ancestors(category,parent):
                return abort(400)    

        if temp_data.has_key('parent'):
            if len(str(temp_data['parent']).strip()) == 0:
                update_map['set__parent'] = None
        update_map['set__ancestors'] = ancestorpath     
        category.update(**update_map)
        category.reload

        # get all child
        children = Category.objects(ancestors__contains=category.id)
        def getpath(path,child):
            if child.parent is None:
                return path
            path.insert(0,child.parent)
            return getpath(path, child.parent)
        #update ancestors in child
        for child in children:
            child_path = getpath([],child)
            child.ancestors = child_path  
            child.save()
        rebuilt_category_product()  
        return render.template('admin/category/detail.html', category = category.reload()), 200
    except Exception as e:
        abort(400)

@module.route('/create', methods=['GET'])
def add():
    categories = Category.objects()
    return render.template('admin/category/create.html',categories=categories)

@module.route('/<string:category_id>/edit', methods=['GET'])
def edit(category_id):
    try:
        category = Category.objects.get(id=category_id)
        categories = Category.objects()
        def is_can_be_parent(can_be_parent, can_be_child):
            def get_ancestors(list,child):
                if child is None:
                    return list
                if child.parent is not None:
                    list.append(child.parent.id)
                return get_ancestors(list, child.parent)
            """
            to check can_be_parent is child of can_be_child much get all child of can_be_child
            to get all child of can_be_child much check all category with each category as c has ancestors, 
            which has can_be_child => c is child of can_be_child
            if can_be_parent in list child of can_be_child return false
            """
            list_child_of_child = []
            for c in categories:
                list = []
                list = get_ancestors(list,c)
                if can_be_child.id in list:
                    list_child_of_child.append(c.id)
            if can_be_parent.id in list_child_of_child:
                return False
            if can_be_child.parent is not None:
                if can_be_child.parent.id == can_be_parent.id:
                    return True
            if can_be_child.id == can_be_parent.id:
                return False
            return True
        categories = filter(lambda can_be_parent: is_can_be_parent(can_be_parent,category), categories);
        return render.template('admin/category/edit.html', category=category,categories=categories)
    except Exception:
        abort(404, "404 does not exist")
@module.route('/<string:category_id>/delete', methods=['POST'])
def delete(category_id):
    try:
        category = Category.objects.get(id=category_id)        
        children = Category.objects(ancestors__contains=category.id)
        num = category.delete()
        def getpath(path,child):
            if child.parent is None:
                return path
            path.insert(0,child.parent)
            return getpath(path, child.parent)
        #update ancestors in child
        for child in children:
            child_path = getpath([],child)
            child.ancestors = child_path  
            child.save()
        return render.template('admin/category/detail.html', category=category)
    except Exception:
        abort(404)
