import { axios } from './axios';
import { ApiResponse } from './types';

interface User {
  id: number;
  username: string;
  profile_picture: string;
  bio: string;
}

interface Post {
  id: number;
  content: string;
  user: User;
  created_at: string;
  likes_count: number;
  comments_count: number;
  workout_id?: number;
  achievement_id?: number;
}

interface Comment {
  id: number;
  content: string;
  user: User;
  created_at: string;
}

interface Challenge {
  id: number;
  name: string;
  description: string;
  creator: User;
  start_date: string;
  end_date: string;
  challenge_type: string;
  target_value: number;
  is_public: boolean;
  status: string;
  participants: User[];
  current_progress?: number;
}

export const socialApi = {
  // Friend system
  getFriends: async (): Promise<User[]> => {
    const response = await axios.get<ApiResponse<User[]>>('/social/friends');
    return response.data.data;
  },

  sendFriendRequest: async (userId: number): Promise<User> => {
    const response = await axios.post<ApiResponse<User>>(`/social/friends/request/${userId}`);
    return response.data.data;
  },

  // Posts and comments
  getFeed: async (skip = 0, limit = 20): Promise<Post[]> => {
    const response = await axios.get<ApiResponse<Post[]>>(`/social/feed?skip=${skip}&limit=${limit}`);
    return response.data.data;
  },

  createPost: async (data: { content: string; workout_id?: number; achievement_id?: number }): Promise<Post> => {
    const response = await axios.post<ApiResponse<Post>>('/social/posts', data);
    return response.data.data;
  },

  likePost: async (postId: number): Promise<void> => {
    await axios.post(`/social/posts/${postId}/like`);
  },

  getComments: async (postId: number): Promise<Comment[]> => {
    const response = await axios.get<ApiResponse<Comment[]>>(`/social/posts/${postId}/comments`);
    return response.data.data;
  },

  createComment: async (postId: number, data: { content: string }): Promise<Comment> => {
    const response = await axios.post<ApiResponse<Comment>>(`/social/posts/${postId}/comment`, data);
    return response.data.data;
  },

  // Challenges
  getChallenges: async (): Promise<Challenge[]> => {
    const response = await axios.get<ApiResponse<Challenge[]>>('/social/challenges');
    return response.data.data;
  },

  createChallenge: async (data: {
    name: string;
    description: string;
    start_date: Date;
    end_date: Date;
    challenge_type: string;
    target_value: number;
    is_public: boolean;
  }): Promise<Challenge> => {
    const response = await axios.post<ApiResponse<Challenge>>('/social/challenges', data);
    return response.data.data;
  },

  joinChallenge: async (challengeId: number): Promise<void> => {
    await axios.post(`/social/challenges/${challengeId}/join`);
  },

  logChallengeActivity: async (
    challengeId: number,
    data: { value: number; notes?: string }
  ): Promise<void> => {
    await axios.post(`/social/challenges/${challengeId}/activity`, data);
  },
};