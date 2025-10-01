import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  CircularProgress
} from '@mui/material';
import { Calendar, ClientList, AppointmentList, Stats } from './components';
import { useAuth } from '../hooks/useAuth';
import { useProfessional } from '../hooks/useProfessional';
import { Professional, Appointment, Client, Stats as StatsType } from '../types';

const ProfessionalDashboard = () => {
  const { user } = useAuth();
  const { professional, loading: profLoading } = useProfessional();
  const [stats, setStats] = useState<StatsType | null>(null);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, appointmentsRes, clientsRes] = await Promise.all([
          fetch('/api/professional/stats'),
          fetch('/api/professional/appointments?upcoming=true'),
          fetch('/api/professional/clients')
        ]);

        const [statsData, appointmentsData, clientsData] = await Promise.all([
          statsRes.json(),
          appointmentsRes.json(),
          clientsRes.json()
        ]);

        setStats(statsData);
        setAppointments(appointmentsData);
        setClients(clientsData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (professional) {
      fetchDashboardData();
    }
  }, [professional]);

  if (profLoading || loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box py={4}>
        <Typography variant="h4" gutterBottom>
          Welcome back, {professional?.user?.name}
        </Typography>

        <Grid container spacing={3}>
          {/* Stats Overview */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Stats
                    title="Total Clients"
                    value={stats?.total_clients || 0}
                    trend={stats?.client_growth || 0}
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Stats
                    title="Monthly Revenue"
                    value={stats?.monthly_revenue || 0}
                    trend={stats?.revenue_growth || 0}
                    format="currency"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Stats
                    title="Average Rating"
                    value={stats?.average_rating || 0}
                    trend={stats?.rating_change || 0}
                    format="rating"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Stats
                    title="Completion Rate"
                    value={stats?.completion_rate || 0}
                    trend={stats?.completion_rate_change || 0}
                    format="percentage"
                  />
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Calendar */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Calendar
                appointments={appointments}
                onAppointmentUpdate={(appointment) => {
                  // Handle appointment update
                }}
              />
            </Paper>
          </Grid>

          {/* Upcoming Appointments */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <AppointmentList
                appointments={appointments}
                onStatusChange={(appointmentId, status) => {
                  // Handle status change
                }}
              />
            </Paper>
          </Grid>

          {/* Client List */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <ClientList
                clients={clients}
                onClientSelect={(client) => {
                  // Handle client selection
                }}
              />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default ProfessionalDashboard;