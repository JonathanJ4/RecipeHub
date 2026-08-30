import { useEffect, useRef, useState } from "react";
import Header from '../components/Header.jsx';
import { fetchJson } from "../lib/api.js";


export default function Ask(){
    const [query,setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [conversationId, setConversationId] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, loading]);

    async function handleSubmit(event){
        event.preventDefault();

        const question = query.trim();

        if (!question || loading) {
          return;
        }
        
        setLoading(true);
        setError('');
        setQuery('');
        setMessages(previousMessages => [
          ...previousMessages,
          { role: 'user', content: question },
        ]);

        try{
            const responseData = await fetchJson('/ask', {
                method:'POST',
                headers:{'Content-Type':'application/json',},
                body: JSON.stringify({
                    query: question,
                    conversation_id: conversationId,
                 }),
            })

            setMessages(previousMessages => [
              ...previousMessages,
              { role: 'assistant', content: responseData.answer },
            ]);
            setConversationId(responseData.conversation_id);
    }   catch (requestError) {
        setError(requestError.message);
    }   finally {
        setLoading(false);
    }
    }


    return (
    <div className="h-screen bg-gray-50 flex flex-col overflow-hidden">
      <Header />

      <main className="flex-1 min-h-0 flex flex-col">
        <div className="border-b bg-white px-4 py-4">
          <h1 className="max-w-3xl mx-auto text-2xl font-bold text-gray-900">
            Ask Recipe Hub
          </h1>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-3xl mx-auto flex flex-col gap-4">
            {messages.length === 0 && (
              <div className="my-12 text-center text-gray-500">
                <p className="text-lg font-medium text-gray-700">
                  What would you like to cook?
                </p>
                <p className="mt-2">
                  Ask for recipe ideas, ingredients, or cooking instructions.
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`max-w-[85%] rounded-2xl px-4 py-3 whitespace-pre-wrap ${
                  message.role === 'user'
                    ? 'self-end bg-olive text-white rounded-br-sm'
                    : 'self-start bg-white text-gray-800 shadow-sm rounded-bl-sm'
                }`}
              >
                {message.content}
              </div>
            ))}

            {loading && (
              <div className="self-start rounded-2xl rounded-bl-sm bg-white px-4 py-3 text-gray-500 shadow-sm">
                Thinking...
              </div>
            )}

            {error && (
              <p className="self-center text-sm text-red-600">
                {error}
              </p>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        <div className="border-t bg-white px-4 py-4">
          <form
            onSubmit={handleSubmit}
            className="max-w-3xl mx-auto flex items-end gap-3"
          >
            <textarea
              value={query}
              onChange={event => setQuery(event.target.value)}
              placeholder="Ask about recipes..."
              rows="2"
              className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 focus:border-olive focus:outline-none"
            />

            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="rounded-xl bg-olive px-6 py-3 text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              Send
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
