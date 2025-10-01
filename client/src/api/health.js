import { axiosInstance } from './axiosInstance';

// Sleep tracking endpoints
export const getSleepData = async (userId, startDate, endDate) => {
  const response = await axiosInstance.get('/health/sleep', {
    params: { userId, startDate, endDate }
  });
  return response.data;
};

export const addSleepData = async (sleepData) => {
  const response = await axiosInstance.post('/health/sleep', sleepData);
  return response.data;
};

export const updateSleepData = async (sleepId, sleepData) => {
  const response = await axiosInstance.put(`/health/sleep/${sleepId}`, sleepData);
  return response.data;
};

export const getSleepStatistics = async (userId, days) => {
  const response = await axiosInstance.get(`/health/sleep/statistics/${userId}`, {
    params: { days }
  });
  return response.data;
};

// Recovery monitoring endpoints
export const getRecoveryMetrics = async () => {
  const response = await axiosInstance.get('/health/recovery/metrics');
  return response.data;
};

export const getRecoveryStatistics = async (days = 30) => {
  const response = await axiosInstance.get('/health/recovery/statistics', {
    params: { days }
  });
  return response.data;
};

export const getRecoveryRecommendations = async () => {
  const response = await axiosInstance.get('/health/recovery/recommendations');
  return response.data;
};

export const updateRecoveryData = async (data) => {
  const response = await axiosInstance.post('/health/recovery/data', data);
  return response.data;
};

// Health tracking endpoints
export const getHealthMetrics = async (userId, metricType) => {
  const response = await axiosInstance.get('/health/metrics', {
    params: { userId, metricType }
  });
  return response.data;
};

export const addHealthMetric = async (metricData) => {
  const response = await axiosInstance.post('/health/metrics', metricData);
  return response.data;
};

export const getHealthSummary = async (userId, timeframe) => {
  const response = await axiosInstance.get(`/health/summary/${userId}`, {
    params: { timeframe }
  });
  return response.data;
};

// Device integration endpoints
export const syncHealthData = async (deviceType, data) => {
  const response = await axiosInstance.post('/health/sync', {
    deviceType,
    data
  });
  return response.data;
};

export const getConnectedDevices = async () => {
  const response = await axiosInstance.get('/health/devices');
  return response.data;
};

export const connectDevice = async (deviceInfo) => {
  const response = await axiosInstance.post('/health/devices/connect', deviceInfo);
  return response.data;
};

export const disconnectDevice = async (deviceId) => {
  const response = await axiosInstance.delete(`/health/devices/${deviceId}`);
  return response.data;
};

// Health insights and trends
export const getHealthTrends = async (userId, metrics, timeframe) => {
  const response = await axiosInstance.get('/health/trends', {
    params: { userId, metrics, timeframe }
  });
  return response.data;
};

export const getHealthInsights = async (userId) => {
  const response = await axiosInstance.get(`/health/insights/${userId}`);
  return response.data;
};