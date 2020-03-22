from flask import Flask, request, json, jsonify
import sys
sys.path.append('./')
import result
import mongoDB

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.before_request
def before_request():
    result.write_log('info', "User requests info, path: {0}, method: {1}, ip: {2}, agent: {3}".format(str(request.path), str(request.method), str(request.remote_addr), str(request.user_agent)))


@app.errorhandler(404)
def method_404(e):
    return result.result(404, "requested URL was not found on the server")


@app.errorhandler(405)
def method_405(e):
    return result.result(405, "http method is not allowed for the requested URL")

# --------------------------------------------------------------------------------------


@app.route('/', methods=["GET"])
def hello_world():
    return "Restful API for 591 rent web."
    # return jsonify(mongoDB.find_houses_by_owner_region('台北', '陳先生'))

@app.route('/ping', methods=["GET"])
def ping():
    return result.result(200, "ping successful", "Welcome to restful api server.")

@app.route('/agent', methods=["GET"])
def houses_list():
    # return json.dumps(mongoDB.houses_list(), ensure_ascii=False)
    return jsonify(mongoDB.houses_list())

@app.route('/phone/<num>', methods=["GET"])
def houses_by_phone(num):
    return mongoDB.find_houses_by_phone_num(num)

@app.route('/gender/<region>/<gender>', methods=["GET"])
def houses_by_gender_region(gender,region):
    return jsonify(mongoDB.find_houses_by_gender_region(gender, region))

@app.route('/owner/<name>/<region>', methods=["GET"])
def house_by_rn(name, region):
    return jsonify(mongoDB.find_houses_by_owner_region(name, region))

# @app.route('/<region>/<name>', methods=["GET"])
# def houses_by_region_name(region,name):
#     return jsonify(mongoDB.find_houses_by_owner_region(name,region))
# --------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(port=5000, debug=True)
