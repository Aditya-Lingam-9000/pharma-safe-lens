import axios from 'axios';

// ⚠️ UPDATE THIS with your ngrok URL from Kaggle notebook
// Example: 'https://a1b2-c3d4-e5f6.ngrok.io'
const API_BASE_URL = "https://unhurting-nonmediative-deegan.ngrok-free.dev"; // Default for local testing

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds for MedGemma inference + OCR
  headers: {
    'Accept': 'application/json',
    'ngrok-skip-browser-warning': 'true' // Required for ngrok free tier
  }
});

/**
 * Upload prescription image and get drug interaction analysis
 * @param {File} imageFile - The prescription image file
 * @returns {Promise<Object>} Analysis results with interactions and AI explanation
 */
export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  try {
    const response = await api.post('/api/v1/analyze-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'ngrok-skip-browser-warning': 'true' // Add header to POST request too
      }
    });
    return response.data;
  } catch (error) {
    // Log the full error for debugging
    console.error('Full error object:', error);
    console.error('Error response:', error.response);
    
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.detail || `Server error: ${error.response.status}`);
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Check if backend is running.');
    } else {
      // Request setup error
      throw new Error('Failed to send request: ' + error.message);
    }
  }
};

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend is not reachable');
  }
};

// Export API base URL for display purposes
export const getApiUrl = () => API_BASE_URL;

// Function to update API URL dynamically (useful when ngrok URL changes)
export const setApiUrl = (newUrl) => {
  api.defaults.baseURL = newUrl;
  console.log('🔄 API URL updated to:', newUrl);
};
