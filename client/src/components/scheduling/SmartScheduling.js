import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  CircularProgress
} from '@mui/material';
import {
  FitnessCenter as WorkoutIcon,
  Schedule as ScheduleIcon,
  Assessment as AssessmentIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useQuery } from 'react-query';
import { addWeeks } from 'date-fns';
import { getRecoveryMetrics } from '../../api/health';

const EVENT_TYPES = [
  { value: 'workout', label: 'Workout', icon: WorkoutIcon },
  { value: 'assessment', label: 'Assessment', icon: AssessmentIcon }
];

const INTENSITY_LEVELS = [
  { value: 'low', label: 'Low Intensity' },
  { value: 'medium', label: 'Medium Intensity' },
  { value: 'high', label: 'High Intensity' }
];

const TIME_PREFERENCES = [
  { value: 'morning', label: 'Morning (5:00 - 12:00)' },
  { value: 'afternoon', label: 'Afternoon (12:00 - 17:00)' },
  { value: 'evening', label: 'Evening (17:00 - 22:00)' }
];

const SmartScheduling = ({ preferences, onGenerate, isGenerating }) => {
  const [formData, setFormData] = useState({
    start_date: new Date(),
    end_date: addWeeks(new Date(), 2),
    event_types: ['workout'],
    constraints: {
      min_duration: 45,
      max_duration: 90,
      preferred_time_of_day: 'morning',
      intensity_level: 'medium'
    }
  });

  const [validationError, setValidationError] = useState(null);

  // Fetch recovery metrics for AI-powered scheduling
  const { data: recoveryMetrics } = useQuery(
    ['recoveryMetrics', formData.start_date],
    () => getRecoveryMetrics()
  );

  const handleChange = (field, isConstraint = false) => (event) => {
    setFormData((prev) => ({
      ...prev,
      [isConstraint ? 'constraints' : field]:
        isConstraint
          ? { ...prev.constraints, [field]: event.target.value }
          : event.target.value
    }));
  };

  const handleDateChange = (field) => (date) => {
    setFormData((prev) => ({
      ...prev,
      [field]: date
    }));
  };

  const handleEventTypeToggle = (type) => {
    setFormData((prev) => {
      const types = prev.event_types.includes(type)
        ? prev.event_types.filter((t) => t !== type)
        : [...prev.event_types, type];
      return {
        ...prev,
        event_types: types
      };
    });
  };

  const handleSubmit = () => {
    // Validate form data
    if (formData.end_date <= formData.start_date) {
      setValidationError('End date must be after start date');
      return;
    }

    if (formData.event_types.length === 0) {
      setValidationError('Please select at least one event type');
      return;
    }

    onGenerate(formData);
  };

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Smart Schedule Generation
          </Typography>
          <Typography color="textSecondary" paragraph>
            Let AI help you create an optimized schedule based on your preferences
            and recovery metrics.
          </Typography>
        </Grid>

        {/* Recovery Status */}
        {recoveryMetrics && (
          <Grid item xs={12}>
            <Paper sx={{ p: 2, mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Current Recovery Status
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Typography color="textSecondary">
                      Readiness Score
                    </Typography>
                    <Typography variant="h4" color={
                      recoveryMetrics.readiness_score >= 80
                        ? 'success.main'
                        : recoveryMetrics.readiness_score >= 60
                        ? 'warning.main'
                        : 'error.main'
                    }>
                      {recoveryMetrics.readiness_score}%
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Typography color="textSecondary">
                      Recommended Intensity
                    </Typography>
                    <Chip
                      label={
                        recoveryMetrics.readiness_score >= 80
                          ? 'High'
                          : recoveryMetrics.readiness_score >= 60
                          ? 'Medium'
                          : 'Low'
                      }
                      color={
                        recoveryMetrics.readiness_score >= 80
                          ? 'success'
                          : recoveryMetrics.readiness_score >= 60
                          ? 'warning'
                          : 'error'
                      }
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Typography color="textSecondary">
                      Rest Recommendation
                    </Typography>
                    <Typography variant="body1">
                      {recoveryMetrics.readiness_score < 60
                        ? 'Rest Day Recommended'
                        : 'Ready for Activity'}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}

        {/* Schedule Parameters */}
        <Grid item xs={12} md={6}>
          <DatePicker
            label="Start Date"
            value={formData.start_date}
            onChange={handleDateChange('start_date')}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <DatePicker
            label="End Date"
            value={formData.end_date}
            onChange={handleDateChange('end_date')}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>

        {/* Event Types */}
        <Grid item xs={12}>
          <Typography variant="subtitle1" gutterBottom>
            Event Types
          </Typography>
          <Box display="flex" gap={1}>
            {EVENT_TYPES.map((type) => {
              const Icon = type.icon;
              return (
                <Chip
                  key={type.value}
                  icon={<Icon />}
                  label={type.label}
                  onClick={() => handleEventTypeToggle(type.value)}
                  color={
                    formData.event_types.includes(type.value)
                      ? 'primary'
                      : 'default'
                  }
                />
              );
            })}
          </Box>
        </Grid>

        {/* Constraints */}
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="number"
            label="Minimum Duration (minutes)"
            value={formData.constraints.min_duration}
            onChange={handleChange('min_duration', true)}
            inputProps={{ min: 15, max: 180 }}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="number"
            label="Maximum Duration (minutes)"
            value={formData.constraints.max_duration}
            onChange={handleChange('max_duration', true)}
            inputProps={{ min: 15, max: 180 }}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Preferred Time of Day</InputLabel>
            <Select
              value={formData.constraints.preferred_time_of_day}
              onChange={handleChange('preferred_time_of_day', true)}
              label="Preferred Time of Day"
            >
              {TIME_PREFERENCES.map((time) => (
                <MenuItem key={time.value} value={time.value}>
                  {time.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Intensity Level</InputLabel>
            <Select
              value={formData.constraints.intensity_level}
              onChange={handleChange('intensity_level', true)}
              label="Intensity Level"
            >
              {INTENSITY_LEVELS.map((level) => (
                <MenuItem key={level.value} value={level.value}>
                  {level.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        {validationError && (
          <Grid item xs={12}>
            <Alert severity="error">{validationError}</Alert>
          </Grid>
        )}

        {/* Generate Button */}
        <Grid item xs={12}>
          <Box display="flex" justifyContent="flex-end">
            <Button
              variant="contained"
              size="large"
              onClick={handleSubmit}
              disabled={isGenerating}
              startIcon={
                isGenerating ? (
                  <CircularProgress size={20} color="inherit" />
                ) : (
                  <ScheduleIcon />
                )
              }
            >
              {isGenerating ? 'Generating...' : 'Generate Smart Schedule'}
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SmartScheduling;