import axios from '../utils/axios';

// Progress Photos
export const uploadProgressPhoto = async (formData) => {
  const response = await axios.post('/api/progress/photos', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const fetchProgressPhotos = async () => {
  const response = await axios.get('/api/progress/photos');
  return response.data;
};