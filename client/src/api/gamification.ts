import axios from 'axios';
import { getAuthHeaders } from './auth';

const BASE_URL = 'http://localhost:8000/api';

export const gamificationApi = {
  getAchievements: async () => {
    const response = await axios.get(`${BASE_URL}/achievements/`, {
      headers: await getAuthHeaders(),
    });
    return response.data;
  },

  getStreak: async () => {
    const response = await axios.get(`${BASE_URL}/streak/`, {
      headers: await getAuthHeaders(),
    });
    return response.data;
  },

  checkAchievements: async () => {
    const response = await axios.post(`${BASE_URL}/check-achievements/`, null, {
      headers: await getAuthHeaders(),
    });
    return response.data;
  },

  updateStreak: async () => {
    const response = await axios.post(`${BASE_URL}/update-streak/`, null, {
      headers: await getAuthHeaders(),
    });
    return response.data;
  },
};