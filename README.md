# certbot-server
Docker container to send commands to Certbot from within an other container
- [Check on Docker Hub](https://hub.docker.com/r/pieterscheffers/certbot-server/)

### Environment variables
- `DEBUG`  (true/false, default: false) Should the Flask server run in debug mode?
- `TOKEN`  (string, default: '') When set, a token is required to get a response
- `SSL`    (true/false, default: false) Should the server use a self-signed certificate and only listen on https?
- `LISTEN` (ip string, default: '0.0.0.0') Listening interface

### GET params
- `command` An uri encoded string of parameters for the [`certbot`](https://certbot.eff.org/docs/using.html#certbot-command-line-options) application
- `token` The token to check for. If the environment variable `TOKEN` isn't set, this variable isn't used
