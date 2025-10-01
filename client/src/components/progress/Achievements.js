import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  LinearProgress,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondary,
  Tooltip
} from '@mui/material';
import {
  EmojiEvents as TrophyIcon,
  Star as StarIcon,
  Lock as LockIcon
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import { fetchUserAchievements } from '../../api/progress';

const AchievementCard = ({ achievement }) => {
  const progress = achievement.progress || 0;
  const isLocked = !achievement.completed;

  return (
    <Card 
      sx={{ 
        height: '100%',
        opacity: isLocked ? 0.7 : 1,
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'scale(1.02)'
        }
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <IconButton
            sx={{
              backgroundColor: isLocked ? 'grey.300' : 'primary.light',
              mr: 2
            }}
          >
            {isLocked ? <LockIcon /> : <StarIcon />}
          </IconButton>
          <Typography variant="h6" component="div">
            {achievement.title}
          </Typography>
        </Box>

        <Typography variant="body2" color="text.secondary" mb={2}>
          {achievement.description}
        </Typography>

        {!achievement.completed && achievement.progress !== undefined && (
          <Box>
            <Box display="flex" justifyContent="space-between" mb={0.5}>
              <Typography variant="caption" color="text.secondary">
                Progress
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {progress}%
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={progress} 
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        )}

        {achievement.completed && (
          <Typography 
            variant="caption" 
            color="success.main"
            display="flex"
            alignItems="center"
          >
            <TrophyIcon sx={{ mr: 0.5, fontSize: 16 }} />
            Earned on {format(new Date(achievement.date_completed), 'MMM d, yyyy')}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

const Achievements = () => {
  const { data: achievements, isLoading } = useQuery(
    'achievements',
    fetchUserAchievements
  );

  const categories = {
    workout: 'Workout Achievements',
    strength: 'Strength Milestones',
    consistency: 'Consistency Rewards',
    special: 'Special Achievements'
  };

  const groupedAchievements = achievements?.reduce((acc, achievement) => {
    const category = achievement.type.split('_')[0];
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(achievement);
    return acc;
  }, {});

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Achievements
        </Typography>

        {isLoading ? (
          <Typography>Loading achievements...</Typography>
        ) : (
          Object.entries(groupedAchievements || {}).map(([category, items]) => (
            <Box key={category} sx={{ mb: 4 }}>
              <Typography variant="h5" sx={{ mb: 2 }}>
                {categories[category] || category}
              </Typography>
              <Grid container spacing={3}>
                {items.map((achievement) => (
                  <Grid item xs={12} sm={6} md={4} key={achievement.id}>
                    <AchievementCard achievement={achievement} />
                  </Grid>
                ))}
              </Grid>
            </Box>
          ))
        )}
      </Box>
    </Container>
  );
};

export default Achievements;