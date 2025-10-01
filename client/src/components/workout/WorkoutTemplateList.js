import React, { useState, useEffect } from 'react';
import { 
  Grid, 
  Container, 
  Typography, 
  TextField, 
  MenuItem, 
  FormControlLabel,
  Switch,
  Box
} from '@mui/material';
import { useQuery } from 'react-query';
import WorkoutTemplateCard from './WorkoutTemplateCard';
import { fetchWorkoutTemplates } from '../../api/workout';

const CATEGORIES = ['strength', 'cardio', 'flexibility', 'hiit', 'other'];
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced'];

const WorkoutTemplateList = () => {
  const [filters, setFilters] = useState({
    category: '',
    difficulty: '',
    includePublic: true,
  });

  const { data: templates, isLoading, error } = useQuery(
    ['workoutTemplates', filters],
    () => fetchWorkoutTemplates(filters)
  );

  const handleFilterChange = (field) => (event) => {
    setFilters(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handlePublicToggle = (event) => {
    setFilters(prev => ({
      ...prev,
      includePublic: event.target.checked
    }));
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading templates: {error.message}</div>;

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Workout Templates
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={4}>
            <TextField
              select
              fullWidth
              label="Category"
              value={filters.category}
              onChange={handleFilterChange('category')}
            >
              <MenuItem value="">All Categories</MenuItem>
              {CATEGORIES.map(cat => (
                <MenuItem key={cat} value={cat}>
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <TextField
              select
              fullWidth
              label="Difficulty"
              value={filters.difficulty}
              onChange={handleFilterChange('difficulty')}
            >
              <MenuItem value="">All Difficulties</MenuItem>
              {DIFFICULTIES.map(diff => (
                <MenuItem key={diff} value={diff}>
                  {diff.charAt(0).toUpperCase() + diff.slice(1)}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={4}>
            <FormControlLabel
              control={
                <Switch
                  checked={filters.includePublic}
                  onChange={handlePublicToggle}
                  color="primary"
                />
              }
              label="Include Public Templates"
            />
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          {templates?.map((template) => (
            <Grid item xs={12} sm={6} md={4} key={template.id}>
              <WorkoutTemplateCard 
                template={template}
                onSelect={(template) => {
                  // Handle template selection
                  navigate(`/schedule/${template.id}`);
                }}
              />
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default WorkoutTemplateList;