const BASE = import.meta.env.VITE_API_URL || '/api';
export async function api(path, params={}) {
  const query = new URLSearchParams(Object.entries(params).filter(([,v]) => v !== undefined && v !== null && v !== '')).toString();
  const response = await fetch(`${BASE}${path}${query ? `?${query}` : ''}`);
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${path}`);
  return await response.json();
}
