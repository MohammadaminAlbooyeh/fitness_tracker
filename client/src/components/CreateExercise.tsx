import { useState } from 'react';
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
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { createExercise } from '../api/api';

const muscleGroups = [
  'Chest',
  'Back',
  'Legs',
  'Shoulders',
  'Arms',
  'Core',
  'Full Body',
];

const categories = [
  'Strength',
  'Cardio',
  'Flexibility',
  'Balance',
  'Plyometrics',
];

export default function CreateExercise() {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    target_muscle: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name as string]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createExercise(formData);
      // Reset form
      setFormData({
        name: '',
        description: '',
        category: '',
        target_muscle: '',
      });
    } catch (error) {
      console.error('Failed to create exercise:', error);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Create New Exercise
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                margin="normal"
                required
                fullWidth
                id="name"
                name="name"
                label="Exercise Name"
                value={formData.name}
                onChange={handleChange}
              />
              <TextField
                margin="normal"
                fullWidth
                id="description"
                name="description"
                label="Description"
                multiline
                rows={4}
                value={formData.description}
                onChange={handleChange}
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Category</InputLabel>
                <Select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  required
                >
                  {categories.map((category) => (
                    <MenuItem key={category} value={category.toLowerCase()}>
                      {category}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl fullWidth margin="normal">
                <InputLabel>Target Muscle Group</InputLabel>
                <Select
                  name="target_muscle"
                  value={formData.target_muscle}
                  onChange={handleChange}
                  required
                >
                  {muscleGroups.map((muscle) => (
                    <MenuItem key={muscle} value={muscle.toLowerCase()}>
                      {muscle}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                sx={{ mt: 3 }}
              >
                Create Exercise
              </Button>
            </form>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 4 }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Exercise Guidelines
            </Typography>
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Categories
                </Typography>
                <Typography variant="body2">
                  • Strength: Weight training exercises<br />
                  • Cardio: Aerobic exercises<br />
                  • Flexibility: Stretching exercises<br />
                  • Balance: Stability exercises<br />
                  • Plyometrics: Explosive movement exercises
                </Typography>
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Tips for Good Form
                </Typography>
                <Typography variant="body2">
                  • Provide clear, step-by-step instructions<br />
                  • Include important form cues<br />
                  • Mention common mistakes to avoid<br />
                  • Add variations or modifications if applicable<br />
                  • Specify equipment needed
                </Typography>
              </CardContent>
            </Card>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}