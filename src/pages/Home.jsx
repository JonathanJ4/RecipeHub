import Header from '../components/Header.jsx';
import Hero from '../components/Hero.jsx';
import TrendingRecipes from '../components/TrendingRecipes.jsx';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <>
      <Header />
      <Hero />
      <TrendingRecipes />

      {/* Call to Action */}
      <section className="bg-white">
        <div className="max-w-4xl mx-auto text-center py-10 px-6">
          <h3 className="text-2xl font-semibold mb-4">Find your next meal</h3>
          <Link to="/search">
            <button className="bg-olive text-white px-6 py-3 rounded-lg hover:bg-olive-light transition">
              Start Searching
            </button>
          </Link>
        </div>
      </section>
    </>
  );
}
