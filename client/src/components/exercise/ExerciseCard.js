import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Chip,
  Stack,
  IconButton,
  Collapse,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  FitnessCenter,
  AccessTime,
  ExpandMore as ExpandMoreIcon,
  PlayCircleOutline as PlayIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

const ExerciseCard = ({ exercise, onLogProgress }) => {
  const [expanded, setExpanded] = useState(false);
  const [videoOpen, setVideoOpen] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
    <>
      <Card sx={{ maxWidth: 345, height: '100%', display: 'flex', flexDirection: 'column' }}>
        {exercise.thumbnail_url && (
          <CardMedia
            component="img"
            height="140"
            image={exercise.thumbnail_url}
            alt={exercise.name}
          />
        )}
        
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography variant="h6" gutterBottom>
            {exercise.name}
          </Typography>
          
          <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
            <Chip 
              size="small" 
              icon={<FitnessCenter />} 
              label={exercise.category} 
              color="primary" 
              variant="outlined"
            />
            <Chip 
              size="small" 
              label={exercise.difficulty_level} 
              color="secondary" 
              variant="outlined"
            />
          </Stack>

          <Typography variant="body2" color="text.secondary" noWrap>
            {exercise.description}
          </Typography>

          {exercise.video_url && (
            <IconButton 
              color="primary" 
              onClick={() => setVideoOpen(true)}
              sx={{ mt: 1 }}
            >
              <PlayIcon />
            </IconButton>
          )}
          
          <Button 
            variant="contained" 
            color="primary" 
            fullWidth 
            sx={{ mt: 2 }}
            onClick={() => onLogProgress(exercise)}
          >
            Log Progress
          </Button>
        </CardContent>

        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Typography paragraph variant="h6">Instructions:</Typography>
            <Typography paragraph>{exercise.instructions}</Typography>

            {exercise.form_tips && (
              <>
                <Typography variant="h6">Form Tips:</Typography>
                <Typography paragraph>{exercise.form_tips}</Typography>
              </>
            )}

            {exercise.safety_warnings && (
              <>
                <Typography variant="h6" color="error">Safety Warnings:</Typography>
                <Typography paragraph>{exercise.safety_warnings}</Typography>
              </>
            )}

            {exercise.equipment.length > 0 && (
              <>
                <Typography variant="h6">Required Equipment:</Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ mt: 1 }}>
                  {exercise.equipment.map((eq) => (
                    <Chip 
                      key={eq.id}
                      label={eq.name}
                      size="small"
                      sx={{ m: 0.5 }}
                    />
                  ))}
                </Stack>
              </>
            )}
          </CardContent>
        </Collapse>
      </Card>

      <Dialog
        open={videoOpen}
        onClose={() => setVideoOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{exercise.name} - Demonstration</DialogTitle>
        <DialogContent>
          <video
            controls
            width="100%"
            src={exercise.video_url}
            style={{ maxHeight: '70vh' }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setVideoOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ExerciseCard;