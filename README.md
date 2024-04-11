# LinkTool

LinkTool allows the user to enter a URL address and then has the option to generate a personalized QR code. LinkTool is also helpful when we want to send someone a link that is very long in that case, it's worth using the option to generate a shortened link that redirects the user to the original long URL.

## 🛠 Built With
* JavaScript
* HTML / CSS
* Django
  
## Installation

1. Install Python version 3.11 [(Python)](https://www.python.org/downloads/)

2. Pull the repository

3. I strongly recommend using a specific virtual environment for this project. You can create one by typing the following 
   command:

```bash
python -m venv <name-of-your-enviroment> 
```
* Activate the virtual environment:
Windows
```bash
.\env\Scripts\activate
```
macOS/Linux
```bash
source env/bin/activate
```
* And add them by accessing the interpreter settings and selecting the file from 
the folder where we created our virtual environment (name-of-your-environment -> Scripts -> python.exe).

4. To install all necessary libraries in the project terminal, type in:

```bash
pip install -r requirements.txt
```
5. If you have completed all the steps, you can run the project by typing the following command into your terminal:
```bash
python manage.py runserver 
```
* And type into your browser ' http://127.0.0.1:8000 '

## Running Tests

```bash
  python manage.py test
```

## The appearance of LinkTool

![image](https://github.com/zagwiktor/linktool-django/assets/92055936/e95bee2f-0dd7-4448-9072-bf25938a524a)
