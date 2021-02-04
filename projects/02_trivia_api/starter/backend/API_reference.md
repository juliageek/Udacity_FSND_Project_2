# API Reference
_____

## Getting Started
+ Base URL: At present, this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the front-end configuration.
+ Authentication: This version of the application does not require authentication or API keys

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false,
    "error": 400,
    "message": "bad request"
}
```
The API will return 4 error types when requests fail:
+ 400: Bad request
+ 404: Resource Not Found
+ 405: Method Not Allowed
+ 422: Not Processable

## API Endpoints

### Questions
_____

#### GET /questions
+ General
    + Returns a list of questions, success value, total number of questions and a list of categories
    + Results are paginated in groups of 10. Include a request parameter to choose page number. The page parameter default is 1.
    
<details>
    <summary>Request</summary>

```
    curl http://127.0.0.1/questions
```
</details>

<details>
  <summary>Sample response</summary>

```

{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 26
}
```
</details>

#### POST /questions (new question)
+ General:
    + Allows the user to create a new question
  
+ Expected request body:
```
{
    "question": "Who was the last emperor of China?",
    "answer": "Henry Puyi",
    "difficulty": 4,
    "category": 4 //history
}
```
+ The API will return success value, created question id, list of questions, total number of questions

<details>
    <summary>Request</summary>
    
```
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who was the last emperor of China?", "answer": "Henry Puyi", "difficulty": 4, "category": 4}'
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "created": 36, 
  "current_questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 27
}
```

</details>


#### POST /questions (search for questions)
+ General:
    + Allows the user to search for questions based on a search term
+ Expected request body:
```
{
    "searchTerm": "World Cup"
}
```
+ The API will return success value, list of questions, total number of questions
<details>
    <summary>Request</summary>

```
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "China"}'
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "questions": [
    {
      "answer": "Henry Puyi", 
      "category": 4, 
      "difficulty": 4, 
      "id": 36, 
      "question": "Who was the last emperor of China?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```
</details>


#### DELETE /questions/{question_id}
+ General:
    + Allows the user to delete a question based on its id
+ The API will return success value and the id of the deleted question
<details>
    <summary>Request</summary>

```
curl http://127.0.0.1:5000/questions/2 -X DELETE
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "deleted": 2, 
  "success": true
}
```
</details>

### Categories
_____

#### GET /categories
+ General:
    + It allows the user to get all question categories
+ The API will return success value and a list of categories
<details>
    <summary>Request</summary>

```
curl http://127.0.0.1:5000/categories
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```
</details>

#### GET /categories/{category_id}/questions
+ General:
    + Allows the user to get all questions per category
+ The API will return success value, a list of questions, total number of questions and current category
<details>
    <summary>Request</summary>

```
curl http://127.0.0.1:5000/categories/1/questions
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "Nucleus", 
      "category": 1, 
      "difficulty": 2, 
      "id": 29, 
      "question": "What is the center of an atom called?"
    }, 
    {
      "answer": "Potassium", 
      "category": 1, 
      "difficulty": 2, 
      "id": 30, 
      "question": "What substance has the chemical symbol K?"
    }, 
    {
      "answer": "Inertia", 
      "category": 1, 
      "difficulty": 4, 
      "id": 31, 
      "question": "What is the 1st law of motion called?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 6
}
```
</details>

#### POST /categories/{category_id}/questions
+ General:
    + Allows the user to search within the questions of a specific category
+ The API will return success value, a list of questions, total number of questions and current category
+ Expected request body:
```
{
    "searchTerm": "Who"
}
```
<details>
    <summary>Request</summary>

```
curl http://127.0.0.1:5000/categories/4/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Who"}'
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "current_category": {
    "id": 4, 
    "type": "History"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Henry Puyi", 
      "category": 4, 
      "difficulty": 4, 
      "id": 36, 
      "question": "Who was the last emperor of China?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```
</details>

### Quizzes
_____
#### POST /quizzes
+ General:
    + Returns a new question from a specific category every time the endpoint is called
+ The API will return success value, a question, a list of previous questions
+ Expected request body:
```
{
    "previousQuestions": [9,11],
    "quizCategory": 1 //OPTIONAL
}
```

<details>
    <summary>Request</summary>
```
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16], "quiz_category": {"id": 2, "type":"Art"}}
```
</details>

<details>
    <summary>Sample response</summary>

```
{
  "previous_questions": [
    16, 
    18
  ], 
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true
}
```
</details>
