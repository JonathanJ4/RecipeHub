export const API_URL = (
  import.meta.env.VITE_API_URL || 'http://localhost:8000'
).replace(/\/$/, '');

export async function fetchJson(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const body = await response.json();
      if (typeof body.detail === 'string') {
        message = body.detail;
      }
    } catch {
      // Keep the HTTP status message when the response is not JSON.
    }

    throw new Error(message);
  }

  return response.json();
}

export function getRecipeImageUrl(recipe) {
  if (recipe.image_url) {
    return recipe.image_url;
  }

  if (recipe.image_name) {
    return `${API_URL}/images/${encodeURIComponent(recipe.image_name)}.jpg`;
  }

  return null;
}
