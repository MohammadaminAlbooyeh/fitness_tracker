import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Badge,
  Avatar,
  useTheme,
} from '@mui/material';
import { Whatshot, EmojiEvents } from '@mui/icons-material';
import { useNotification } from '../context/NotificationContext';
import { gamificationApi } from '../api/gamification';

interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  earned_at: string;
}

interface StreakData {
  current_streak: number;
  longest_streak: number;
  last_workout_date: string;
}

export const Achievements: React.FC = () => {
  const theme = useTheme();
  const { showNotification } = useNotification();
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [achievementsData, streakData] = await Promise.all([
          gamificationApi.getAchievements(),
          gamificationApi.getStreak()
        ]);
        setAchievements(achievementsData);
        setStreak(streakData);
      } catch (error) {
        console.error('Error fetching achievements:', error);
        showNotification('Failed to load achievements', 'error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [showNotification]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Streak Card */}
      <Card sx={{ mb: 4, bgcolor: theme.palette.primary.main, color: 'white' }}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={2}>
            <Whatshot sx={{ fontSize: 40 }} />
            <Box>
              <Typography variant="h5">Current Streak</Typography>
              <Typography variant="h3">
                {streak?.current_streak || 0} days
              </Typography>
            </Box>
          </Box>
          <Typography variant="subtitle1" sx={{ mt: 1 }}>
            Longest Streak: {streak?.longest_streak || 0} days
          </Typography>
        </CardContent>
      </Card>

      {/* Achievements Grid */}
      <Typography variant="h5" gutterBottom>
        Achievements
      </Typography>
      <Grid container spacing={3}>
        {achievements.map((achievement) => (
          <Grid item xs={12} sm={6} md={4} key={achievement.id}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" gap={2}>
                  <Badge
                    overlap="circular"
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                    badgeContent={
                      <EmojiEvents
                        sx={{
                          color: theme.palette.secondary.main,
                          fontSize: '1.5rem',
                        }}
                      />
                    }
                  >
                    <Avatar
                      sx={{
                        bgcolor: theme.palette.primary.main,
                        width: 56,
                        height: 56,
                      }}
                    >
                      {achievement.icon}
                    </Avatar>
                  </Badge>
                  <Box>
                    <Typography variant="h6">{achievement.name}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      {achievement.description}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      Earned: {new Date(achievement.earned_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};