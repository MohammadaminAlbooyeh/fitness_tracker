import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  CircularProgress,
  Avatar,
  AvatarGroup,
  Chip,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import {
  EmojiEvents as TrophyIcon,
  Group as GroupIcon,
  TimerOutlined as TimerIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useNotification } from '../context/NotificationContext';
import { socialApi } from '../api/social';

interface Challenge {
  id: number;
  name: string;
  description: string;
  creator: {
    id: number;
    username: string;
    profile_picture: string;
  };
  start_date: string;
  end_date: string;
  challenge_type: string;
  target_value: number;
  is_public: boolean;
  status: string;
  participants: Array<{
    id: number;
    username: string;
    profile_picture: string;
  }>;
  current_progress?: number;
}

export const Challenges: React.FC = () => {
  const { showNotification } = useNotification();
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    start_date: new Date(),
    end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1 week from now
    challenge_type: '',
    target_value: '',
    is_public: true,
  });

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      const data = await socialApi.getChallenges();
      setChallenges(data);
    } catch (error) {
      console.error('Error fetching challenges:', error);
      showNotification('Failed to load challenges', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChallenge = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await socialApi.createChallenge({
        ...formData,
        target_value: Number(formData.target_value),
      });
      showNotification('Challenge created successfully', 'success');
      setShowCreateDialog(false);
      fetchChallenges();
    } catch (error) {
      console.error('Error creating challenge:', error);
      showNotification('Failed to create challenge', 'error');
    }
  };

  const handleJoinChallenge = async (challengeId: number) => {
    try {
      await socialApi.joinChallenge(challengeId);
      showNotification('Successfully joined the challenge', 'success');
      fetchChallenges();
    } catch (error) {
      console.error('Error joining challenge:', error);
      showNotification('Failed to join challenge', 'error');
    }
  };

  const calculateProgress = (challenge: Challenge) => {
    if (!challenge.current_progress) return 0;
    return Math.min((challenge.current_progress / challenge.target_value) * 100, 100);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'success';
      case 'completed':
        return 'primary';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const challengeTypes = [
    'Workout Count',
    'Total Steps',
    'Weight Loss',
    'Running Distance',
    'Workout Minutes',
  ];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4">
          Fitness Challenges
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setShowCreateDialog(true)}
        >
          Create Challenge
        </Button>
      </Box>

      <Grid container spacing={3}>
        {challenges.map((challenge) => (
          <Grid item xs={12} md={6} key={challenge.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6">
                    {challenge.name}
                  </Typography>
                  <Chip
                    label={challenge.status}
                    color={getStatusColor(challenge.status)}
                    size="small"
                  />
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {challenge.description}
                </Typography>

                <Box display="flex" alignItems="center" mb={2}>
                  <TimerIcon sx={{ mr: 1 }} />
                  <Typography variant="body2">
                    {new Date(challenge.start_date).toLocaleDateString()} - {' '}
                    {new Date(challenge.end_date).toLocaleDateString()}
                  </Typography>
                </Box>

                <Box display="flex" alignItems="center" mb={2}>
                  <TrophyIcon sx={{ mr: 1 }} />
                  <Typography variant="body2">
                    Target: {challenge.target_value} {challenge.challenge_type}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Box display="flex" justifyContent="space-between" mb={1}>
                    <Typography variant="body2">Progress</Typography>
                    <Typography variant="body2">
                      {Math.round(calculateProgress(challenge))}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={calculateProgress(challenge)}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                <Box display="flex" alignItems="center">
                  <GroupIcon sx={{ mr: 1 }} />
                  <AvatarGroup max={4}>
                    {challenge.participants.map((participant) => (
                      <Avatar
                        key={participant.id}
                        src={participant.profile_picture}
                        alt={participant.username}
                      >
                        {participant.username[0]}
                      </Avatar>
                    ))}
                  </AvatarGroup>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={() => handleJoinChallenge(challenge.id)}
                  disabled={challenge.status !== 'active'}
                >
                  Join Challenge
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog
        open={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={handleCreateChallenge}>
          <DialogTitle>Create New Challenge</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Challenge Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              margin="normal"
              multiline
              rows={3}
            />
            <TextField
              fullWidth
              select
              label="Challenge Type"
              value={formData.challenge_type}
              onChange={(e) => setFormData({ ...formData, challenge_type: e.target.value })}
              margin="normal"
              required
            >
              {challengeTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              fullWidth
              label="Target Value"
              type="number"
              value={formData.target_value}
              onChange={(e) => setFormData({ ...formData, target_value: e.target.value })}
              margin="normal"
              required
            />
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <Box sx={{ mt: 2 }}>
                <DatePicker
                  label="Start Date"
                  value={formData.start_date}
                  onChange={(date) => date && setFormData({ ...formData, start_date: date })}
                />
              </Box>
              <Box sx={{ mt: 2 }}>
                <DatePicker
                  label="End Date"
                  value={formData.end_date}
                  onChange={(date) => date && setFormData({ ...formData, end_date: date })}
                  minDate={formData.start_date}
                />
              </Box>
            </LocalizationProvider>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowCreateDialog(false)}>Cancel</Button>
            <Button type="submit" variant="contained" color="primary">
              Create Challenge
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};