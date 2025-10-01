import { api } from './api';

export const fetchWorkoutTemplates = async ({ category, difficulty, includePublic }) => {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (difficulty) params.append('difficulty', difficulty);
  params.append('include_public', String(includePublic));

  const response = await api.get(`/workouts/templates?${params.toString()}`);
  return response.data;
};

export const fetchScheduledWorkouts = async () => {
  const response = await api.get('/workouts/scheduled');
  return response.data;
};

export const scheduleWorkout = async (workoutData) => {
  const response = await api.post('/workouts/schedule', workoutData);
  return response.data;
};

export const updateWorkoutStatus = async ({ workoutId, status }) => {
  const response = await api.patch(`/workouts/scheduled/${workoutId}/${status}`);
  return response.data;
};

export const createWorkoutTemplate = async (templateData) => {
  const response = await api.post('/workouts/templates', templateData);
  return response.data;
};