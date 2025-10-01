import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { getWorkouts } from '../api/api';

interface WorkoutLog {
  id: number;
  workout_id: number;
  completed_at: string;
  exercises: {
    name: string;
    sets: number;
    reps: number;
    weight?: number;
    duration?: number;
  }[];
}

interface WorkoutDetails {
  id: number;
  name: string;
  description: string;
  exercises: {
    name: string;
    sets: number;
    reps: number;
  }[];
}

export default function WorkoutProgress() {
  const [workout, setWorkout] = useState<WorkoutDetails | null>(null);
  const [logs, setLogs] = useState<WorkoutLog[]>([]);
  const [openLog, setOpenLog] = useState(false);
  const [currentLog, setCurrentLog] = useState<any>({});
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    const fetchWorkoutDetails = async () => {
      try {
        // You'll need to implement these API calls
        const workoutData = await getWorkouts();
        const logsData = []; // Implement getWorkoutLogs
        setWorkout(workoutData);
        setLogs(logsData);
      } catch (error) {
        console.error('Failed to fetch workout details:', error);
      }
    };

    if (id) {
      fetchWorkoutDetails();
    }
  }, [id]);

  const handleLogWorkout = () => {
    setOpenLog(true);
    // Initialize current log with workout exercises
    if (workout) {
      setCurrentLog({
        exercises: workout.exercises.map(ex => ({
          ...ex,
          completed_sets: [],
        })),
      });
    }
  };

  const handleSaveLog = async () => {
    try {
      // Implement saveWorkoutLog API call
      setOpenLog(false);
      // Refresh logs
      const newLogs = []; // Implement getWorkoutLogs
      setLogs(newLogs);
    } catch (error) {
      console.error('Failed to save workout log:', error);
    }
  };

  if (!workout) {
    return (
      <Container>
        <Typography>Loading...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {workout.name}
        </Typography>
        <Typography color="textSecondary" paragraph>
          {workout.description}
        </Typography>
        <Button
          variant="contained"
          onClick={handleLogWorkout}
          sx={{ mr: 2 }}
        >
          Log Workout
        </Button>
        <Button
          variant="outlined"
          onClick={() => navigate('/dashboard')}
        >
          Back to Dashboard
        </Button>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Workout Plan
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Exercise</TableCell>
                    <TableCell align="right">Sets</TableCell>
                    <TableCell align="right">Reps</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {workout.exercises.map((exercise, index) => (
                    <TableRow key={index}>
                      <TableCell>{exercise.name}</TableCell>
                      <TableCell align="right">{exercise.sets}</TableCell>
                      <TableCell align="right">{exercise.reps}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent History
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Progress</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {logs.map((log) => (
                    <TableRow key={log.id}>
                      <TableCell>
                        {new Date(log.completed_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        {/* Add a progress visualization */}
                        Completed
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={openLog} onClose={() => setOpenLog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Log Workout</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            {currentLog.exercises?.map((exercise: any, index: number) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  {exercise.name}
                </Typography>
                {Array.from({ length: exercise.sets }).map((_, setIndex) => (
                  <Box key={setIndex} sx={{ display: 'flex', gap: 2, mb: 1 }}>
                    <TextField
                      label={`Set ${setIndex + 1} Reps`}
                      type="number"
                      size="small"
                      onChange={(e) => {
                        const newLog = { ...currentLog };
                        if (!newLog.exercises[index].completed_sets[setIndex]) {
                          newLog.exercises[index].completed_sets[setIndex] = {};
                        }
                        newLog.exercises[index].completed_sets[setIndex].reps = Number(e.target.value);
                        setCurrentLog(newLog);
                      }}
                    />
                    <TextField
                      label="Weight (kg)"
                      type="number"
                      size="small"
                      onChange={(e) => {
                        const newLog = { ...currentLog };
                        if (!newLog.exercises[index].completed_sets[setIndex]) {
                          newLog.exercises[index].completed_sets[setIndex] = {};
                        }
                        newLog.exercises[index].completed_sets[setIndex].weight = Number(e.target.value);
                        setCurrentLog(newLog);
                      }}
                    />
                  </Box>
                ))}
              </Box>
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenLog(false)}>Cancel</Button>
          <Button onClick={handleSaveLog} variant="contained">
            Save Log
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}