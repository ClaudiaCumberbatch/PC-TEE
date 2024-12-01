# PC-TEE

Environment preparation: 

```bash
pip install flask
```

Generate TSL key (key.pem is private key and cert.pem is certificate):

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

Run the service:

```bash
python app.py
```
