import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Grid,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Card,
  CardContent,
  useTheme,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  LinearProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { useNotification } from '../context/NotificationContext';
import { progressApi } from '../api/progress';

interface MeasurementGoal {
  metric: string;
  target: number;
  deadline: string;
}

interface BodyMeasurement {
  id: number;
  date: string;
  weight?: number;
  height?: number;
  body_fat?: number;
  muscle_mass?: number;
  chest?: number;
  waist?: number;
  hips?: number;
  biceps_left?: number;
  biceps_right?: number;
  thigh_left?: number;
  thigh_right?: number;
}

interface ProgressStats {
  weight_change: number;
  body_fat_change: number;
  muscle_mass_change: number;
}

export const BodyMeasurements: React.FC = () => {
  const theme = useTheme();
  const { showNotification } = useNotification();
  const [measurements, setMeasurements] = useState<BodyMeasurement[]>([]);
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState<Partial<BodyMeasurement>>({});
  const [goals, setGoals] = useState<MeasurementGoal[]>([]);
  const [showGoalDialog, setShowGoalDialog] = useState(false);
  const [newGoal, setNewGoal] = useState<Partial<MeasurementGoal>>({});
  const [selectedMetric, setSelectedMetric] = useState<string>('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [measurementsData, statsData] = await Promise.all([
        progressApi.getMeasurements(),
        progressApi.getProgressStats(),
      ]);
      setMeasurements(measurementsData);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching measurements:', error);
      showNotification('Failed to load measurements', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof BodyMeasurement) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({
      ...formData,
      [field]: event.target.value ? Number(event.target.value) : undefined,
    });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await progressApi.createMeasurement(formData);
      showNotification('Measurement added successfully', 'success');
      setFormData({});
      fetchData();
    } catch (error) {
      console.error('Error adding measurement:', error);
      showNotification('Failed to add measurement', 'error');
    }
  };

  // Goal Management
  const handleAddGoal = async (goalData: { metric: string; target: number; deadline: string }) => {
    try {
      await progressApi.createGoal(goalData);
      showNotification('Goal added successfully', 'success');
      fetchGoals();
      setShowGoalDialog(false);
    } catch (error) {
      console.error('Error adding goal:', error);
      showNotification('Failed to add goal', 'error');
    }
  };

  const handleEditGoal = async (id: number, goalData: { metric: string; target: number; deadline: string }) => {
    try {
      await progressApi.updateGoal(id, goalData);
      showNotification('Goal updated successfully', 'success');
      fetchGoals();
      setShowGoalDialog(false);
    } catch (error) {
      console.error('Error updating goal:', error);
      showNotification('Failed to update goal', 'error');
    }
  };

  const handleDeleteGoal = async (id: number) => {
    try {
      await progressApi.deleteGoal(id);
      showNotification('Goal deleted successfully', 'success');
      fetchGoals();
    } catch (error) {
      console.error('Error deleting goal:', error);
      showNotification('Failed to delete goal', 'error');
    }
  };

  const fetchGoals = async () => {
    try {
      const goalsData = await progressApi.getGoals();
      setGoals(goalsData);
    } catch (error) {
      console.error('Error fetching goals:', error);
      showNotification('Failed to load goals', 'error');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  const generateComparisonData = (measurements: BodyMeasurement[]) => {
    if (measurements.length < 2) return null;
    const latest = measurements[measurements.length - 1];
    const previous = measurements[measurements.length - 2];
    
    return Object.entries(latest)
      .filter(([key, value]) => 
        typeof value === 'number' && 
        key !== 'id' && 
        previous[key as keyof BodyMeasurement]
      )
      .map(([key, value]) => ({
        metric: key.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase()),
        current: value,
        previous: previous[key as keyof BodyMeasurement],
        change: Number(value) - Number(previous[key as keyof BodyMeasurement])
      }));
  };

  const comparisonData = generateComparisonData(measurements);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Body Measurements
      </Typography>

      {/* Latest vs Previous Comparison */}
      {comparisonData && comparisonData.length > 0 && (
        <Paper sx={{ p: 2, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Latest vs Previous Measurements
          </Typography>
          <Grid container spacing={2}>
            {comparisonData.map((item) => (
              <Grid item xs={12} sm={6} md={4} key={item.metric}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      {item.metric}
                    </Typography>
                    <Typography variant="h6">
                      Current: {item.current.toFixed(1)}
                    </Typography>
                    <Typography variant="body2">
                      Previous: {item.previous.toFixed(1)}
                    </Typography>
                    <Typography 
                      variant="body1" 
                      color={item.change > 0 ? 'success.main' : 'error.main'}
                      sx={{ mt: 1 }}
                    >
                      Change: {item.change > 0 ? '+' : ''}{item.change.toFixed(1)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {/* Progress Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Weight Change
              </Typography>
              <Typography variant="h4" color={stats?.weight_change > 0 ? 'error' : 'success'}>
                {stats?.weight_change?.toFixed(1)} kg
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Body Fat Change
              </Typography>
              <Typography variant="h4" color={stats?.body_fat_change > 0 ? 'error' : 'success'}>
                {stats?.body_fat_change?.toFixed(1)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Muscle Mass Change
              </Typography>
              <Typography variant="h4" color={stats?.muscle_mass_change > 0 ? 'success' : 'error'}>
                {stats?.muscle_mass_change?.toFixed(1)} kg
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Weight Chart */}
      <Paper sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Weight Progress
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={measurements}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <YAxis />
            <Tooltip
              labelFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <Line
              type="monotone"
              dataKey="weight"
              stroke={theme.palette.primary.main}
              name="Weight (kg)"
            />
          </LineChart>
        </ResponsiveContainer>
      </Paper>

      {/* Add New Measurement Form */}
      {/* Goals Section */}
      <Paper sx={{ p: 2, mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h6">
            Fitness Goals
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              setSelectedMetric('');
              setNewGoal({});
              setShowGoalDialog(true);
            }}
          >
            Add New Goal
          </Button>
        </Box>
        <Grid container spacing={3}>
          {goals.map((goal) => (
            <Grid item xs={12} sm={6} md={4} key={goal.id}>
              <GoalCard
                goal={goal}
                onEdit={() => {
                  setSelectedMetric(goal.metric);
                  setNewGoal({
                    metric: goal.metric,
                    target: goal.target,
                    deadline: goal.deadline,
                  });
                  setShowGoalDialog(true);
                }}
                onDelete={() => handleDeleteGoal(goal.id)}
              />
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Add Measurement Form */}
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Add New Measurement
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="Weight (kg)"
                type="number"
                value={formData.weight || ''}
                onChange={handleInputChange('weight')}
                inputProps={{ step: '0.1' }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="Body Fat %"
                type="number"
                value={formData.body_fat || ''}
                onChange={handleInputChange('body_fat')}
                inputProps={{ step: '0.1' }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                label="Muscle Mass (kg)"
                type="number"
                value={formData.muscle_mass || ''}
                onChange={handleInputChange('muscle_mass')}
                inputProps={{ step: '0.1' }}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
              >
                Add Measurement
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      {/* Goal Dialog */}
      <GoalDialog
        open={showGoalDialog}
        onClose={() => setShowGoalDialog(false)}
        onSubmit={(goalData) => {
          if (selectedMetric) {
            const goal = goals.find((g) => g.metric === selectedMetric);
            if (goal) {
              handleEditGoal(goal.id, goalData);
            }
          } else {
            handleAddGoal(goalData);
          }
        }}
        availableMetrics={[
          'Weight',
          'Body Fat',
          'Muscle Mass',
          'Chest',
          'Waist',
          'Hips',
          'Biceps (Left)',
          'Biceps (Right)',
          'Thigh (Left)',
          'Thigh (Right)',
        ]}
        initialData={newGoal.metric ? newGoal : undefined}
      />
    </Box>
  );
};