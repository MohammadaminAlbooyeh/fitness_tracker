import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  IconButton,
  Button,
  Chip,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { fetchScheduledWorkouts, updateWorkoutStatus } from '../../api/workout';
import { formatDateTime } from '../../utils/timeUtils';

const ScheduledWorkoutList = () => {
  const queryClient = useQueryClient();
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedWorkout, setSelectedWorkout] = useState(null);

  const { data: workouts, isLoading } = useQuery(
    'scheduledWorkouts',
    fetchScheduledWorkouts
  );

  const updateStatusMutation = useMutation(updateWorkoutStatus, {
    onSuccess: () => {
      queryClient.invalidateQueries('scheduledWorkouts');
      handleCloseMenu();
    }
  });

  const handleOpenMenu = (event, workout) => {
    setAnchorEl(event.currentTarget);
    setSelectedWorkout(workout);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
    setSelectedWorkout(null);
  };

  const handleStatusUpdate = (status) => {
    if (selectedWorkout) {
      updateStatusMutation.mutate({
        workoutId: selectedWorkout.id,
        status
      });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'cancelled':
        return 'error';
      case 'scheduled':
        return 'primary';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon />;
      case 'cancelled':
        return <CancelIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  if (isLoading) return <div>Loading...</div>;

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Scheduled Workouts
        </Typography>

        <Grid container spacing={3}>
          {workouts?.map((workout) => (
            <Grid item xs={12} key={workout.id}>
              <Paper sx={{ p: 3 }}>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} sm={4}>
                    <Typography variant="h6">
                      {workout.template.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {workout.template.category} | {workout.template.difficulty}
                    </Typography>
                  </Grid>

                  <Grid item xs={12} sm={3}>
                    <Typography variant="body2" color="text.secondary">
                      Scheduled for:
                    </Typography>
                    <Typography>
                      {formatDateTime(workout.scheduled_date)}
                    </Typography>
                  </Grid>

                  <Grid item xs={12} sm={3}>
                    <Chip
                      icon={getStatusIcon(workout.status)}
                      label={workout.status.toUpperCase()}
                      color={getStatusColor(workout.status)}
                      variant="outlined"
                    />
                  </Grid>

                  <Grid item xs={12} sm={2}>
                    <IconButton
                      onClick={(e) => handleOpenMenu(e, workout)}
                      disabled={workout.status === 'completed'}
                    >
                      <MoreVertIcon />
                    </IconButton>
                  </Grid>

                  {workout.notes && (
                    <Grid item xs={12}>
                      <Typography variant="body2" color="text.secondary">
                        Notes: {workout.notes}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
          ))}
        </Grid>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleCloseMenu}
        >
          <MenuItem onClick={() => handleStatusUpdate('completed')}>
            Mark as Completed
          </MenuItem>
          <MenuItem onClick={() => handleStatusUpdate('cancelled')}>
            Cancel Workout
          </MenuItem>
        </Menu>
      </Box>
    </Container>
  );
};

export default ScheduledWorkoutList;