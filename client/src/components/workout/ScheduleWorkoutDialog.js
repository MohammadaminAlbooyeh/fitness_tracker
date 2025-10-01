import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Stack,
  FormControlLabel,
  Switch,
  Alert
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers';
import { useMutation, useQueryClient } from 'react-query';
import { scheduleWorkout } from '../../api/workout';

const ScheduleWorkoutDialog = ({ open, onClose, template }) => {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    scheduledDate: null,
    notes: '',
    reminderEnabled: true,
    reminderTime: null,
  });
  const [error, setError] = useState(null);

  const scheduleMutation = useMutation(scheduleWorkout, {
    onSuccess: () => {
      queryClient.invalidateQueries(['scheduledWorkouts']);
      onClose();
    },
    onError: (err) => {
      setError(err.message);
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.scheduledDate) {
      setError('Please select a workout date');
      return;
    }

    const reminderData = formData.reminderEnabled && formData.reminderTime ? {
      reminder_time: formData.reminderTime,
      notification_type: 'push' // Default to push notifications
    } : null;

    scheduleMutation.mutate({
      template_id: template.id,
      scheduled_date: formData.scheduledDate.toISOString(),
      notes: formData.notes,
      reminder_enabled: formData.reminderEnabled,
      reminder: reminderData
    });
  };

  const handleChange = (field) => (value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    setError(null);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Schedule Workout: {template?.name}</DialogTitle>
      
      <DialogContent>
        <Stack spacing={3} sx={{ mt: 2 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <DateTimePicker
            label="Workout Date & Time"
            value={formData.scheduledDate}
            onChange={handleChange('scheduledDate')}
            renderInput={(params) => <TextField {...params} fullWidth />}
            minDateTime={new Date()}
          />

          <TextField
            label="Notes"
            multiline
            rows={3}
            value={formData.notes}
            onChange={(e) => handleChange('notes')(e.target.value)}
            fullWidth
          />

          <FormControlLabel
            control={
              <Switch
                checked={formData.reminderEnabled}
                onChange={(e) => handleChange('reminderEnabled')(e.target.checked)}
                color="primary"
              />
            }
            label="Enable Reminder"
          />

          {formData.reminderEnabled && (
            <DateTimePicker
              label="Reminder Time"
              value={formData.reminderTime}
              onChange={handleChange('reminderTime')}
              renderInput={(params) => <TextField {...params} fullWidth />}
              minDateTime={new Date()}
              maxDateTime={formData.scheduledDate}
            />
          )}
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          color="primary"
          disabled={scheduleMutation.isLoading}
        >
          Schedule
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ScheduleWorkoutDialog;