from wsgiref.simple_server import make_server
import demo
import lstm_name2gender
import json

def application(environ, start_response):
    path_info = environ.get('PATH_INFO')
    print("http_origin:", environ.get("HTTP_ORIGIN"))
    http_method = environ.get("REQUEST_METHOD")
    print("http_method: ", http_method)
    response_headers = [('Content-Type', 'application/json'),
        ( "Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Headers","content-type"),
        ("Access-Control-Allow-Methods", "GET")]
    status = "500 Internal Server Error"
    response_body = {}
    if http_method in [None, "OPTION"]:
        start_response(status, response_headers)
        return [ bytes("", encoding='utf-8') ]
    else:
        genderModel = lstm_name2gender.LSTMModel()
        if path_info and path_info.startswith("/match/"):
            _, name = path_info.rsplit('/', maxsplit=1)
            name = name.strip().capitalize()
            print("name: ", name)
            print("name_length: ", len(name))
            print("gender_prediction:", genderModel.predict(name))

            response_body.update(demo.sm(name))
            gender, proba = genderModel.predict(name)
            gender = int(gender)
            proba = list(proba)
            proba = [float(x) for x in proba]
            response_body.update({"inferred_gender": {"gender": gender, "proba": proba}})
            status = '200 OK'
        response_body_in_bytes = bytes(json.dumps(response_body), encoding="utf-8")
        start_response(status, response_headers)
        print(str(response_body))
        return [ response_body_in_bytes ]


if __name__ == '__main__':
    httpd = make_server('0.0.0.0', 8000, application)
    httpd.serve_forever()
