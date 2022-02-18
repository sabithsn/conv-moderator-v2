# Annotation Website Tutorial
This is a tutorial on how to set up the annotation website.

### Setting-up an AWS EC2 Instance

Before beginning the set-up of the annotation website, it is necessary to create an EC2 instance on Amazon AWS or any other cloud computing server. This EC2 instance will hold all of the back-end API serving using gunicorn; front-end serving using Apache; and database serving using MySQL.

In order to create an EC2 instance please follow the Amazon tutorial here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html

Here are some useful commands to use the EC2 instance:

#### Login to the EC2 Instance

```bash
ssh -i <path_to_your_ssh_key.pem> ubuntu@<DNS_NUMBERS>.<SERVER_LOCATION>.compute.amazonaws.com
```

As an example, my website's <DNS_NUMBERS> is ec2-3-138-110-97 and my <SERVER_LOCATION> is us-east-2.

#### Copy a Document to the EC2 Instance

```bash
scp -i <path_to_your_ssh_key.pem> <file_you_want_to_copy> ubuntu@<DNS_NUMBERS>.<SERVER_LOCATION>.compute.amazonaws.com:/home/ubuntu/annotation_website/
```

At this point you can copy everything under the annotation_website/ from your local machine to the AWS server using this command.

### Setting-up the Annotation Website

After the AWS server is launched, there are 3 main jobs that need to be done to set the annotation website:

1. Set up the back-end: Uses gunicorn
2. Set up the front-end: Uses Vue.js and Apache
3. Set up the database: Uses Apache server

### 1) Back-end with Gunicorn

The main code that you need to manipulate to change the back-end is app.py under the annotation_website/backend/ folder. This file handles the HTTP requests to the backend API and does computation on the given request using the functions in the app.py. An example HTTP request handling is:

```python
@app.route('/', methods=('GET', 'POST',))
def hello_world():
    return 'Hello World!'
```

Other examples can be found in app.py. Some possible functionalities of the back-end include login, annotate etc.

#### Serving with Gunicorn

After you make the necessary handling of the request, you can set up gunicorn on the AWS server to start the backend API. Please install gunicorn to the AWS using the following procedure: https://pypi.org/project/gunicorn/

We need to make the backend run indefinitely on our EC2 instance, so we need another session that will remain active even after we log out. We use tmux for this. To learn how to use tmux please refer to this documentation (https://tmuxcheatsheet.com/).

Login to your EC2 instance. Copy the app.py file to the AWS server under the backend folder. Open a new session using the "tmux" command. In order for app.py to run you need to install flask and pymysql as follows:

```bash
pip3 install pymysql
pip3 install flask_cors
```

Then start the gunicorn serving under PORT 5000 using:

```bash
gunicorn -b 0.0.0.0:5000 app:app
```

Then detach from the tmux session using (**Ctrl+B** then **D**) and let gunicorn listen indefinitely for HTTP requests on PORT 5000.

### 2) Front-end with Vue.js & Apache

In order to create a front-end you can either design your own front-end or modify the already-given frontend. If you would like to create your own front-end skip to the "Serving with Apache" section.

To modify the Vue.js you can directly use the already-present buttons and re-arrange. These are present under the frontend/src folder. Under this folder there are several files which correspond to the screens of the website. To learn more about Vue.js please refer to https://vuejs.org/v2/guide/

You need to convert the Vue.js files to html files and folders to serve as a frontend. To do this you need to download vue CLI to your local computer (https://cli.vuejs.org/#getting-started). After you install Vue CLI, you can run it using

```
vui ui
```

Then from the opened screen you need to import the project folder. After that you need to build the project and this will create a dist folder. Then you need to upload the contents of this folder to the AWS EC2 instance, under the frontend folder.

#### Serving with Apache

You need to install the Apache server on AWS EC2 instance, please refer to this tutorial: https://ubuntu.com/tutorials/install-and-configure-apache

You need to copy the contents of the frontend (or dist) to the /var/www/html folder in the AC2 instance

You can test your apache server by just inputting the following into your URL:

```html
http://<your_dns>
```

**ATTENTION:** Here http is important, it should not be https, otherwise it gives an error.

### 3) Database with MySQL

You need to install a MySQL server on the AC2 instance. To do this please refer to: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

After creating the MySQL server, it is necessary to initialize tables in the database. Please use the db.sql in the annotation_website/ to initialize the tables in the database. In order to do this you need to first get into the database using the 

```bash
mysql
```

command in the EC2 instance. Then you can run db.sql inside the mysql server. This will set-up all the tables. 

In the backend, the database is connected to save the annotation in the localhost under the **annotate()** function.

In order to extract all the values in the annotations table in the MySQL database you can use the following command while in the EC2 terminal (not inside mysql):

```bash
mysql -h localhost -u <YOUR_USERNAME> -p annotation -e "select * from annotation" -B > annotations_2020_11_15.tsv
```

