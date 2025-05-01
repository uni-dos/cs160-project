<template>
    <Navbar />
    <div class="create-recipe">
        <h2>Create your Recipe</h2>
        <form @submit.prevent="handleSubmit" class="centered">
            <!-- Title -->
            <div class="title">
                <FloatLabel variant="on">
                    <InputText id="title" v-model="title" variant="filled" size="large" :invalid="invalidFields.title" @input="invalidFields.title = false"/>
                    <label for="title">Recipe Title</label>
                </FloatLabel>
                <small v-if="invalidFields.title" class="p-error">Please enter a recipe title.</small>
            </div>

            <!-- Short Description -->
            <div class="short-description">
                <FloatLabel variant="on">
                    <Textarea id="short-description" v-model="short_description" variant="filled" size="large" rows="10" cols="30" :invalid="invalidFields.short_description" @input="invalidFields.short_description = false"></Textarea>
                    <label for="short-description">Short Description</label>
                </FloatLabel>
            </div>

            <!-- Steps -->
            <div class="steps">
                <div v-for="(step, index) in steps" :key="index" class="step-entry">
                    <div class="step-row">
                        <FloatLabel variant="on">
                            <InputText id="steps" v-model="steps[index]" variant="filled" size="large"  :invalid="invalidFields.steps[index]" @input="invalidFields.steps[index]=false"/>
                            <label for="steps">Step {{  index + 1 }}</label>
                        </FloatLabel>
                        <Button class="remove-btn" icon="pi pi-trash" severity="danger" @click="removeStep(index)"></Button>
                    </div>
                </div>
                <Button label="Add a step" icon="pi pi-plus" @click="addStep"></Button>
            </div>

            <!-- Time -->
            <div class="time">
                <FloatLabel variant="on">
                    <InputNumber inputId="hours" v-model="hours" suffix=" hrs" fluid variant="filled" size="large" :min="0" showButtons mode="decimal" :invalid="invalidFields.hours" @input="invalidFields.hours = false" />
                    <label for="hours">Hours</label>
                </FloatLabel>
                <FloatLabel variant="on">
                    <InputNumber inputId="mins" v-model="mins" suffix=" mins" fluid variant="filled" size="large" :min="0" :max="59" showButtons mode="decimal" :invalid="invalidFields.minutes" @input="invalidFields.minutes = false"/>
                    <label for="mins">Minutes</label>
                </FloatLabel>
            </div>

            <!-- Servings -->
            <div class="servings">
                <FloatLabel variant="on">
                    <InputNumber inputId="servings" v-model="servings" suffix=" servings" fluid variant="filled" size="large" :min="0" showButtons :step="1" :invalid="invalidFields.servings" @input="invalidFields.servings = false"/>
                    <label for="servings">Number of Servings</label>
                </FloatLabel>
            </div>

            <!-- Ingredients -->
            <div class="ingredients">
                <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient-entry">
                    <div class="ingredient-row">
                        <FloatLabel variant="on">
                            <AutoComplete v-model="ingredients[index]" inputId="ingredientsSuggestions" dropdown :suggestions="ingredientsSuggestions" @complete="search" variant="filled" size="large" forceSelection @keydown.enter.prevent :invalid="invalidFields.ingredients[index]" @input="invalidFields.ingredients[index]=false" ></AutoComplete>
                            <label for="ingredientsSuggestions">Ingredient {{ index + 1 }}</label>
                        </FloatLabel>
                        <FloatLabel variant="on">
                            <InputNumber class="ingredientAmount" inputId="amount" v-model="selectedAmounts[index]" fluid variant="filled" size="large" :min="0" :minFractionDigits="0" :maxFractionDigits="2" showButtons :step="0.25" :invalid="invalidFields.selectedAmounts[index]" @input="invalidFields.selectedAmounts[index]=false"/>
                            <label for="amount">Amount</label>
                        </FloatLabel>
                        <Select v-model="selectedWeights[index]" :options="weights" optionLabel="label" optionValue="value" showClear placeholder="Select a weight" variant="filled" size="large" :invalid="invalidFields.selectedWeights[index]" @change="invalidFields.selectedWeights[index]=false"></Select>
                        <Button class="remove-btn" icon="pi pi-trash" severity="danger" @click="removeIngredient(index)"></Button>
                    </div>
                </div>
                <Button label="Add an ingredient" icon="pi pi-plus" @click="addIngredient"></Button>
            </div>

            <!-- Submit -->
            <div class="submit">
                <Button label="Create Recipe" type="submit" icon="pi pi-check-circle"></Button>
            </div>
        </form>
    </div>

</template>

<script lang="ts">
    import ingredientsData from '../data/ingredients.json';
    import axios from 'axios';
    export default {
            data () {
            return{
                username: '',
                title: '',
                short_description: '',
                steps: [""],
                hours: null,
                mins: null,
                servings: null,
                weights: [
                    { label: "Grams (g)", value: "g"},
                    { label: "Kilograms (kg)", value: "kg"},
                    { label: "Pounds (lb)", value: "lb"},
                    { label: "Ounces (oz)", value: "oz"},
                    { label: "Liters (l)", value: "l"},
                    { label: "Milliliters (ml)", value: "ml"},
                    { label: "Tablespoons (tbsp)", value: "tbsp"},
                    { label: "Teaspoons (tsp)", value: "tsp"},
                    { label: "Cups (cup)", value: "cup"},
                    { label: "Pints (pt)", value: "pt"},
                    { label: "Quarts (qt)", value: "qt"},
                    { label: "Gallons (gal)", value: "gal"},
                    { label: "Fluid Ounces (floz)", value: "floz"},
                    { label: "Quantity (qty)", value: "qty"}
                ],
                selectedAmounts: [null],
                selectedWeights: [""],
                ingredients: [""],
                invalidFields: {
                    title: false,
                    short_description: false,
                    steps: [] as boolean[],
                    hours: false,
                    minutes: false,
                    servings: false,
                    ingredients: [] as boolean[],
                    selectedAmounts: [] as boolean[],
                    selectedWeights: [] as boolean[]
                },
                ingredientsData: ingredientsData,
                ingredientsSuggestions: [] as string[]
             }
            },
            async mounted() {
                try {
                } catch (error) {
                    console.log(error)
                }      
            },
            methods: {
                async handleSubmit() {
                    if (!this.validateFields()) {
                        return;
                    }
                    const formattedSteps = this.steps.filter(step => step.trim()).join("<br>");
                    const formattedIngredients = this.ingredients.map((ingredient, index) => ({
                        ingredient_name: ingredient.trim(),
                        amount: this.selectedAmounts[index],
                        weight: this.selectedWeights[index]
                    }));

                    const payload = {
                        author_username: this.$route.params.username,
                        title: this.title,
                        short_description: this.short_description,
                        steps: formattedSteps,
                        time: {hours: this.hours, mins: this.mins},
                        servings: this.servings,
                        ingredients: formattedIngredients
                    }

                    try {
                        const response = await axios.post('http://localhost:5000/recipe', payload, {headers: { 'Content-Type': 'application/json'}});
                        if (response.status === 201) {
                            console.log(response.data.message);
                        }
                    } catch (error) {
                        console.log(error);
                    }
                },
                addStep() {
                    this.steps.push(""); // append placeholder empty string to steps array
                    this.invalidFields.steps.push(false);
                },
                removeStep(index: number) {
                    this.steps.splice(index, 1);
                    this.invalidFields.steps.splice(index, 1);
                },
                addIngredient() {
                    this.ingredients.push("") // append placeholder empty string to ingredients array
                    this.selectedAmounts.push(null);
                    this.selectedWeights.push("");
                    this.invalidFields.ingredients.push(false);
                    this.invalidFields.selectedAmounts.push(false);
                    this.invalidFields.selectedWeights.push(false);
                },
                removeIngredient(index: number) {
                    this.ingredients.splice(index, 1);
                    this.selectedAmounts.splice(index, 1);
                    this.selectedWeights.splice(index, 1);
                    this.invalidFields.ingredients.splice(index, 1);
                    this.invalidFields.selectedAmounts.splice(index, 1);
                    this.invalidFields.selectedWeights.splice(index, 1);
                },
                validateFields() {
                    let isValid = true;

                    if (!this.title.trim()) {
                        this.invalidFields.title = true;
                        isValid = false;
                    } else {
                        this.invalidFields.title = false;
                    }

                    if (!this.short_description.trim()) {
                        this.invalidFields.short_description = true;
                        isValid = false;
                    } else {
                        this.invalidFields.short_description = false;
                    }

                    this.steps.forEach((step, index) => {
                        if (!step.trim()) {
                            this.invalidFields.steps[index] = true;
                            isValid = false;
                        } else {
                            this.invalidFields.steps[index] = false;
                        }
                    });

                    if (this.hours === null || this.hours < 0) {
                        this.invalidFields.hours = true;
                        isValid = false;
                    } else {
                        this.invalidFields.hours = false;
                    }

                    if (this.mins === null || this.mins < 0) {
                        this.invalidFields.minutes = true;
                        isValid = false;
                    } else {
                        this.invalidFields.minutes = false;
                    }

                    if (!this.servings) {
                        this.invalidFields.servings = true;
                        isValid = false;
                    } else {
                        this.invalidFields.servings = false;
                    }

                    this.ingredients.forEach((ingredient, index) => {
                        console.log(ingredient);
                        if (!ingredient || !ingredient.trim()) {
                            this.invalidFields.ingredients[index] = true;
                            isValid = false;
                        } else {
                            this.invalidFields.ingredients[index] = false;
                        }
                    });

                    this.selectedAmounts.forEach((amount, index) => {
                        console.log(amount);
                        if (!amount || !(amount > 0)) {
                            this.invalidFields.selectedAmounts[index] = true;
                            isValid = false;
                        } else {
                            this.invalidFields.selectedAmounts[index] = false;
                        }
                    });

                    this.selectedWeights.forEach((weight, index) => {
                        console.log(weight);
                        if (!weight) {
                            this.invalidFields.selectedWeights[index] = true;
                            isValid = false;
                        } else {
                            this.invalidFields.selectedWeights[index] = false;
                        }
                    });

                    return isValid;
                },
                search(event: {query: string}) {
                    const query = event.query.toLowerCase();
                    const maxItems = 10;
                    this.ingredientsSuggestions = this.ingredientsData.filter(ingredient => ingredient.ingredient_name.toLowerCase().includes(query))
                                                        .slice(0, maxItems)
                                                        .map((ingredient) => ingredient.ingredient_name);
                }
            }
        }
</script>

<style scoped>
.title, .short-description {
    margin-bottom: 20px;
}

.step-row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.step-row p-input-text {
    flex-grow: 1;
    margin-right: 10px;
}

.remove-btn {
  border-radius: 5px;
  margin-left: 5px;
}

.step-row .remove-btn:hover {
  background-color: #d9363e;
}

.steps {
    margin-bottom: 20px;
}

.time {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}

.servings {
    display: flex;
    margin-bottom: 20px;
}

.ingredient-row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.ingredients {
    margin-bottom: 20px;
}

.submit {
    display: flex;
    gap: 10px;
    justify-content: flex-start;
}
</style>