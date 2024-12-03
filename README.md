# PC-TEE

## Build the Environment

```bash
pip install flask tensorflow
```

## Train the Model

Generate data. This will output test_data.csv and train_data.csv under the current directory. The columns are Name_Length, Age, Income, and Label.

```bash
python generate.py
```

Train a simple model. The argument is the path of training data.

```bash
python train.py train_data.csv
```

## Website

Generate TSL key (key.pem is private key and cert.pem is certificate).

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

Run the service. This will start a https service on port 443. The website allows users to submit a csv file for prediction and show the results in the web page.

```bash
python app.py
```
