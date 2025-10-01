import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  Button,
  Box,
  LinearProgress,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  IconButton,
  Chip
} from '@mui/material';
import {
  Add as AddIcon,
  EmojiEvents as TrophyIcon,
  Group as GroupIcon,
  Schedule as ScheduleIcon,
  Flag as FlagIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import { 
  fetchChallenges,
  createChallenge,
  joinChallenge,
  updateChallengeProgress
} from '../../api/social';

const CHALLENGE_TYPES = [
  { value: 'workout', label: 'Workout Challenge' },
  { value: 'steps', label: 'Steps Challenge' },
  { value: 'weight_loss', label: 'Weight Loss Challenge' },
  { value: 'strength', label: 'Strength Challenge' },
  { value: 'cardio', label: 'Cardio Challenge' }
];

const ChallengeCard = ({ challenge }) => {
  const queryClient = useQueryClient();
  const joinMutation = useMutation(joinChallenge, {
    onSuccess: () => {
      queryClient.invalidateQueries('challenges');
    }
  });

  const updateProgressMutation = useMutation(updateChallengeProgress, {
    onSuccess: () => {
      queryClient.invalidateQueries('challenges');
    }
  });

  const progress = (challenge.current_value / challenge.target_value) * 100;
  const isJoined = challenge.is_participant;
  const isCompleted = challenge.completed;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">
            {challenge.title}
          </Typography>
          <Chip
            icon={<TrophyIcon />}
            label={CHALLENGE_TYPES.find(t => t.value === challenge.challenge_type)?.label}
            color="primary"
            variant="outlined"
          />
        </Box>

        <Typography variant="body2" paragraph>
          {challenge.description}
        </Typography>

        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <GroupIcon sx={{ mr: 1, color: 'text.secondary' }} />
              <Typography variant="body2" color="text.secondary">
                {challenge.participants_count} participants
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <ScheduleIcon sx={{ mr: 1, color: 'text.secondary' }} />
              <Typography variant="body2" color="text.secondary">
                {format(new Date(challenge.end_date), 'MMM d, yyyy')}
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {isJoined && (
          <Box sx={{ mb: 2 }}>
            <Box display="flex" justifyContent="space-between" mb={0.5}>
              <Typography variant="body2" color="text.secondary">
                Progress
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {challenge.current_value} / {challenge.target_value}
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={progress}
              sx={{
                height: 8,
                borderRadius: 4,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: isCompleted ? 'success.main' : 'primary.main',
                }
              }}
            />
          </Box>
        )}

        {!isJoined ? (
          <Button
            fullWidth
            variant="contained"
            onClick={() => joinMutation.mutate(challenge.id)}
          >
            Join Challenge
          </Button>
        ) : (
          <Button
            fullWidth
            variant="outlined"
            onClick={() => updateProgressMutation.mutate({
              challengeId: challenge.id,
              progress: challenge.current_value + 1
            })}
            disabled={isCompleted}
          >
            {isCompleted ? 'Completed!' : 'Update Progress'}
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

const CreateChallengeDialog = ({ open, onClose }) => {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    challenge_type: 'workout',
    target_value: '',
    end_date: '',
    private: false
  });

  const createMutation = useMutation(createChallenge, {
    onSuccess: () => {
      queryClient.invalidateQueries('challenges');
      onClose();
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create New Challenge</DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Challenge Title"
              value={formData.title}
              onChange={handleChange('title')}
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Description"
              value={formData.description}
              onChange={handleChange('description')}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              select
              fullWidth
              label="Challenge Type"
              value={formData.challenge_type}
              onChange={handleChange('challenge_type')}
            >
              {CHALLENGE_TYPES.map(type => (
                <MenuItem key={type.value} value={type.value}>
                  {type.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Target Value"
              value={formData.target_value}
              onChange={handleChange('target_value')}
              helperText="Set the goal (reps, steps, etc.)"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="date"
              label="End Date"
              value={formData.end_date}
              onChange={handleChange('end_date')}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          color="primary"
          disabled={createMutation.isLoading}
        >
          Create Challenge
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const Challenges = () => {
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const { data: challenges, isLoading } = useQuery('challenges', fetchChallenges);

  const activeChallenges = challenges?.filter(c => !c.completed) || [];
  const completedChallenges = challenges?.filter(c => c.completed) || [];

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
          <Typography variant="h4">
            Challenges
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Create Challenge
          </Button>
        </Box>

        {isLoading ? (
          <Typography>Loading challenges...</Typography>
        ) : (
          <>
            <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
              Active Challenges
            </Typography>
            <Grid container spacing={3} sx={{ mb: 6 }}>
              {activeChallenges.map((challenge) => (
                <Grid item xs={12} sm={6} md={4} key={challenge.id}>
                  <ChallengeCard challenge={challenge} />
                </Grid>
              ))}
            </Grid>

            <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
              Completed Challenges
            </Typography>
            <Grid container spacing={3}>
              {completedChallenges.map((challenge) => (
                <Grid item xs={12} sm={6} md={4} key={challenge.id}>
                  <ChallengeCard challenge={challenge} />
                </Grid>
              ))}
            </Grid>
          </>
        )}
      </Box>

      <CreateChallengeDialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
      />
    </Container>
  );
};

export default Challenges;