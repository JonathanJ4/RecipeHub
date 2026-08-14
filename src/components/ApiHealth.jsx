import { useEffect, useState } from 'react';
import { fetchJson } from '../lib/api.js';

export default function ApiHealth() {
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    const controller = new AbortController();

    async function checkHealth() {
      try {
        const data = await fetchJson('/health', {
          signal: controller.signal,
        });
        setStatus(data.status === 'ok' ? 'online' : 'offline');
      } catch (error) {
        if (error.name !== 'AbortError') {
          setStatus('offline');
        }
      }
    }

    checkHealth();

    return () => controller.abort();
  }, []);

  const isOnline = status === 'online';

  return (
    <span
      className="inline-flex items-center gap-2 text-sm text-gray-600"
      title={`FastAPI backend: ${status}`}
      aria-live="polite"
    >
      <span
        className={`h-2 w-2 rounded-full ${
          isOnline ? 'bg-green-500' : status === 'checking' ? 'bg-amber-400' : 'bg-red-500'
        }`}
        aria-hidden="true"
      />
      API {status}
    </span>
  );
}
