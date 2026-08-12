import { useEffect, useState } from 'react';
import RecipeCard from './RecipeCard.jsx';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export default function TrendingRecipes() {
  const [recipes, setRecipes] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${API_URL}/recipes/trending`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to load trending');
        return res.json();
      })
      .then(data => setRecipes(data))
      .catch(err => setError(err.message));
  }, []);

  if (error) {
    return (
      <p className="text-center text-red-500 py-8">
        Error loading trending recipes: {error}
      </p>
    );
  }
  if (!recipes) {
    return <p className="text-center py-8">Loading trending recipes…</p>;
  }

  return (
    <section className="max-w-4xl mx-auto px-6 py-10">
      <h3 className="text-2xl font-semibold mb-6">Trending Recipes</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {recipes.map(r => (
          <RecipeCard key={r._id} recipe={r} />
        ))}
      </div>
    </section>
  );
}
