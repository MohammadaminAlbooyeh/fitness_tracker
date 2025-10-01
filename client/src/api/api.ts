import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async (email: string, password: string) => {
  const response = await api.post('/token', new URLSearchParams({
    'username': email,
    'password': password,
  }));
  return response.data;
};

export const register = async (userData: {
  email: string;
  password: string;
  username: string;
  full_name?: string;
}) => {
  const response = await api.post('/register', userData);
  return response.data;
};

export const getWorkouts = async () => {
  const response = await api.get('/workouts');
  return response.data;
};

export const createWorkout = async (workoutData: {
  name: string;
  description?: string;
  exercises: Array<{
    exercise_id: number;
    sets?: number;
    reps?: number;
    weight?: number;
    duration?: number;
  }>;
}) => {
  const response = await api.post('/workouts', workoutData);
  return response.data;
};

export const getExercises = async () => {
  const response = await api.get('/exercises');
  return response.data;
};

export const createExercise = async (exerciseData: {
  name: string;
  description?: string;
  category: string;
  target_muscle: string;
}) => {
  const response = await api.post('/exercises', exerciseData);
  return response.data;
};