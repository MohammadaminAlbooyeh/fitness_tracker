import React from 'react';
import { Card, CardContent, Typography, Grid, Chip, Button } from '@mui/material';
import { FitnessCenter, AccessTime, Star } from '@mui/icons-material';
import { formatDuration } from '../../utils/timeUtils';

const WorkoutTemplateCard = ({ template, onSelect }) => {
  return (
    <Card 
      sx={{ 
        cursor: 'pointer', 
        '&:hover': { boxShadow: 6 },
        height: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}
      onClick={() => onSelect(template)}
    >
      <CardContent sx={{ flex: 1 }}>
        <Typography variant="h6" gutterBottom>
          {template.name}
        </Typography>
        
        <Typography 
          variant="body2" 
          color="text.secondary" 
          sx={{ mb: 2 }}
          component="div"
        >
          {template.description}
        </Typography>

        <Grid container spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Grid item>
            <Chip
              icon={<FitnessCenter />}
              label={template.category}
              size="small"
              color="primary"
              variant="outlined"
            />
          </Grid>
          <Grid item>
            <Chip
              icon={<Star />}
              label={template.difficulty}
              size="small"
              color="secondary"
              variant="outlined"
            />
          </Grid>
          <Grid item>
            <Chip
              icon={<AccessTime />}
              label={formatDuration(template.estimated_duration)}
              size="small"
              variant="outlined"
            />
          </Grid>
        </Grid>

        <Typography variant="caption" color="text.secondary" component="div">
          {template.exercises?.length || 0} exercises
        </Typography>
      </CardContent>

      <Button 
        variant="contained" 
        color="primary"
        sx={{ m: 2 }}
        onClick={(e) => {
          e.stopPropagation();
          onSelect(template);
        }}
      >
        Schedule Workout
      </Button>
    </Card>
  );
};

export default WorkoutTemplateCard;