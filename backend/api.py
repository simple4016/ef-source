from flask import Flask, url_for, request, json
from flask_restful import Resource, Api
from flask_cors import CORS

import sys
sys.path.append('./common')

from db_tables import app  # noqa: E402
sys.path.append('./service')


import service  # noqa: E402

api = Api(app)
CORS(app)



@app.route('/getAsset', methods=['GET'])
def api_getAsset():
    return service.get_Asset(request.args)


@app.route('/getGasPrice', methods=['GET'])
def api_getGasPrice():
    return service.get_Gas(request.args)




# this service API is split into /yUSDInfo and /userInfoInyUSD
@app.route('/getPrivateAsset', methods=['GET'])
def api_getPrivateAsset():
    return service.get_PrivateAsset(request.args)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='6011', debug=True, threaded=True)
