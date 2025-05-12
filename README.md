# CS160 Project

A sustainable recipe-sharing platform that promotes reducing one's carbon footprint. It allows users to share recipes with sustainable ingredients and cooking techniques, which others can view. It also is a service that allows users to learn about sustainable cooking methods, the carbon footprint of ingredients, and find locally sourced ingredients.

Technologies used

- MySQL
- Python
- Primevue
- Vue

## How to Run

### Backend

#### Ensure you are in the backend directory

```sh
cd /backend
```

#### (Optional) create a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

#### Install pipenv globally or within the virtual environment

```sh
pip install pipenv
```

#### Create a virtual envrionment and install dependencies from the Pipfile

```sh
pipenv install
```

#### Activate the virtual environment created by pipenv

```sh
pipenv shell
```

#### Start the Flask server

```sh
python3 main.py
```

The Flask server will run on <code>http://127.0.0.1:5000</code>

### Frontend

#### Ensure you are in the frontend/reshare directory

```sh
cd /frontend/reshare
```

#### Install dependencies from package.json

```sh
npm install
```

#### Start the Vue app using Vite

```sh
npm run dev
```

The Vite app will run on <code>http://127.0.0.1:5173</code>
