Instructions:

First, let's install the core packages. Run these commands one by one:

bash
pip install streamlit
bash
pip install python-dotenv
bash
pip install requests
Now install development tools (for code quality):

bash
pip install black ruff
Let's verify all packages installed correctly:

bash
pip list




You should see at least these packages:

streamlit

python-dotenv

requests

black

ruff

Let's also create a requirements.txt file. This is important for deployment and reproducibility:

bash
pip freeze > requirements.txt
Check the requirements file:

bash
head -10 requirements.txt

_________________________________________


Why we install these packages:

streamlit: For building our web app UI

python-dotenv: To load environment variables from .env file

requests: To make API calls to OpenRouter

black: Code formatter (keeps our code clean and consistent)

ruff: Super fast linter (finds and fixes code issues)

Why requirements.txt is important:

Streamlit Cloud uses this to install dependencies when deploying

Other developers can recreate the exact same environment

It's a standard in Python projects
_________________________________________
