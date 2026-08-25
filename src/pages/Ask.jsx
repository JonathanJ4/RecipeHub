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
            <Header/>

            <main className="min-h-screen bg-gray-50 px-4 py-12" >
                <div classname="max-w-2xl mx-auto">
                    <h1 classname= "text-3xl font bold mb-6">
                        Ask Recipe Hub
                    </h1>

                    <form onSubmit={handle_submit}>
                        <input type="text" value ={query} onChange={event => setQuery(event.target.value)}/>
                    </form>
                </div>

            </main>

        </>

    )

}