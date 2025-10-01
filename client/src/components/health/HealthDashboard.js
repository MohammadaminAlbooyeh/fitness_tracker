import React from 'react';
import { Container, Grid, Paper, Typography, Box } from '@mui/material';
import SleepTracking from './SleepTracking';
import RecoveryMonitoring from './RecoveryMonitoring';
import { useQuery } from 'react-query';
import { getHealthSummary } from '../../api/health';

const HealthDashboard = () => {
  const { data: healthSummary, isLoading } = useQuery('healthSummary', () =>
    getHealthSummary(1, '7d')
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Health & Recovery Dashboard
        </Typography>

        {/* Overview Section */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Weekly Overview
              </Typography>
              {isLoading ? (
                <Typography>Loading summary...</Typography>
              ) : (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={3}>
                    <Box textAlign="center">
                      <Typography variant="subtitle1" color="textSecondary">
                        Average Recovery Score
                      </Typography>
                      <Typography variant="h4">
                        {healthSummary?.averageRecoveryScore}%
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box textAlign="center">
                      <Typography variant="subtitle1" color="textSecondary">
                        Average Sleep Duration
                      </Typography>
                      <Typography variant="h4">
                        {healthSummary?.averageSleepDuration}h
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box textAlign="center">
                      <Typography variant="subtitle1" color="textSecondary">
                        Stress Level
                      </Typography>
                      <Typography variant="h4">
                        {healthSummary?.averageStressLevel}%
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Box textAlign="center">
                      <Typography variant="subtitle1" color="textSecondary">
                        Active Days
                      </Typography>
                      <Typography variant="h4">
                        {healthSummary?.activeDays}/7
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              )}
            </Paper>
          </Grid>
        </Grid>

        {/* Main Components */}
        <Grid container spacing={3}>
          {/* Recovery Monitoring Section */}
          <Grid item xs={12}>
            <RecoveryMonitoring />
          </Grid>

          {/* Sleep Tracking Section */}
          <Grid item xs={12}>
            <SleepTracking />
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default HealthDashboard;