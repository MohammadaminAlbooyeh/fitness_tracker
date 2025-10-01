import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Card,
  CardContent,
  Slider
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Bedtime as BedtimeIcon,
  WbTwilight as WbTwilightIcon
} from '@mui/icons-material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, TimePicker, DatePicker } from '@mui/x-date-pickers';
import { format, differenceInHours, differenceInMinutes } from 'date-fns';
import { Line } from 'react-chartjs-2';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  getSleepData,
  createSleepEntry,
  updateSleepEntry,
  deleteSleepEntry,
  getSleepStatistics
} from '../../api/health';
import { SleepQuality } from '../../types/health';

const SleepTracking = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [openDialog, setOpenDialog] = useState(false);
  const [editEntry, setEditEntry] = useState(null);
  const queryClient = useQueryClient();

  const [formData, setFormData] = useState({
    date: new Date(),
    sleep_start: new Date(),
    sleep_end: new Date(),
    quality: 'GOOD',
    notes: ''
  });

  const { data: sleepData, isLoading: loadingSleep } = useQuery(
    ['sleepData', format(selectedDate, 'yyyy-MM')],
    () => getSleepData(selectedDate)
  );

  const { data: statistics, isLoading: loadingStats } = useQuery(
    'sleepStatistics',
    () => getSleepStatistics(30)
  );

  const createMutation = useMutation(createSleepEntry, {
    onSuccess: () => {
      queryClient.invalidateQueries('sleepData');
      queryClient.invalidateQueries('sleepStatistics');
      handleCloseDialog();
    }
  });

  const updateMutation = useMutation(updateSleepEntry, {
    onSuccess: () => {
      queryClient.invalidateQueries('sleepData');
      queryClient.invalidateQueries('sleepStatistics');
      handleCloseDialog();
    }
  });

  const deleteMutation = useMutation(deleteSleepEntry, {
    onSuccess: () => {
      queryClient.invalidateQueries('sleepData');
      queryClient.invalidateQueries('sleepStatistics');
    }
  });

  const handleOpenDialog = (entry = null) => {
    if (entry) {
      setFormData({
        ...entry,
        date: new Date(entry.date),
        sleep_start: new Date(entry.sleep_start),
        sleep_end: new Date(entry.sleep_end)
      });
      setEditEntry(entry);
    } else {
      setFormData({
        date: new Date(),
        sleep_start: new Date(),
        sleep_end: new Date(),
        quality: 'GOOD',
        notes: ''
      });
      setEditEntry(null);
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditEntry(null);
  };

  const handleSubmit = () => {
    const duration = differenceInHours(formData.sleep_end, formData.sleep_start);
    const data = {
      ...formData,
      duration
    };

    if (editEntry) {
      updateMutation.mutate({ id: editEntry.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const getSleepQualityColor = (quality) => {
    switch (quality) {
      case 'EXCELLENT':
        return '#4caf50';
      case 'GOOD':
        return '#8bc34a';
      case 'FAIR':
        return '#ffc107';
      case 'POOR':
        return '#f44336';
      default:
        return '#9e9e9e';
    }
  };

  const chartData = {
    labels: sleepData?.map(entry => format(new Date(entry.date), 'MMM dd')) || [],
    datasets: [
      {
        label: 'Sleep Duration (hours)',
        data: sleepData?.map(entry => entry.duration) || [],
        fill: false,
        borderColor: '#2196f3',
        tension: 0.4
      },
      {
        label: 'Sleep Score',
        data: sleepData?.map(entry => entry.sleep_score) || [],
        fill: false,
        borderColor: '#4caf50',
        tension: 0.4,
        yAxisID: 'y1'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Hours'
        }
      },
      y1: {
        beginAtZero: true,
        position: 'right',
        title: {
          display: true,
          text: 'Sleep Score'
        },
        grid: {
          drawOnChartArea: false
        }
      }
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h4">Sleep Tracking</Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => handleOpenDialog()}
              >
                Add Sleep Entry
              </Button>
            </Box>
          </Grid>

          {/* Statistics Cards */}
          <Grid item xs={12}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Average Sleep Duration
                    </Typography>
                    <Typography variant="h4">
                      {statistics?.average_duration?.toFixed(1)}h
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Average Sleep Score
                    </Typography>
                    <Typography variant="h4">
                      {statistics?.average_sleep_score?.toFixed(0)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      Deep Sleep Average
                    </Typography>
                    <Typography variant="h4">
                      {statistics?.average_deep_sleep?.toFixed(1)}h
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      REM Sleep Average
                    </Typography>
                    <Typography variant="h4">
                      {statistics?.average_rem_sleep?.toFixed(1)}h
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Grid>

          {/* Sleep Chart */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Sleep Trends
              </Typography>
              <Box sx={{ height: 300 }}>
                <Line data={chartData} options={chartOptions} />
              </Box>
            </Paper>
          </Grid>

          {/* Sleep Entries */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Sleep Log
              </Typography>
              {sleepData?.map((entry) => (
                <Box
                  key={entry.id}
                  sx={{
                    p: 2,
                    mb: 2,
                    border: 1,
                    borderColor: 'divider',
                    borderRadius: 1,
                    display: 'flex',
                    alignItems: 'center'
                  }}
                >
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="subtitle1">
                      {format(new Date(entry.date), 'MMMM d, yyyy')}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={2}>
                      <Box display="flex" alignItems="center">
                        <BedtimeIcon sx={{ mr: 1 }} />
                        {format(new Date(entry.sleep_start), 'hh:mm a')}
                      </Box>
                      <Box display="flex" alignItems="center">
                        <WbTwilightIcon sx={{ mr: 1 }} />
                        {format(new Date(entry.sleep_end), 'hh:mm a')}
                      </Box>
                      <Typography
                        sx={{
                          color: getSleepQualityColor(entry.quality),
                          fontWeight: 'bold'
                        }}
                      >
                        {entry.quality}
                      </Typography>
                    </Box>
                    {entry.notes && (
                      <Typography color="textSecondary" variant="body2">
                        {entry.notes}
                      </Typography>
                    )}
                  </Box>
                  <Box>
                    <IconButton onClick={() => handleOpenDialog(entry)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => deleteMutation.mutate(entry.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
              ))}
            </Paper>
          </Grid>
        </Grid>

        {/* Add/Edit Dialog */}
        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {editEntry ? 'Edit Sleep Entry' : 'Add Sleep Entry'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <DatePicker
                    label="Date"
                    value={formData.date}
                    onChange={(newValue) => setFormData({ ...formData, date: newValue })}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <TimePicker
                    label="Sleep Time"
                    value={formData.sleep_start}
                    onChange={(newValue) => setFormData({ ...formData, sleep_start: newValue })}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12} sm={6}>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <TimePicker
                    label="Wake Time"
                    value={formData.sleep_end}
                    onChange={(newValue) => setFormData({ ...formData, sleep_end: newValue })}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                  />
                </LocalizationProvider>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Sleep Quality</InputLabel>
                  <Select
                    value={formData.quality}
                    label="Sleep Quality"
                    onChange={(e) => setFormData({ ...formData, quality: e.target.value })}
                  >
                    {Object.values(SleepQuality).map((quality) => (
                      <MenuItem key={quality} value={quality}>
                        {quality}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Notes"
                  multiline
                  rows={4}
                  fullWidth
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={createMutation.isLoading || updateMutation.isLoading}
            >
              {editEntry ? 'Update' : 'Add'}
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default SleepTracking;