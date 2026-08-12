import { useEffect, useState } from 'react';

const FASTAPI_URL = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000';

export default function ApiHealth() {
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    const controller = new AbortController();

    async function checkHealth() {
      try {
        const response = await fetch(`${FASTAPI_URL}/health`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Health check failed with status ${response.status}`);
        }

        const data = await response.json();
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
