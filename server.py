from flask import Flask, request, make_response
from subprocess import CalledProcessError, check_output, STDOUT, Popen, PIPE
import json
import os
import ssl

current_dir = os.path.dirname(os.path.abspath(__file__))

# get environment variables
debugmode = os.getenv('DEBUG', False)
token = os.getenv('TOKEN', '')
useSSL = os.getenv('SSL', False)
listen = os.getenv('LISTEN', '0.0.0.0')

# setup SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(os.path.join(current_dir, 'cert.pem'), os.path.join(current_dir, 'key.pem'))

app = Flask(__name__)

@app.route('/')
def index():
    try:

        # check token
        if token:
            reqToken = request.args.get('token', '')

            if token != reqToken:
                res = make_response('Forbidden', 403)
                res.headers['Content-Type'] = 'text/plain'
                return res;

        args = request.args.get('command', '').split(' ')
        command = [ 'certbot' ]

        if len(args) > 1:
            command = command + args

        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout = proc.stdout.read()
        stderr = proc.stderr.read()

        output = json.dumps({ 'command': command, 'stdout': stdout, 'stderr': stderr }, indent=2)

        res = make_response(output)
        res.headers['Content-Type'] = 'application/json'
        return res

    except (CalledProcessError, OSError) as e:
        res = make_response('Error in certbot process: ' + str(e), 500)
        res.headers['Content-Type'] = 'text/plain'
        return res

if __name__ == '__main__':
    if useSSL:
        app.run(debug=debugmode, host=listen, ssl_context=context)
    else:
        app.run(debug=debugmode, host=listen)
