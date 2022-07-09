from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from apps.database.multiple import MultipleManage
from werkzeug.datastructures import ImmutableMultiDict
from apps.validates.multiple_validate import AddMultipleAccountForm, DeleteMultipleAccountForm, \
    ModifyMultipleAccountForm, GetMultipleAccountForm, ModifySomeMultipleAccountForm
from decorators import permission_required
from apps.models import get_value
from decorators import file_required
import asyncio

multiple_bp = Blueprint('multiple_data', __name__, url_prefix='/api/v1/multiple')


@multiple_bp.route('/search_account', methods=['GET'])
@jwt_required()
def search_multiple_account():
    form = GetMultipleAccountForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()).replace(':', '') + '_multiple_account'
        accounts_data = asyncio.run(get_value(redis_key))
        if accounts_data:
            return jsonify({'msg': 'success', 'data': eval(accounts_data), 'code': 200}), 200
        multiple = MultipleManage(datadict=get_form_data(form), handle_type='search_multiple_account')
        result, code = handle_route(multiple, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@multiple_bp.route('/add_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def add_multiple_account():
    json_data = request.json.items() if request.json else ''
    multiple_data = [(item[0], item[1]) for item in json_data]
    form = AddMultipleAccountForm(ImmutableMultiDict(multiple_data))
    if form.validate():
        multiple = MultipleManage(datadict=get_form_data(form), handle_type='add_multiple_account')
        result, code = handle_route(multiple, del_redis_key='multiple')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@multiple_bp.route('/modify_account', methods=['POST'])
@permission_required(['configure', 'other'])
@jwt_required()
def modify_multiple_account():
    json_data = request.json.items() if request.json else ''
    multiple_data = [(item[0], item[1]) for item in json_data]
    if get_jwt().get('author') == 'other':
        form = ModifySomeMultipleAccountForm(ImmutableMultiDict(multiple_data))
    else:
        form = ModifyMultipleAccountForm(ImmutableMultiDict(multiple_data))
    if form.validate():
        multiple = MultipleManage(datadict=get_form_data(form), handle_type='modify_multiple_account')
        result, code = handle_route(multiple, del_redis_key='multiple')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@multiple_bp.route('/delete_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def delete_multiple_account():
    form = DeleteMultipleAccountForm(request.form)
    if form.validate():
        multiple = MultipleManage(datadict=get_form_data(form), handle_type='delete_multiple_account')
        result, code = handle_route(multiple, del_redis_key='multiple')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@multiple_bp.route('/export_account', methods=['GET'])
@jwt_required()
def export_multiple_account():
    multiple = MultipleManage(handle_type='export_multiple_account')
    if multiple.data.get('result'):
        return multiple.data.get('data')
    return jsonify({'msg': multiple.data.get('message'), 'code': 403}), 403


@multiple_bp.route('/import_account', methods=['POST'])
@file_required()
@permission_required('configure')
@jwt_required()
def import_multiple_account():
    uploaded_file = request.files.get('file')
    multiple = MultipleManage(upload_file=uploaded_file, handle_type='import_multiple_account')
    result, code = handle_route(multiple, del_redis_key='multiple')
    return jsonify(result), code
