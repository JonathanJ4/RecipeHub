import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Search from './pages/Search.jsx';
import RecipeDetail from './pages/RecipeDetail.jsx';
import Ask from './pages/Ask.jsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/search" element={<Search />} />
      <Route path="/recipe/:id" element={<RecipeDetail />} />
      <Route path="/ask" element={<Ask />} />
    </Routes>
  );
}

export default App;