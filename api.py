from flask import Flask
from flask_restful import Api, Resource
from subprocess import check_output, CalledProcessError, STDOUT
import json

app = Flask(__name__)
api = Api(app)


def getstatusoutput(cmd):
    try:
        data = check_output(
                cmd, shell=True, universal_newlines=True, stderr=STDOUT)
        status = 0
    except CalledProcessError as ex:
        data = ex.output
        status = ex.returncode
    if data[-1:] == '\n':
        data = data[:-1]
    return status, data


# Movie
# shows a single domain item and lets you delete a domain item
class Movie(Resource):
    def get(self, movie_id):
        status, result = getstatusoutput("./scraper.py " + movie_id)
        if status == 0:
            result = json.loads(result)
            httpStatusCode = 200
        else:
            result = {"Error": result}
            httpStatusCode = 500
        return result, httpStatusCode


api.add_resource(Movie, '/movie/amazon/<movie_id>')

if __name__ == '__main__':
    app.run(debug=True)
