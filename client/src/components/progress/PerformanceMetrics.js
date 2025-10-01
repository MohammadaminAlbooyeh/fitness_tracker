import React from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  Tabs,
  Tab,
  CircularProgress,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Timer as TimerIcon,
  FitnessCenter as WeightIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { Line } from 'recharts';
import { format } from 'date-fns';
import { fetchPerformanceMetrics } from '../../api/progress';

const MetricCard = ({ title, value, unit, icon, change }) => (
  <Card>
    <CardContent>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="body2" color="text.secondary">
            {title}
          </Typography>
          <Typography variant="h5" component="div" sx={{ mt: 1 }}>
            {value} {unit}
          </Typography>
        </Box>
        <IconButton
          sx={{
            backgroundColor: 'primary.light',
            color: 'primary.main',
            '&:hover': { backgroundColor: 'primary.main', color: 'white' }
          }}
        >
          {icon}
        </IconButton>
      </Box>
      {change && (
        <Typography
          variant="caption"
          color={change >= 0 ? 'success.main' : 'error.main'}
          sx={{ display: 'flex', alignItems: 'center', mt: 1 }}
        >
          <TrendingUpIcon
            sx={{
              mr: 0.5,
              transform: change >= 0 ? 'none' : 'rotate(180deg)'
            }}
          />
          {Math.abs(change)}% from last month
        </Typography>
      )}
    </CardContent>
  </Card>
);

const PerformanceMetrics = () => {
  const [selectedMetric, setSelectedMetric] = React.useState('strength');
  const [timeRange, setTimeRange] = React.useState('month');

  const { data: metrics, isLoading } = useQuery(
    ['performanceMetrics', selectedMetric, timeRange],
    () => fetchPerformanceMetrics(selectedMetric, timeRange)
  );

  const metricTypes = [
    { value: 'strength', label: 'Strength' },
    { value: 'endurance', label: 'Endurance' },
    { value: 'power', label: 'Power' },
    { value: 'speed', label: 'Speed' }
  ];

  const timeRanges = [
    { value: 'week', label: 'Week' },
    { value: 'month', label: 'Month' },
    { value: 'year', label: 'Year' }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Performance Metrics
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Tabs
              value={selectedMetric}
              onChange={(e, v) => setSelectedMetric(v)}
              variant="scrollable"
              scrollButtons="auto"
            >
              {metricTypes.map(type => (
                <Tab
                  key={type.value}
                  value={type.value}
                  label={type.label}
                />
              ))}
            </Tabs>
          </Grid>

          {isLoading ? (
            <Grid item xs={12} textAlign="center">
              <CircularProgress />
            </Grid>
          ) : (
            <>
              <Grid item xs={12} md={3}>
                <MetricCard
                  title="Max Weight"
                  value={metrics?.maxWeight || 0}
                  unit="kg"
                  icon={<WeightIcon />}
                  change={metrics?.weightChange}
                />
              </Grid>
              
              <Grid item xs={12} md={3}>
                <MetricCard
                  title="Best Time"
                  value={metrics?.bestTime || 0}
                  unit="sec"
                  icon={<TimerIcon />}
                  change={metrics?.timeChange}
                />
              </Grid>
              
              <Grid item xs={12} md={3}>
                <MetricCard
                  title="Peak Power"
                  value={metrics?.peakPower || 0}
                  unit="watts"
                  icon={<SpeedIcon />}
                  change={metrics?.powerChange}
                />
              </Grid>

              <Grid item xs={12}>
                <Paper sx={{ p: 3 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                    <Typography variant="h6">
                      Progress Over Time
                    </Typography>
                    <Tabs
                      value={timeRange}
                      onChange={(e, v) => setTimeRange(v)}
                      size="small"
                    >
                      {timeRanges.map(range => (
                        <Tab
                          key={range.value}
                          value={range.value}
                          label={range.label}
                        />
                      ))}
                    </Tabs>
                  </Box>

                  {metrics?.timeSeriesData && (
                    <Line
                      data={metrics.timeSeriesData}
                      height={400}
                      margin={{
                        top: 20,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                    >
                      {/* Chart configuration */}
                    </Line>
                  )}
                </Paper>
              </Grid>
            </>
          )}
        </Grid>
      </Box>
    </Container>
  );
};

export default PerformanceMetrics;