import { useEffect, useState } from 'react';
import RecipeCard from './RecipeCard.jsx';
import { fetchJson } from '../lib/api.js';

export default function FeaturedRecipes() {
  const [recipes, setRecipes] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJson('/recipes?limit=6')
      .then(data => setRecipes(data))
      .catch(err => setError(err.message));
  }, []);

  if (error) {
    return (
      <p className="text-center text-red-500 py-8">
        Error loading recipes: {error}
      </p>
    );
  }
  if (!recipes) {
    return <p className="text-center py-8">Loading recipes…</p>;
  }

  return (
    <section className="max-w-4xl mx-auto px-6 py-10">
      <h3 className="text-2xl font-semibold mb-6">Featured Recipes</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </section>
  );
}
