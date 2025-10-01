import { axios } from './axios';
import { ApiResponse } from './types';

interface BodyMeasurement {
  id: number;
  date: string;
  weight?: number;
  height?: number;
  body_fat?: number;
  muscle_mass?: number;
  chest?: number;
  waist?: number;
  hips?: number;
  biceps_left?: number;
  biceps_right?: number;
  thigh_left?: number;
  thigh_right?: number;
}

interface ProgressStats {
  weight_change: number;
  body_fat_change: number;
  muscle_mass_change: number;
}

interface ProgressPhoto {
  id: number;
  date: string;
  photo_url: string;
  photo_type: 'front' | 'back' | 'side';
}

interface Goal {
  id: number;
  metric: string;
  target: number;
  deadline: string;
  current_value: number;
  progress: number;
}

export const progressApi = {
  // Body Measurements
  getMeasurements: async (): Promise<BodyMeasurement[]> => {
    const response = await axios.get<ApiResponse<BodyMeasurement[]>>('/progress/measurements');
    return response.data.data;
  },

  // Goals
  getGoals: async (): Promise<Goal[]> => {
    const response = await axios.get<ApiResponse<Goal[]>>('/progress/goals');
    return response.data.data;
  },

  createGoal: async (data: Omit<Goal, 'id' | 'current_value' | 'progress'>): Promise<Goal> => {
    const response = await axios.post<ApiResponse<Goal>>('/progress/goals', data);
    return response.data.data;
  },

  updateGoal: async (id: number, data: Partial<Goal>): Promise<Goal> => {
    const response = await axios.put<ApiResponse<Goal>>(`/progress/goals/${id}`, data);
    return response.data.data;
  },

  deleteGoal: async (id: number): Promise<void> => {
    await axios.delete(`/progress/goals/${id}`);
  },

  createMeasurement: async (data: Partial<BodyMeasurement>): Promise<BodyMeasurement> => {
    const response = await axios.post<ApiResponse<BodyMeasurement>>('/progress/measurements', data);
    return response.data.data;
  },

  getProgressStats: async (): Promise<ProgressStats> => {
    const response = await axios.get<ApiResponse<ProgressStats>>('/progress/stats');
    return response.data.data;
  },

  // Progress Photos
  getProgressPhotos: async (): Promise<ProgressPhoto[]> => {
    const response = await axios.get<ApiResponse<ProgressPhoto[]>>('/progress/photos');
    return response.data.data;
  },

  uploadProgressPhoto: async (formData: FormData): Promise<ProgressPhoto> => {
    const response = await axios.post<ApiResponse<ProgressPhoto>>('/progress/photos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data.data;
  },

  deleteProgressPhoto: async (photoId: number): Promise<void> => {
    await axios.delete(`/progress/photos/${photoId}`);
  },
};