import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Box
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format, subMonths } from 'date-fns';
import { Add as AddIcon } from '@mui/icons-material';
import { createMeasurement, fetchMeasurements } from '../../api/progress';

const MEASUREMENT_TYPES = [
  { value: 'weight', label: 'Weight', unit: 'kg' },
  { value: 'body_fat', label: 'Body Fat', unit: '%' },
  { value: 'chest', label: 'Chest', unit: 'cm' },
  { value: 'waist', label: 'Waist', unit: 'cm' },
  { value: 'hips', label: 'Hips', unit: 'cm' },
  { value: 'biceps', label: 'Biceps', unit: 'cm' },
  { value: 'thighs', label: 'Thighs', unit: 'cm' },
];

const MeasurementsTracker = () => {
  const queryClient = useQueryClient();
  const [selectedType, setSelectedType] = useState('weight');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    measurement_type: 'weight',
    value: '',
    notes: ''
  });

  const { data: measurements, isLoading } = useQuery(
    ['measurements', selectedType],
    () => fetchMeasurements({ type: selectedType })
  );

  const createMutation = useMutation(createMeasurement, {
    onSuccess: () => {
      queryClient.invalidateQueries(['measurements', selectedType]);
      setDialogOpen(false);
      setFormData({ measurement_type: 'weight', value: '', notes: '' });
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const measurementType = MEASUREMENT_TYPES.find(t => t.value === formData.measurement_type);
    createMutation.mutate({
      ...formData,
      unit: measurementType.unit
    });
  };

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const chartData = measurements?.map(m => ({
    date: format(new Date(m.date), 'MMM dd'),
    value: m.value
  })) || [];

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4" gutterBottom>
              Measurements Tracker
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setDialogOpen(true)}
            >
              Add Measurement
            </Button>
          </Grid>

          <Grid item xs={12} md={3}>
            {MEASUREMENT_TYPES.map(type => (
              <Button
                key={type.value}
                fullWidth
                variant={selectedType === type.value ? "contained" : "outlined"}
                onClick={() => setSelectedType(type.value)}
                sx={{ mb: 1 }}
              >
                {type.label}
              </Button>
            ))}
          </Grid>

          <Grid item xs={12} md={9}>
            <Paper sx={{ p: 3, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                {MEASUREMENT_TYPES.find(t => t.value === selectedType)?.label} Progress
              </Typography>
              
              {isLoading ? (
                <Typography>Loading...</Typography>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#8884d8"
                      strokeWidth={2}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              )}
            </Paper>
          </Grid>
        </Grid>

        <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
          <DialogTitle>Add New Measurement</DialogTitle>
          <DialogContent>
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Measurement Type"
                  value={formData.measurement_type}
                  onChange={handleChange('measurement_type')}
                >
                  {MEASUREMENT_TYPES.map(type => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label} ({type.unit})
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  type="number"
                  label="Value"
                  value={formData.value}
                  onChange={handleChange('value')}
                  InputProps={{
                    endAdornment: MEASUREMENT_TYPES.find(
                      t => t.value === formData.measurement_type
                    )?.unit
                  }}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Notes"
                  value={formData.notes}
                  onChange={handleChange('notes')}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
            <Button
              onClick={handleSubmit}
              variant="contained"
              color="primary"
              disabled={createMutation.isLoading}
            >
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default MeasurementsTracker;