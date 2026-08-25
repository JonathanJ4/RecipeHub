import { useState } from "react";
import Header from '../components/Header.jsx';
import { fetchJson } from "../lib/api.js";


export default function Ask(){
    const [query,setQuery] = useState('');
    const [answer,setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    async function handle_submit(event){

        event.preventDefault();
        
        setLoading(true);
        setError(''); 
        setAnswer(''); // Doing this to remove the old answer 


        try{
            const responseData = await fetchJson('/ask', {
                method:'Post',
                headers:{'Content-Type':'application/json',},
                body: JSON.stringify({
                    query: query.trim(),
                 }),
            })
        
        setAnswer(responseData.answer);
    }   catch (requestError) {
        setError(requestError.message);
    }   finally {
        setLoading(false);
    }
    }


    return (
    <>
      <Header />

      <main className="min-h-screen bg-gray-50 px-4 py-12">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold mb-6">
            Ask Recipe Hub
          </h1>

          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={query}
              onChange={event => setQuery(event.target.value)}
              placeholder="What can I make with chicken and broccoli?"
              className="w-full border rounded-lg px-4 py-3"
            />

            <button
              type="submit"
              disabled={loading}
              className="mt-4 bg-olive text-white px-6 py-3 rounded-lg"
            >
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </form>

          {error && (
            <p className="mt-6 text-red-600">
              {error}
            </p>
          )}

          {answer && (
            <section className="mt-8 bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-3">
                Answer
              </h2>

              <p className="whitespace-pre-wrap">
                {answer}
              </p>
            </section>
          )}
        </div>
      </main>
    </>
  );
}