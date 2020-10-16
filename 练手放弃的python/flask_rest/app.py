from flask import Flask
from flask_restful import Api, Resource, request


app = Flask(__name__)
api = Api(app)


datas = [{'id': 1, 'name': 'xag', 'age': 18}, {'id': 2, 'name': 'xingag', 'age': 19}]

class UserView(Resource):
    def get(self):
        return {"code":200, 'msg': "success", 'data': datas}

    def post(self):
        json_data = request.get_json()

        new_id = len(datas) +1
        datas.append({'id':new_id, **json_data})

        return {'code': 200, 'msg': 'ok', 'success': datas[new_id - 1]}


api.add_resource(UserView, '/user')

@app.route("/")
def hello():
    return "hello, flask"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)