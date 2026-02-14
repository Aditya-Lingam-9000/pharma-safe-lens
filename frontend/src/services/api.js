import axios from 'axios';

// ⚠️ UPDATE THIS with your ngrok URL from Kaggle notebook
const API_BASE_URL = "https://unhurting-nonmediative-deegan.ngrok-free.dev";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 180000,
  headers: {
    'Accept': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  }
});

/**
 * Upload image via the STREAMING endpoint.
 * Calls onInit when drugs/interactions are detected (fast)
 * Calls onInteraction each time one AI explanation finishes
 * Calls onDone when all interactions are complete
 */
export const uploadImageStream = async (imageFile, { onInit, onInteraction, onDone, onError }) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(`${API_BASE_URL}/api/v1/analyze-image-stream`, {
    method: 'POST',
    body: formData,
    headers: {
      'ngrok-skip-browser-warning': 'true'
    }
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Server error ${response.status}: ${text}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // SSE events are delimited by double newline
    const parts = buffer.split('\n\n');
    buffer = parts.pop(); // keep incomplete chunk in buffer

    for (const part of parts) {
      if (!part.trim()) continue;

      let eventType = 'message';
      let eventData = '';

      for (const line of part.split('\n')) {
        if (line.startsWith('event: ')) {
          eventType = line.slice(7).trim();
        } else if (line.startsWith('data: ')) {
          eventData = line.slice(6);
        }
      }

      if (!eventData) continue;

      try {
        const parsed = JSON.parse(eventData);

        switch (eventType) {
          case 'init':
            onInit?.(parsed);
            break;
          case 'interaction':
            onInteraction?.(parsed);
            break;
          case 'done':
            onDone?.();
            break;
          case 'error':
            onError?.(parsed.detail || 'Unknown server error');
            break;
          default:
            break;
        }
      } catch (e) {
        console.warn('SSE parse error:', e, eventData);
      }
    }
  }
};

/**
 * Original non-streaming upload (kept as fallback)
 */
export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  try {
    const response = await api.post('/api/v1/analyze-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'ngrok-skip-browser-warning': 'true'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Full error object:', error);
    console.error('Error response:', error.response);
    
    if (error.response) {
      throw new Error(error.response.data.detail || `Server error: ${error.response.status}`);
    } else if (error.request) {
      throw new Error('No response from server. Check if backend is running.');
    } else {
      throw new Error('Failed to send request: ' + error.message);
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend is not reachable');
  }
};

export const getApiUrl = () => API_BASE_URL;

export const setApiUrl = (newUrl) => {
  api.defaults.baseURL = newUrl;
  console.log('API URL updated to:', newUrl);
};
