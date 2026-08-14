import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Header from '../components/Header.jsx';
import { fetchJson } from '../lib/api.js';

export default function RecipeDetail() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchJson(`/recipes/${id}`)
      .then(data => setRecipe(data))
      .catch(err => setError(err.message));
  }, [id]);

  if (error) {
    return (
      <>
        <Header />
        <p className="text-center text-red-500 py-8">{error}</p>
      </>
    );
  }

  if (!recipe) {
    return (
      <>
        <Header />
        <p className="text-center py-8">Loading…</p>
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="max-w-3xl mx-auto px-6 py-10 space-y-8">
        {/* 1. Title */}
        <h1 className="text-4xl font-bold">{recipe.title}</h1>

        {/* 2. Image */}
        {recipe.image_url && (
          <img
            src={recipe.image_url}
            alt={recipe.title}
            className="w-full h-64 object-cover rounded-lg"
          />
        )}

        {/* 3. Ingredients */}
        {recipe.ingredients?.length > 0 && (
          <section>
            <h2 className="text-2xl font-semibold mb-2">Ingredients</h2>
            <ul className="list-disc list-inside space-y-1 text-gray-800">
              {recipe.ingredients.map((i, idx) => (
                <li key={idx}>{i}</li>
              ))}
            </ul>
          </section>
        )}

        {/* 4. Full instructions */}
        {recipe.instructions && (
          <section>
            <h2 className="text-2xl font-semibold mb-2">Instructions</h2>
            <p className="whitespace-pre-line text-gray-800">
              {recipe.instructions}
            </p>
          </section>
        )}
      </main>
    </>
  );
}
