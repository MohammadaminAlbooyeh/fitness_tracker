import React, { useState, useEffect } from 'react';
import {
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Typography,
  Box,
  Chip,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton
} from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { format } from 'date-fns';

const DAYS_OF_WEEK = [
  { value: 0, label: 'Monday' },
  { value: 1, label: 'Tuesday' },
  { value: 2, label: 'Wednesday' },
  { value: 3, label: 'Thursday' },
  { value: 4, label: 'Friday' },
  { value: 5, label: 'Saturday' },
  { value: 6, label: 'Sunday' }
];

const NOTIFICATION_TYPES = [
  { value: 'email', label: 'Email' },
  { value: 'push', label: 'Push Notification' },
  { value: 'sms', label: 'SMS' }
];

const TIME_RANGES = [
  { value: 'morning', label: 'Morning (5:00 - 12:00)' },
  { value: 'afternoon', label: 'Afternoon (12:00 - 17:00)' },
  { value: 'evening', label: 'Evening (17:00 - 22:00)' }
];

const SchedulePreferences = ({
  preferences,
  onSubmit,
  onClose,
  isSubmitting
}) => {
  const initialState = {
    preferred_workout_days: [],
    preferred_workout_times: [],
    blackout_times: [],
    max_workouts_per_week: 5,
    min_rest_between_workouts: 24,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    notification_preferences: {
      types: ['email'],
      advance_notice: 30, // minutes
      reminders: [
        { type: 'email', time: 30 }, // 30 minutes before
        { type: 'push', time: 5 } // 5 minutes before
      ]
    }
  };

  const [formData, setFormData] = useState(preferences || initialState);
  const [newTimeRange, setNewTimeRange] = useState({
    start: null,
    end: null
  });
  const [validationError, setValidationError] = useState(null);

  useEffect(() => {
    if (preferences) {
      setFormData(preferences);
    }
  }, [preferences]);

  const handleChange = (field) => (event) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleDayToggle = (day) => {
    setFormData((prev) => {
      const days = prev.preferred_workout_days.includes(day)
        ? prev.preferred_workout_days.filter((d) => d !== day)
        : [...prev.preferred_workout_days, day];
      return {
        ...prev,
        preferred_workout_days: days
      };
    });
  };

  const handleTimeRangeAdd = () => {
    if (newTimeRange.start && newTimeRange.end) {
      if (newTimeRange.end <= newTimeRange.start) {
        setValidationError('End time must be after start time');
        return;
      }

      setFormData((prev) => ({
        ...prev,
        preferred_workout_times: [
          ...prev.preferred_workout_times,
          {
            start: format(newTimeRange.start, 'HH:mm'),
            end: format(newTimeRange.end, 'HH:mm')
          }
        ]
      }));
      setNewTimeRange({ start: null, end: null });
      setValidationError(null);
    }
  };

  const handleTimeRangeDelete = (index) => {
    setFormData((prev) => ({
      ...prev,
      preferred_workout_times: prev.preferred_workout_times.filter(
        (_, i) => i !== index
      )
    }));
  };

  const handleNotificationTypeToggle = (type) => {
    setFormData((prev) => {
      const types = prev.notification_preferences.types.includes(type)
        ? prev.notification_preferences.types.filter((t) => t !== type)
        : [...prev.notification_preferences.types, type];
      return {
        ...prev,
        notification_preferences: {
          ...prev.notification_preferences,
          types
        }
      };
    });
  };

  const handleSubmit = () => {
    // Validate form data
    if (formData.preferred_workout_days.length === 0) {
      setValidationError('Please select at least one preferred workout day');
      return;
    }

    if (formData.preferred_workout_times.length === 0) {
      setValidationError('Please add at least one preferred workout time range');
      return;
    }

    if (formData.notification_preferences.types.length === 0) {
      setValidationError('Please select at least one notification type');
      return;
    }

    onSubmit(formData);
  };

  return (
    <>
      <DialogTitle>Schedule Preferences</DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          {/* Preferred Workout Days */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Preferred Workout Days
            </Typography>
            <FormGroup row>
              {DAYS_OF_WEEK.map((day) => (
                <FormControlLabel
                  key={day.value}
                  control={
                    <Checkbox
                      checked={formData.preferred_workout_days.includes(day.value)}
                      onChange={() => handleDayToggle(day.value)}
                    />
                  }
                  label={day.label}
                />
              ))}
            </FormGroup>
          </Grid>

          {/* Preferred Workout Times */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Preferred Workout Times
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={5}>
                <TimePicker
                  label="Start Time"
                  value={newTimeRange.start}
                  onChange={(time) =>
                    setNewTimeRange((prev) => ({ ...prev, start: time }))
                  }
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
              <Grid item xs={12} sm={5}>
                <TimePicker
                  label="End Time"
                  value={newTimeRange.end}
                  onChange={(time) =>
                    setNewTimeRange((prev) => ({ ...prev, end: time }))
                  }
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
              <Grid item xs={12} sm={2}>
                <Button
                  variant="contained"
                  onClick={handleTimeRangeAdd}
                  disabled={!newTimeRange.start || !newTimeRange.end}
                  sx={{ height: '100%' }}
                >
                  <AddIcon />
                </Button>
              </Grid>
            </Grid>

            <List>
              {formData.preferred_workout_times.map((range, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${range.start} - ${range.end}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => handleTimeRangeDelete(index)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Grid>

          {/* Workout Limits */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Maximum Workouts per Week"
              value={formData.max_workouts_per_week}
              onChange={handleChange('max_workouts_per_week')}
              inputProps={{ min: 1, max: 7 }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Minimum Rest Between Workouts (hours)"
              value={formData.min_rest_between_workouts}
              onChange={handleChange('min_rest_between_workouts')}
              inputProps={{ min: 1, max: 72 }}
            />
          </Grid>

          {/* Notification Preferences */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Notification Preferences
            </Typography>
            <Box display="flex" gap={1} mb={2}>
              {NOTIFICATION_TYPES.map((type) => (
                <Chip
                  key={type.value}
                  label={type.label}
                  onClick={() => handleNotificationTypeToggle(type.value)}
                  color={
                    formData.notification_preferences.types.includes(type.value)
                      ? 'primary'
                      : 'default'
                  }
                />
              ))}
            </Box>
            <TextField
              fullWidth
              type="number"
              label="Default Advance Notice (minutes)"
              value={formData.notification_preferences.advance_notice}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  notification_preferences: {
                    ...prev.notification_preferences,
                    advance_notice: parseInt(e.target.value)
                  }
                }))
              }
              inputProps={{ min: 5, max: 1440 }}
            />
          </Grid>

          {validationError && (
            <Grid item xs={12}>
              <Alert severity="error">{validationError}</Alert>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Saving...' : 'Save Preferences'}
        </Button>
      </DialogActions>
    </>
  );
};

export default SchedulePreferences;