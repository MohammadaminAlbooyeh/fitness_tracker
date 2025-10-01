import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Switch,
  FormControlLabel,
  Grid,
  Autocomplete,
  CircularProgress,
  Alert
} from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useQuery } from 'react-query';
import { format, addHours } from 'date-fns';
import { getUsers } from '../../api/users';

const EVENT_TYPES = [
  { value: 'workout', label: 'Workout' },
  { value: 'class', label: 'Class' },
  { value: 'assessment', label: 'Assessment' },
  { value: 'recovery', label: 'Recovery' },
  { value: 'consultation', label: 'Consultation' }
];

const RECURRENCE_TYPES = [
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' }
];

const EventDialog = ({
  open,
  onClose,
  onSubmit,
  selectedDate,
  editEvent,
  isSubmitting
}) => {
  const initialState = {
    title: '',
    description: '',
    event_type: 'workout',
    start_time: selectedDate || new Date(),
    end_time: addHours(selectedDate || new Date(), 1),
    location: '',
    participants: [],
    is_recurring: false,
    recurrence: {
      type: 'weekly',
      interval: 1,
      days_of_week: [],
      end_date: null,
      max_occurrences: null
    },
    metadata: {}
  };

  const [formData, setFormData] = useState(editEvent || initialState);
  const [validationError, setValidationError] = useState(null);

  // Fetch users for participant selection
  const { data: users, isLoading: loadingUsers } = useQuery('users', getUsers);

  const handleChange = (field) => (event) => {
    setFormData((prev) => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleDateTimeChange = (field) => (value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value
    }));
  };

  const handleParticipantsChange = (event, value) => {
    setFormData((prev) => ({
      ...prev,
      participants: value.map((user) => user.id)
    }));
  };

  const handleRecurrenceChange = (field) => (event) => {
    setFormData((prev) => ({
      ...prev,
      recurrence: {
        ...prev.recurrence,
        [field]: event.target.value
      }
    }));
  };

  const handleSubmit = () => {
    // Validate form data
    if (!formData.title) {
      setValidationError('Title is required');
      return;
    }

    if (formData.end_time <= formData.start_time) {
      setValidationError('End time must be after start time');
      return;
    }

    onSubmit(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {editEvent ? 'Edit Event' : 'Create New Event'}
      </DialogTitle>
      <DialogContent>
        <Box component="form" noValidate sx={{ mt: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Title"
                value={formData.title}
                onChange={handleChange('title')}
                required
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

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Event Type</InputLabel>
                <Select
                  value={formData.event_type}
                  onChange={handleChange('event_type')}
                  label="Event Type"
                >
                  {EVENT_TYPES.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Location"
                value={formData.location}
                onChange={handleChange('location')}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <DatePicker
                label="Date"
                value={formData.start_time}
                onChange={(date) => {
                  const newStartTime = date;
                  const newEndTime = addHours(date, 1);
                  setFormData((prev) => ({
                    ...prev,
                    start_time: newStartTime,
                    end_time: newEndTime
                  }));
                }}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Grid>

            <Grid item xs={12} sm={3}>
              <TimePicker
                label="Start Time"
                value={formData.start_time}
                onChange={handleDateTimeChange('start_time')}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Grid>

            <Grid item xs={12} sm={3}>
              <TimePicker
                label="End Time"
                value={formData.end_time}
                onChange={handleDateTimeChange('end_time')}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Grid>

            <Grid item xs={12}>
              <Autocomplete
                multiple
                loading={loadingUsers}
                options={users || []}
                getOptionLabel={(option) => option.name}
                value={(users || []).filter((user) =>
                  formData.participants.includes(user.id)
                )}
                onChange={handleParticipantsChange}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Participants"
                    InputProps={{
                      ...params.InputProps,
                      endAdornment: (
                        <>
                          {loadingUsers && <CircularProgress size={20} />}
                          {params.InputProps.endAdornment}
                        </>
                      )
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formData.is_recurring}
                    onChange={(e) =>
                      setFormData((prev) => ({
                        ...prev,
                        is_recurring: e.target.checked
                      }))
                    }
                  />
                }
                label="Recurring Event"
              />
            </Grid>

            {formData.is_recurring && (
              <>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Recurrence Type</InputLabel>
                    <Select
                      value={formData.recurrence.type}
                      onChange={handleRecurrenceChange('type')}
                      label="Recurrence Type"
                    >
                      {RECURRENCE_TYPES.map((type) => (
                        <MenuItem key={type.value} value={type.value}>
                          {type.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Interval"
                    value={formData.recurrence.interval}
                    onChange={handleRecurrenceChange('interval')}
                    inputProps={{ min: 1 }}
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <DatePicker
                    label="End Date"
                    value={formData.recurrence.end_date}
                    onChange={(date) =>
                      setFormData((prev) => ({
                        ...prev,
                        recurrence: {
                          ...prev.recurrence,
                          end_date: date
                        }
                      }))
                    }
                    renderInput={(params) => <TextField {...params} fullWidth />}
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Maximum Occurrences"
                    value={formData.recurrence.max_occurrences}
                    onChange={handleRecurrenceChange('max_occurrences')}
                    inputProps={{ min: 1 }}
                  />
                </Grid>
              </>
            )}
          </Grid>

          {validationError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {validationError}
            </Alert>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Saving...' : editEvent ? 'Update' : 'Create'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default EventDialog;