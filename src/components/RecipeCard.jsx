import { Link } from 'react-router-dom';

export default function RecipeCard({ recipe }) {
  const preview = (recipe.ingredients || []).slice(0, 3);

  return (
    <Link
      to={`/recipe/${recipe.id}`}
      className="block bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden"
    >
      {recipe.image_url ? (
        <img
          className="w-full h-40 object-cover"
          src={recipe.image_url}
          alt={recipe.title}
        />
      ) : (
        <div className="w-full h-40 bg-olive-light flex items-center justify-center text-olive">
          <span className="text-sm font-medium">Recipe Hub</span>
        </div>
      )}

      <div className="p-4">
        <h4 className="font-semibold text-lg mb-1">{recipe.title}</h4>
        {preview.length > 0 && (
          <p className="text-gray-500 text-xs italic">
            {preview.join(', ')}
            {recipe.ingredients.length > 3 ? '…' : ''}
          </p>
        )}
      </div>
    </Link>
  );
}
