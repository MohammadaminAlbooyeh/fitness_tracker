import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  TextField,
  MenuItem,
  Box,
  Button,
  FormControl,
  InputLabel,
  Select,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stack,
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Add as AddIcon } from '@mui/icons-material';
import ExerciseCard from './ExerciseCard';
import ProgressDialog from './ProgressDialog';
import CreateExerciseDialog from './CreateExerciseDialog';
import { fetchExercises, fetchEquipment, fetchMuscles } from '../../api/exercise';

const CATEGORIES = ['strength', 'cardio', 'flexibility', 'hiit', 'other'];
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced'];

const ExerciseLibrary = () => {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState({
    category: '',
    difficulty: '',
    equipment: '',
    muscle: '',
    searchQuery: '',
  });
  
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [progressDialogOpen, setProgressDialogOpen] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);

  // Fetch exercises with filters
  const { data: exercises, isLoading } = useQuery(
    ['exercises', filters],
    () => fetchExercises(filters)
  );

  // Fetch equipment and muscles for filters
  const { data: equipment } = useQuery('equipment', fetchEquipment);
  const { data: muscles } = useQuery('muscles', fetchMuscles);

  const handleFilterChange = (field) => (event) => {
    setFilters(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleLogProgress = (exercise) => {
    setSelectedExercise(exercise);
    setProgressDialogOpen(true);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3} alignItems="center" sx={{ mb: 4 }}>
          <Grid item xs={12} sm={8}>
            <Typography variant="h4" gutterBottom>
              Exercise Library
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4} sx={{ textAlign: 'right' }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={<AddIcon />}
              onClick={() => setCreateDialogOpen(true)}
            >
              Create Exercise
            </Button>
          </Grid>
        </Grid>

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              label="Search Exercises"
              value={filters.searchQuery}
              onChange={handleFilterChange('searchQuery')}
            />
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={filters.category}
                label="Category"
                onChange={handleFilterChange('category')}
              >
                <MenuItem value="">All Categories</MenuItem>
                {CATEGORIES.map(category => (
                  <MenuItem key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Difficulty</InputLabel>
              <Select
                value={filters.difficulty}
                label="Difficulty"
                onChange={handleFilterChange('difficulty')}
              >
                <MenuItem value="">All Difficulties</MenuItem>
                {DIFFICULTIES.map(diff => (
                  <MenuItem key={diff} value={diff}>
                    {diff.charAt(0).toUpperCase() + diff.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Equipment</InputLabel>
              <Select
                value={filters.equipment}
                label="Equipment"
                onChange={handleFilterChange('equipment')}
              >
                <MenuItem value="">All Equipment</MenuItem>
                {equipment?.map(eq => (
                  <MenuItem key={eq.id} value={eq.id}>
                    {eq.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        {isLoading ? (
          <Typography>Loading exercises...</Typography>
        ) : (
          <Grid container spacing={3}>
            {exercises?.map(exercise => (
              <Grid item xs={12} sm={6} md={4} key={exercise.id}>
                <ExerciseCard
                  exercise={exercise}
                  onLogProgress={handleLogProgress}
                />
              </Grid>
            ))}
          </Grid>
        )}
      </Box>

      {selectedExercise && (
        <ProgressDialog
          open={progressDialogOpen}
          onClose={() => {
            setProgressDialogOpen(false);
            setSelectedExercise(null);
          }}
          exercise={selectedExercise}
        />
      )}

      <CreateExerciseDialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        equipment={equipment}
        muscles={muscles}
        onSuccess={() => {
          queryClient.invalidateQueries('exercises');
          setCreateDialogOpen(false);
        }}
      />
    </Container>
  );
};

export default ExerciseLibrary;