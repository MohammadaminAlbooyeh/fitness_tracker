import { api } from './api';

export const fetchExercises = async ({ category, difficulty, equipment, muscle, searchQuery }) => {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (difficulty) params.append('difficulty', difficulty);
  if (equipment) params.append('equipment_id', equipment);
  if (muscle) params.append('muscle_id', muscle);
  if (searchQuery) params.append('query', searchQuery);

  const response = await api.get(`/exercises/?${params.toString()}`);
  return response.data;
};

export const fetchEquipment = async () => {
  const response = await api.get('/equipment/');
  return response.data;
};

export const fetchMuscles = async () => {
  const response = await api.get('/muscles/');
  return response.data;
};

export const createExercise = async (exerciseData) => {
  const response = await api.post('/exercises/', exerciseData);
  return response.data;
};

export const uploadExerciseVideo = async (exerciseId, videoFile) => {
  const formData = new FormData();
  formData.append('video', videoFile);
  
  const response = await api.post(`/exercises/${exerciseId}/video`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const logExerciseProgress = async (progressData) => {
  const response = await api.post(`/exercises/${progressData.exercise_id}/progress`, progressData);
  return response.data;
};

export const fetchExerciseProgress = async (exerciseId) => {
  const response = await api.get(`/progress/${exerciseId}`);
  return response.data;
};

export const fetchPersonalRecords = async () => {
  const response = await api.get('/progress/personal-records');
  return response.data;
};