import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Button,
} from '@mui/material';
import { getWorkouts } from '../api/api';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

interface Workout {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

export default function Dashboard() {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const data = await getWorkouts();
        setWorkouts(data);
      } catch (error) {
        console.error('Failed to fetch workouts:', error);
      }
    };

    if (isAuthenticated) {
      fetchWorkouts();
    }
  }, [isAuthenticated]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Your Workouts
        </Typography>
        <Button
          component={Link}
          to="/create-workout"
          variant="contained"
          color="primary"
        >
          Create New Workout
        </Button>
      </Box>

      <Grid container spacing={3}>
        {workouts.map((workout) => (
          <Grid item xs={12} sm={6} md={4} key={workout.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2">
                  {workout.name}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Created: {new Date(workout.created_at).toLocaleDateString()}
                </Typography>
                <Typography variant="body2">
                  {workout.description}
                </Typography>
                <Button
                  component={Link}
                  to={`/workout/${workout.id}`}
                  sx={{ mt: 2 }}
                >
                  View Details
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
        {workouts.length === 0 && (
          <Grid item xs={12}>
            <Typography variant="h6" align="center" color="textSecondary">
              No workouts yet. Create your first workout!
            </Typography>
          </Grid>
        )}
      </Grid>
    </Container>
  );
}