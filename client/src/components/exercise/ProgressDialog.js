import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Stack,
  Typography,
  Rating,
  Alert,
  Box
} from '@mui/material';
import { useMutation, useQueryClient } from 'react-query';
import { logExerciseProgress } from '../../api/exercise';

const ProgressDialog = ({ open, onClose, exercise }) => {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    weight: '',
    reps: '',
    sets: '',
    duration: '',
    distance: '',
    notes: '',
    form_rating: 5,
    form_feedback: ''
  });
  
  const [error, setError] = useState(null);

  const progressMutation = useMutation(logExerciseProgress, {
    onSuccess: () => {
      queryClient.invalidateQueries(['exerciseProgress', exercise.id]);
      onClose();
    },
    onError: (err) => {
      setError(err.message);
    }
  });

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
    setError(null);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      exercise_id: exercise.id,
      ...formData
    };
    progressMutation.mutate(data);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Log Progress: {exercise.name}</DialogTitle>
      
      <DialogContent>
        <Stack spacing={3} sx={{ mt: 2 }}>
          {error && (
            <Alert severity="error">
              {error}
            </Alert>
          )}

          {/* Show relevant fields based on exercise category */}
          {exercise.category === 'strength' && (
            <>
              <TextField
                label="Weight (kg)"
                type="number"
                value={formData.weight}
                onChange={handleChange('weight')}
                inputProps={{ min: 0, step: 0.5 }}
              />
              <TextField
                label="Reps"
                type="number"
                value={formData.reps}
                onChange={handleChange('reps')}
                inputProps={{ min: 1 }}
              />
              <TextField
                label="Sets"
                type="number"
                value={formData.sets}
                onChange={handleChange('sets')}
                inputProps={{ min: 1 }}
              />
            </>
          )}

          {exercise.category === 'cardio' && (
            <>
              <TextField
                label="Duration (minutes)"
                type="number"
                value={formData.duration}
                onChange={handleChange('duration')}
                inputProps={{ min: 1 }}
              />
              <TextField
                label="Distance (meters)"
                type="number"
                value={formData.distance}
                onChange={handleChange('distance')}
                inputProps={{ min: 0 }}
              />
            </>
          )}

          <Box>
            <Typography component="legend">Form Rating</Typography>
            <Rating
              value={formData.form_rating}
              onChange={(event, newValue) => {
                setFormData(prev => ({
                  ...prev,
                  form_rating: newValue
                }));
              }}
            />
          </Box>

          <TextField
            label="Form Feedback"
            multiline
            rows={2}
            value={formData.form_feedback}
            onChange={handleChange('form_feedback')}
          />

          <TextField
            label="Notes"
            multiline
            rows={3}
            value={formData.notes}
            onChange={handleChange('notes')}
          />
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          color="primary"
          disabled={progressMutation.isLoading}
        >
          Save Progress
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ProgressDialog;