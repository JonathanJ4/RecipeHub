import mongoose from 'mongoose';

const recipeSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  instructions: { type: String, default: '' },
  image: { type: String, default: '' },
  mealType: { type: String, default: '' },
  popularity: { type: Number, default: 0 },
  ingredients: {
    type: [String],
    default: [],
  },
});

export default mongoose.model('Recipe', recipeSchema);
