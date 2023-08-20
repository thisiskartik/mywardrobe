# MyWardrobe.in

Conversational Fashion Outfit Generator powered by GenAI.

## Setup for development

-   Clone the repository.
-   Go to `backend` folder, create a virtual environment and install all the requirements in `requirements.txt` file.
-   Inside the `backend` folder create a `.env` file and set following environment variables:
    -   `DEBUG_MODE`: set this to `True`
    -   `DJANGO_SECRET_KEY`: Create a secret key for Django.
    -   `OPENAI_API_KEY`: Set OpenAI API Key to access it's LLM models.
-   Inside the backend folder run `npm run migrate`
-   Go to `frontend` folder and run `npm install`
-   Finall run `npm run dev` in `frontend` folder and `python manage.py runserver` in `backend` folder.
-   Open the application in `http://localhost:3000`

## Production

Live production application is available at [MyWardrobe.in](http://mywardrobe.in)
