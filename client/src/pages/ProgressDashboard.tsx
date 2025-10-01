import React from 'react';
import { Box, Container, Grid, Typography, Paper, Tabs, Tab } from '@mui/material';
import { BodyMeasurements } from '../components/BodyMeasurements';
import { ProgressPhotos } from '../components/ProgressPhotos';
import { useNotification } from '../context/NotificationContext';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`progress-tabpanel-${index}`}
      aria-labelledby={`progress-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

export const ProgressDashboard: React.FC = () => {
  const [tabValue, setTabValue] = React.useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h3" gutterBottom>
          Progress Tracking
        </Typography>

        <Paper sx={{ width: '100%', mb: 4 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
            centered
          >
            <Tab label="Body Measurements" />
            <Tab label="Progress Photos" />
          </Tabs>
        </Paper>

        <TabPanel value={tabValue} index={0}>
          <BodyMeasurements />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <ProgressPhotos />
        </TabPanel>
      </Box>
    </Container>
  );
};