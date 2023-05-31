# DestiKnow

### Introduction

The DestiKnow project is a web application where people can view travel information about countries. It features an interactive map which takes you to a webpage containing the information about the country that was clicked. The travel advice is from the perspective of a British national travelling from the UK. Information for 185 countries is stored in an external database.

### Usage

##### Running the app

To run the web application, the run_app_win.bat file can be run on windows to run the web application. On linux, navigate to the same direction as app.py and run

```bash
python3 app.py
```

##### Tests

To run the tests, run the run_tests.bat file. This will run all the tests in the `./tests` directory.

### Requirements

- flask

- flask-sqlalchemy
- flask-mysqldb
- python-env
- wtforms
- flask_wtf
- flask_login

The latest versions of these libraries were used as of 31th May, 2023.

### Installation

To install the required libraries, run the following command:

```bash
pip install -r requirements.txt
```
### Database

The database is stored in a MySQL database and is hosted by the university.

Any access is restricted to the university network or through an SSH tunnel.

For access to the database please contact the university.

### Data Sources

The data for the countries comes from various reliable sources such as the UK government.

Although this data is from a reliable source and is vetted by us there is always a likelhood of certain elements of the data being either incorrect or possibly out of date depending on when the data was collected.

The description for each country is created from generative AI so may have degree of inaccuracy however these descriptions have been checked byus and are generally accurate.

You can contribute your opinion of the accuracy of the data by clicking the upvote or downvote button on the country page.

### GitHub

This project has been devloped with GitHub and can be found at the following GitHub repository:

[Team 24 GitHub](https://github.com/newcastleuniversity-computing/CSC2033_Team24_22-23)

> Please be aware that the GitHub repository is private and you will need to be part of Newcastle University to access it.


### License

The map used for this project is available for use under the MIT license as stated within the map.html file.

The logo used for this project is available for use under the creative commons license.

A more detailed list of the licenses used can be found in the licenses.md file.

### Authors

- [Thomas](https://github.com/Pixel-Tomiii)
- [Renato](https://github.com/RenCos)
- [Cameron](https://github.com/CrBridge)
- [Bartosz]()
- [Utsav]()
- [Ryan]()




