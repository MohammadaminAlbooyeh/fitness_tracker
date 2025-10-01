import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { createWorkout, getExercises } from '../api/api';

interface Exercise {
  id: number;
  name: string;
  category: string;
}

interface WorkoutExercise {
  exercise_id: number;
  sets: number;
  reps: number;
  weight?: number;
  duration?: number;
}

export default function CreateWorkout() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [exercises, setExercises] = useState<WorkoutExercise[]>([]);
  const [availableExercises, setAvailableExercises] = useState<Exercise[]>([]);

  const addExercise = () => {
    setExercises([...exercises, {
      exercise_id: 0,
      sets: 3,
      reps: 10,
    }]);
  };

  const removeExercise = (index: number) => {
    setExercises(exercises.filter((_, i) => i !== index));
  };

  const updateExercise = (index: number, field: keyof WorkoutExercise, value: number) => {
    const updatedExercises = [...exercises];
    updatedExercises[index] = {
      ...updatedExercises[index],
      [field]: value,
    };
    setExercises(updatedExercises);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createWorkout({
        name,
        description,
        exercises,
      });
      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to create workout:', error);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Create New Workout
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="name"
            label="Workout Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <TextField
            margin="normal"
            fullWidth
            id="description"
            label="Description"
            multiline
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
            Exercises
          </Typography>

          {exercises.map((exercise, index) => (
            <Box key={index} sx={{ mb: 2, display: 'flex', gap: 2 }}>
              <FormControl fullWidth>
                <InputLabel>Exercise</InputLabel>
                <Select
                  value={exercise.exercise_id}
                  onChange={(e) => updateExercise(index, 'exercise_id', Number(e.target.value))}
                >
                  {availableExercises.map((ex) => (
                    <MenuItem key={ex.id} value={ex.id}>
                      {ex.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <TextField
                label="Sets"
                type="number"
                value={exercise.sets}
                onChange={(e) => updateExercise(index, 'sets', Number(e.target.value))}
                sx={{ width: 100 }}
              />
              <TextField
                label="Reps"
                type="number"
                value={exercise.reps}
                onChange={(e) => updateExercise(index, 'reps', Number(e.target.value))}
                sx={{ width: 100 }}
              />
              <IconButton
                onClick={() => removeExercise(index)}
                color="error"
              >
                <DeleteIcon />
              </IconButton>
            </Box>
          ))}

          <Button
            variant="outlined"
            onClick={addExercise}
            sx={{ mt: 2, mb: 4 }}
          >
            Add Exercise
          </Button>

          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/dashboard')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={exercises.length === 0}
            >
              Create Workout
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
}