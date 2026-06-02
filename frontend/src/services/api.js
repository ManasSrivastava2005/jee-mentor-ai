const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || 'Request failed');
  }
  return response.json();
}

export function solveQuestion(question) {
  return request('/solve', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
}

export function generateSimilar(question, subject, topic) {
  return request('/generate-similar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, subject, topic }),
  });
}

export function uploadQuestionImage(file) {
  const form = new FormData();
  form.append('file', file);
  return request('/ocr', { method: 'POST', body: form });
}

export function getAnalytics() {
  return request('/analytics');
}

export function getHistory() {
  return request('/history');
}
