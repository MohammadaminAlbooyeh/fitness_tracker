import React, { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  Tab,
  Tabs,
  IconButton,
  Dialog,
  useTheme
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Schedule as ScheduleIcon,
  Assistant as AssistantIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import Calendar from './Calendar';
import SchedulePreferences from './SchedulePreferences';
import SmartScheduling from './SmartScheduling';
import {
  getSchedulePreferences,
  updateSchedulePreferences,
  generateSmartSchedule
} from '../../api/scheduling';

const TabPanel = ({ children, value, index, ...other }) => (
  <div
    role="tabpanel"
    hidden={value !== index}
    id={`scheduling-tabpanel-${index}`}
    aria-labelledby={`scheduling-tab-${index}`}
    {...other}
  >
    {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
  </div>
);

const ScheduleManager = () => {
  const theme = useTheme();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState(0);
  const [isPreferencesOpen, setIsPreferencesOpen] = useState(false);

  // Fetch user's schedule preferences
  const { data: preferences, isLoading: loadingPreferences } = useQuery(
    'schedulePreferences',
    () => getSchedulePreferences(1) // Replace with actual user ID
  );

  // Update preferences mutation
  const updatePreferencesMutation = useMutation(updateSchedulePreferences, {
    onSuccess: () => {
      queryClient.invalidateQueries('schedulePreferences');
      setIsPreferencesOpen(false);
    }
  });

  // Generate smart schedule mutation
  const generateScheduleMutation = useMutation(generateSmartSchedule, {
    onSuccess: (data) => {
      queryClient.invalidateQueries(['events']);
      // Handle success (e.g., show success message, update calendar view)
    }
  });

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handlePreferencesSubmit = (updatedPreferences) => {
    updatePreferencesMutation.mutate(updatedPreferences);
  };

  const handleSmartScheduleGenerate = (params) => {
    generateScheduleMutation.mutate(params);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Header */}
          <Grid item xs={12}>
            <Box
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              mb={3}
            >
              <Typography variant="h4">Schedule Manager</Typography>
              <Box>
                <IconButton
                  onClick={() => setIsPreferencesOpen(true)}
                  color="primary"
                >
                  <SettingsIcon />
                </IconButton>
              </Box>
            </Box>
          </Grid>

          {/* Main Content */}
          <Grid item xs={12}>
            <Paper elevation={3}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs
                  value={activeTab}
                  onChange={handleTabChange}
                  aria-label="schedule manager tabs"
                >
                  <Tab
                    icon={<CalendarIcon />}
                    label="Calendar"
                    id="scheduling-tab-0"
                  />
                  <Tab
                    icon={<ScheduleIcon />}
                    label="Schedule"
                    id="scheduling-tab-1"
                  />
                  <Tab
                    icon={<AssistantIcon />}
                    label="Smart Scheduling"
                    id="scheduling-tab-2"
                  />
                </Tabs>
              </Box>

              {/* Calendar View */}
              <TabPanel value={activeTab} index={0}>
                <Calendar />
              </TabPanel>

              {/* Schedule Management */}
              <TabPanel value={activeTab} index={1}>
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Upcoming Schedule
                  </Typography>
                  {/* Add schedule management components here */}
                </Box>
              </TabPanel>

              {/* Smart Scheduling */}
              <TabPanel value={activeTab} index={2}>
                <SmartScheduling
                  preferences={preferences}
                  onGenerate={handleSmartScheduleGenerate}
                  isGenerating={generateScheduleMutation.isLoading}
                />
              </TabPanel>
            </Paper>
          </Grid>
        </Grid>

        {/* Preferences Dialog */}
        <Dialog
          open={isPreferencesOpen}
          onClose={() => setIsPreferencesOpen(false)}
          maxWidth="md"
          fullWidth
        >
          <SchedulePreferences
            preferences={preferences}
            onSubmit={handlePreferencesSubmit}
            onClose={() => setIsPreferencesOpen(false)}
            isSubmitting={updatePreferencesMutation.isLoading}
          />
        </Dialog>
      </Box>
    </Container>
  );
};

export default ScheduleManager;