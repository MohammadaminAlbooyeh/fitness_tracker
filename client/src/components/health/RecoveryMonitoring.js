import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Divider,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Favorite as HeartIcon,
  DirectionsRun as ActivityIcon,
  RestartAlt as RecoveryIcon,
  BatterySaver as EnergyIcon,
  Info as InfoIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { format } from 'date-fns';
import { Line } from 'react-chartjs-2';
import { 
  getRecoveryMetrics,
  getRecoveryStatistics,
  getRecoveryRecommendations
} from '../../api/health';

const RecoveryScore = ({ score }) => {
  const getColor = (value) => {
    if (value >= 80) return 'success';
    if (value >= 60) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress
        variant="determinate"
        value={score}
        color={getColor(score)}
        size={120}
      />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography
          variant="h4"
          component="div"
          color={`${getColor(score)}.main`}
        >
          {score}
        </Typography>
      </Box>
    </Box>
  );
};

const MetricCard = ({ title, value, unit, icon: Icon, trend, info }) => (
  <Card>
    <CardContent>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Box display="flex" alignItems="center">
          {trend && (
            <Box component="span" sx={{ mr: 1 }}>
              {trend > 0 ? (
                <TrendingUpIcon color="success" />
              ) : (
                <TrendingDownIcon color="error" />
              )}
            </Box>
          )}
          <Tooltip title={info}>
            <IconButton size="small">
              <InfoIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      <Box display="flex" alignItems="center" mt={1}>
        <Icon sx={{ mr: 1, fontSize: 40, opacity: 0.7 }} />
        <Typography variant="h4">
          {value}
          {unit && (
            <Typography variant="subtitle1" component="span" sx={{ ml: 0.5 }}>
              {unit}
            </Typography>
          )}
        </Typography>
      </Box>
    </CardContent>
  </Card>
);

const RecommendationItem = ({ recommendation }) => {
  const getIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <ErrorIcon color="error" />;
      case 'medium':
        return <WarningIcon color="warning" />;
      default:
        return <CheckIcon color="success" />;
    }
  };

  return (
    <ListItem>
      <ListItemIcon>
        {getIcon(recommendation.priority)}
      </ListItemIcon>
      <ListItemText
        primary={recommendation.message}
        secondary={
          <List dense>
            {recommendation.actions.map((action, index) => (
              <ListItem key={index} dense>
                <ListItemText primary={action} />
              </ListItem>
            ))}
          </List>
        }
      />
      <Chip
        label={recommendation.type}
        color="primary"
        variant="outlined"
        size="small"
      />
    </ListItem>
  );
};

const RecoveryMonitoring = () => {
  const { data: metrics, isLoading: loadingMetrics } = useQuery(
    'recoveryMetrics',
    () => getRecoveryMetrics()
  );

  const { data: statistics, isLoading: loadingStats } = useQuery(
    'recoveryStatistics',
    () => getRecoveryStatistics(30)
  );

  const { data: recommendations, isLoading: loadingRecommendations } = useQuery(
    'recoveryRecommendations',
    getRecoveryRecommendations
  );

  const chartData = {
    labels: statistics?.recovery_trend?.map(
      (point) => format(new Date(point.date), 'MMM dd')
    ) || [],
    datasets: [
      {
        label: 'Readiness Score',
        data: statistics?.recovery_trend?.map((point) => point.score) || [],
        fill: false,
        borderColor: '#2196f3',
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Score'
        }
      }
    },
    plugins: {
      legend: {
        position: 'top'
      }
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h4" gutterBottom>
              Recovery Monitoring
            </Typography>
          </Grid>

          {/* Main Recovery Score */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                Today's Recovery Score
              </Typography>
              <RecoveryScore score={metrics?.readiness_score || 0} />
              <Typography
                variant="subtitle1"
                color="textSecondary"
                sx={{ mt: 2 }}
              >
                {metrics?.recovery_status}
              </Typography>
            </Paper>
          </Grid>

          {/* Key Metrics */}
          <Grid item xs={12} md={8}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <MetricCard
                  title="HRV Score"
                  value={metrics?.hrv_score || 0}
                  icon={HeartIcon}
                  trend={5}
                  info="Heart Rate Variability indicates autonomic nervous system recovery"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <MetricCard
                  title="Resting Heart Rate"
                  value={metrics?.resting_heart_rate || 0}
                  unit="bpm"
                  icon={HeartIcon}
                  trend={-2}
                  info="Lower resting heart rate typically indicates better recovery"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <MetricCard
                  title="Muscle Strain"
                  value={metrics?.muscle_strain || 0}
                  unit="%"
                  icon={ActivityIcon}
                  trend={8}
                  info="Indicates cumulative impact of recent workouts"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <MetricCard
                  title="Stress Level"
                  value={metrics?.stress_level || 0}
                  unit="%"
                  icon={EnergyIcon}
                  trend={-3}
                  info="Based on HRV and other recovery indicators"
                />
              </Grid>
            </Grid>
          </Grid>

          {/* Recovery Trend */}
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recovery Trend
              </Typography>
              <Box sx={{ height: 300 }}>
                <Line data={chartData} options={chartOptions} />
              </Box>
            </Paper>
          </Grid>

          {/* Recovery Statistics */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                30-Day Overview
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Average Readiness"
                    secondary={`${statistics?.average_readiness?.toFixed(1)}%`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Optimal Recovery Days"
                    secondary={statistics?.optimal_recovery_days}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Rest Days Needed"
                    secondary={statistics?.needs_rest_days}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Average HRV"
                    secondary={`${statistics?.average_hrv?.toFixed(1)} ms`}
                  />
                </ListItem>
              </List>
            </Paper>
          </Grid>

          {/* Recommendations */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Recovery Recommendations
              </Typography>
              <List>
                {recommendations?.map((recommendation, index) => (
                  <React.Fragment key={index}>
                    <RecommendationItem recommendation={recommendation} />
                    {index < recommendations.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default RecoveryMonitoring;