# CS160 Project

A sustainable recipe-sharing platform that promotes reducing one's carbon footprint. It allows users to share recipes with sustainable ingredients and cooking techniques, which others can view. It also is a service that allows users to learn about sustainable cooking methods, the carbon footprint of ingredients, and find locally sourced ingredients.

Technologies used

- MySQL
- Python
- Primevue
- Vue

Demo on [YouTube](https://youtu.be/G-J9-ZoIDn4)

## How to Run

### **Database**

#### **AWS MySQL Database**

Our application uses a MySQL database hosted on AWS. The connection details for the AWS database are stored in environment variables and configured accordingly. We created the database's tables by connecting to the database through MySQL workbench and executing the sql script _createdb.sql_ found in the /backend directory.

#### **Local MySQL Database**

For local development, you need to set up a local MySQL database, configure the connection details in environment variables, and run the sql script _createdb.sql_ found in the /backend directory to create the tables.

Your .env file should be located in the /backend directory and should be formatted like this:

```
DB_URL=localhost
DB_PORT=3306
DB_UNAME=root
DB_PSWD=password
DB_NAME=project_db
TOKEN_KEY=SOME_KEY
```

### **Backend**

#### **Ensure you are in the backend directory**

```sh
cd /backend
```

#### **(Optional) create a virtual environment**

```sh
python3 -m venv venv
source venv/bin/activate
```

#### **Install pipenv globally or within the virtual environment**

```sh
pip install pipenv
```

#### **Create a virtual envrionment and install dependencies from the Pipfile**

```sh
pipenv install
```

#### **Activate the virtual environment created by pipenv**

```sh
pipenv shell
```

#### **Start the Flask server**

```sh
python3 main.py
```

**The Flask server will run on <code>http://127.0.0.1:5000</code>**

### **Frontend**

#### **Ensure you are in the frontend/reshare directory**

```sh
cd /frontend/reshare
```

#### Install dependencies from package.json

```sh
npm install
```

#### **Start the Vue app using Vite**

```sh
npm run dev
```

**The Vite app will run on <code>http://127.0.0.1:5173</code>**
