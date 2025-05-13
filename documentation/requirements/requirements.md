# Feature Description and Requirements

## Feature: User Authentication

### 1. Description

Users should be able to sign up, log in, and log out securely.

### 2. Requirements

- User must provide a valid username and password to register
- User must re-confirm the password to register
- Passwords must be hashed before storing in database
- Login should validate username and password credentials
- Successful login creates a session
- Logout should clear the session and redirect to homepage

## Feature: Recipe Creation

### 1. Description

Users should be able to create recipes by adding ingredients and steps.

### 2. Requirements

- Users can create a recipe with a title, short description, ingredients, steps, time to make, and number of servings.
- Users can select ingredients from the available database.
- Users can successively add ingredients to their recipe.
- Users can select corresponding amounts and weights for the ingredients.
- Users can remove any ingredient from their list of ingredients.
- Users can successivley add steps to their recipe.
- Users can remove any step from their list of steps.

## Feature: Sustainability Rating

### 1. Description

Each recipe has a sustainability rating based on the ingredients used.

### 2. Requirements

- The system calculates a sustainability rating by:
  - using a database of ingredients and their corresponding estimated carbon dioxide emitted per gram of ingredient
  - summing the emissions from each selected ingredient
  - for each ingredient, we multiply the user-specified weight by a unit conversion factor to convert it to grams
  - then multiply by the number of servings and the CO₂ emissions per gram from the database
  - we divide by 1000 to convert the result from grams to kilograms
  - this process is repeated for all selected ingredients
- Users can view the sustainabilty rating on each recipe.

## Feature: Recipe Bookmarking

### 1. Description

Users should be able to bookmark recipes to save them for later.

### 2. Requirements

- Users can bookmark recipes.
- Icon on recipe card shows if a recipe has been bookmarked.
- Users can unbookmark recipes when they no longer need them
- Users can view their bookmarked recipes.

## Feature: Recipe Discovery

### 1. Description

Users should be able to search for recipes based on what they contain.

### 2. Requirements

- Users can search recipes through keywords in title, author username, description, ingredients, and steps.
- Users can filter receipes by sustainability rating, newest, or alphabetically.
- Search should be efficient for large database of recipes.
