# Udacity Trivia API Project 

It's game night at Udacity and this Trivia project allows users play the trivia game and test their knowledge across different question categories. The project objective was to create an API and a unit test for implementing the API allowing it perform the following:

1. Display questions, either all questions or by category. Questions should show the question, category, difficulty and rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a string query.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Installing Dependencies

Developers should have Python v3.6.0 and above and pip installed. 


### Backend Dependencies 

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip install -r requirements.txt
```
or

```
pip3 install -r requirements.txt
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```
psql trivia < trivia.psql
```
or


```
psql -U <username> trivia < trivia.psql
```


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
py -m flask run
```

## Testing
To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
``` 

## API Reference

### Getting Started 
Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
Authentication: This version does not require authentication or API keys.

### Error Handling

There are four types of errors the API will return`;
- 400 - Bad Request
- 404 - Resource Not Found
- 422 - Unprocessable
- 500 - Internal Server Error

### Endpoints
#### GET '/categories'
- Fetches a dictionary of all available categories.
- Returns an object with a single key categories, that contains an array of objects containing id and type key:value pairs. 
- Returns the total number of categories 
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### GET '/categories/<int:id>/questions'
- Gets all questions in a specified category by id using url parameters
- Returns a JSON object with paginated questions from a specified category
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`
```
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "rating": null
    }
  ],
  "success": true,
  "total_questions": 1
}
```
#### POST '/categories'
- Creates a new category using JSON request parameters in the database
- Sample: `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type": "Technology" }'`
- Created category:
```
{
    "7": "Technology"
}
```
- JSON response
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Technology"
  }, 
  "success": true, 
  "created": 7,
  "total_categories": 7
}
```
#### GET '/questions'
- Returns a list of questions
  - Includes a list of categories
  - Paginated in groups of 10
  - Includes details of question such as category, difficulty, answer and id
- Sample: `curl http://127.0.0.1:5000/questions`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 4, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "rating": null
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'0?", 
      "rating": null
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", 
      "rating": null
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?", 
      "rating": null
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?", 
      "rating": null
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?", 
      "rating": null
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?", 
      "rating": null
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?", 
      "rating": null
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?", 
      "rating": null
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?", 
      "rating": null
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```

#### DELETE '/questions/<int:id>'
- Deletes a question by id using url parameters
- Returns id of deleted questions if successful
- Sample: `curl http://127.0.0.1:5000/questions/4 -X DELETE`
```
  {
    "deleted": 4, 
    "success": true
  }
```
#### POST '/questions'
- Creates a new question using JSON request parameters in the database
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What is the name of the song Beyonce sang with Wizkid?", "answer": "Brown Skin Girl", "difficulty": 2, "category": "5", "rating": 3 }'`
- Created question:
```
{
    "answer": "Brown Skin Girl", 
    "category": 5, 
    "difficulty": 2, 
    "id": 25, 
    "question": "What is the name of the song Beyonce sang with Wizkid?",
    "rating": 3
}
```
- JSON response:
```
{
  "created": 25, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": null
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": null
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "rating": null
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "rating": null
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?",
      "rating": null
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "rating": null
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "rating": null
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?",
      "rating": null
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?",
      "rating": null
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "rating": null
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```

#### POST '/questions/search'
- Searches for questions using a search term, 
- Returns a JSON object with paginated questions matching the search term
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "artist"}'`
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
      "rating": null
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
      "rating": null
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### POST '/play'
- Allows user to play the trivia game
- Uses JSON request parameters of a chosen category and previous questions
- Returns JSON object with random available questions which are not among previous used questions
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [7, 8], "quiz_category": {"type": "Geography", "id": "3"}}'`
```
{
  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?",
    "rating": null
  }, 
  "success": true
}
```
