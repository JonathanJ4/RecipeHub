import { useState } from "react";
import Header from '../components/Header.jsx';
import { fetchJson } from "../lib/api.js";


export default function Ask(){
    const [query,setQuery] = useState('');
    const [answer,setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    async function handle_submit(){

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

}