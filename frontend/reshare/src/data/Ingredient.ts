export interface Ingredient {
    ingredient_name: String,
    amount: Number,
    weight: String
}

export interface Recipe_Result {
    recipe_id : Number,
    title : String,
    short_description : String,
    steps : String,
    time : String,
    servings : Number,
    author_username : String,
    sustainability_rating : Number,
    average_rating : Number,
    ingredients: Ingredient[]
}