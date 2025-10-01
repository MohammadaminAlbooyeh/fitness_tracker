import axios from '../utils/axios';

// Social Feed
export const fetchSocialFeed = async () => {
  const response = await axios.get('/api/social/feed');
  return response.data;
};

export const likeWorkout = async (workoutId) => {
  const response = await axios.post(`/api/social/workouts/${workoutId}/like`);
  return response.data;
};

export const commentOnWorkout = async ({ workoutId, content }) => {
  const response = await axios.post(`/api/social/workouts/${workoutId}/comment`, { content });
  return response.data;
};

export const shareWorkout = async (workoutId) => {
  const response = await axios.post(`/api/social/workouts/${workoutId}/share`);
  return response.data;
};

// Challenges
export const fetchChallenges = async () => {
  const response = await axios.get('/api/social/challenges');
  return response.data;
};

export const createChallenge = async (challengeData) => {
  const response = await axios.post('/api/social/challenges', challengeData);
  return response.data;
};

export const joinChallenge = async (challengeId) => {
  const response = await axios.post(`/api/social/challenges/${challengeId}/join`);
  return response.data;
};

export const updateChallengeProgress = async ({ challengeId, progress }) => {
  const response = await axios.put(`/api/social/challenges/${challengeId}/progress`, { progress });
  return response.data;
};

// Following
export const followUser = async (userId) => {
  const response = await axios.post(`/api/social/users/${userId}/follow`);
  return response.data;
};

export const unfollowUser = async (userId) => {
  const response = await axios.delete(`/api/social/users/${userId}/follow`);
  return response.data;
};

export const getFollowers = async (userId) => {
  const response = await axios.get(`/api/social/users/${userId}/followers`);
  return response.data;
};

export const getFollowing = async (userId) => {
  const response = await axios.get(`/api/social/users/${userId}/following`);
  return response.data;
};