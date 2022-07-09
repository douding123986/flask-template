from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.database.topology import TopologyManage
from werkzeug.datastructures import ImmutableMultiDict
from apps.models import get_value
from apps.validates.topology_validate import AddTopologyForm, GetTopologyForm, ModifyTopologyForm, DeleteTopologyForm, \
    GetDevicePortForm
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from decorators import permission_required, file_required
import asyncio

topology_bp = Blueprint('topology_data', __name__, url_prefix='/api/v1/topology')


@topology_bp.route('/add_topology', methods=['POST'])
@permission_required('configure')
@jwt_required()
def add_topology():
    topology = request.json.get('topology') if request.json else ''
    form = AddTopologyForm(ImmutableMultiDict([('topology', topology)]))
    if form.validate():
        topology = TopologyManage(datadict=request.json, handle_type='add_topology')
        result, code = handle_route(topology, del_redis_key='topology')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@topology_bp.route('/delete_topology', methods=['POST'])
@permission_required('configure')
@jwt_required()
def delete_topology():
    form = DeleteTopologyForm(request.form)
    if form.validate():
        topology = TopologyManage(datadict=get_form_data(form), handle_type='delete_topology')
        result, code = handle_route(topology, del_redis_key='topology')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@topology_bp.route('/modify_topology', methods=['POST'])
@permission_required('configure')
@jwt_required()
def modify_topology():
    topology = str(request.json.get('topology')) if request.json else ''
    topology_id = str(request.json.get('topology_id')) if request.json else ''
    form = ModifyTopologyForm(ImmutableMultiDict([('topology', topology), ('topology_id', topology_id)]))
    if form.validate():
        topology = TopologyManage(datadict=request.json, handle_type='modify_topology')
        result, code = handle_route(topology, del_redis_key='topology')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@topology_bp.route('/search_topology', methods=['GET'])
@jwt_required()
def search_topology():
    form = GetTopologyForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()).replace(':', '') + '_device_topology'
        accounts_data = asyncio.run(get_value(redis_key))
        if accounts_data:
            return jsonify({'msg': 'success', 'data': eval(accounts_data), 'code': 200}), 200
        topology = TopologyManage(datadict=get_form_data(form), handle_type='search_topology')
        result, code = handle_route(topology, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@topology_bp.route('/import_topology', methods=['POST'])
@file_required()
@permission_required('configure')
@jwt_required()
def import_topology():
    uploaded_file = request.files.get('file')
    topology = TopologyManage(upload_file=uploaded_file, handle_type='import_topology')
    result, code = handle_route(topology, del_redis_key='device')
    return jsonify(result), code


@topology_bp.route('/export_topology', methods=['GET'])
@jwt_required()
def export_topology():
    topology = TopologyManage(handle_type='export_topology')
    if topology.data.get('result'):
        return topology.data.get('data')
    return jsonify({'msg': topology.data.get('message'), 'code': 403}), 403


@topology_bp.route('/get_topology', methods=['GET'])
@jwt_required()
def get_topology():
    form = GetDevicePortForm(request.args)
    if form.validate():
        topology = TopologyManage(datadict=get_form_data(form), handle_type='get_topology')
        result, code = handle_route(topology)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
