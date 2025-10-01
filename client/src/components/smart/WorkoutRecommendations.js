import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondary,
  Divider
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { useQuery, useMutation } from 'react-query';
import { format } from 'date-fns';
import {
  getWorkoutRecommendations,
  updateRecommendationFeedback,
  generateNewRecommendation,
  getRecommendationInsights
} from '../../api/smart_features';

const RecommendationCard = ({ recommendation, onFeedback, onGenerateNew }) => {
  const [showInsights, setShowInsights] = useState(false);
  const { data: insights } = useQuery(
    ['recommendationInsights', recommendation.id],
    () => getRecommendationInsights(recommendation.id),
    {
      enabled: showInsights
    }
  );

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">
            {recommendation.name}
          </Typography>
          <Chip
            label={recommendation.type}
            color="primary"
            size="small"
          />
        </Box>

        <Typography variant="body2" color="text.secondary" paragraph>
          {recommendation.description}
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2">Duration</Typography>
            <Typography variant="body2">
              {recommendation.duration} minutes
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2">Intensity</Typography>
            <Typography variant="body2">
              {recommendation.intensity}
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2">Focus</Typography>
            <Typography variant="body2">
              {recommendation.focus}
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2">Difficulty</Typography>
            <Typography variant="body2">
              {recommendation.difficulty}
            </Typography>
          </Grid>
        </Grid>

        {showInsights && insights && (
          <Box mt={2}>
            <Typography variant="subtitle1" gutterBottom>
              Why this was recommended:
            </Typography>
            <List>
              {insights.factors.map((factor, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={factor.description}
                    secondary={`Impact: ${factor.weight}%`}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </CardContent>

      <CardActions>
        <IconButton
          onClick={() => onFeedback(recommendation.id, true)}
          color={recommendation.userFeedback === true ? 'primary' : 'default'}
        >
          <ThumbUpIcon />
        </IconButton>
        <IconButton
          onClick={() => onFeedback(recommendation.id, false)}
          color={recommendation.userFeedback === false ? 'primary' : 'default'}
        >
          <ThumbDownIcon />
        </IconButton>
        <IconButton onClick={() => setShowInsights(!showInsights)}>
          <InfoIcon />
        </IconButton>
        <Button
          size="small"
          startIcon={<RefreshIcon />}
          onClick={() => onGenerateNew(recommendation.id)}
          sx={{ ml: 'auto' }}
        >
          Generate Alternative
        </Button>
      </CardActions>
    </Card>
  );
};

const WorkoutRecommendations = () => {
  const [filters, setFilters] = useState({
    type: 'all',
    intensity: 'all',
    duration: 'all'
  });

  const { data: recommendations, isLoading, refetch } = useQuery(
    ['workoutRecommendations', filters],
    () => getWorkoutRecommendations(filters)
  );

  const updateFeedbackMutation = useMutation(
    ({ id, feedback }) => updateRecommendationFeedback(id, feedback),
    {
      onSuccess: () => refetch()
    }
  );

  const generateNewMutation = useMutation(
    (id) => generateNewRecommendation(id),
    {
      onSuccess: () => refetch()
    }
  );

  const handleFeedback = (id, isPositive) => {
    updateFeedbackMutation.mutate({ id, feedback: isPositive });
  };

  const handleGenerateNew = (id) => {
    generateNewMutation.mutate(id);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Smart Workout Recommendations
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Workout Type</InputLabel>
                <Select
                  value={filters.type}
                  label="Workout Type"
                  onChange={(e) => setFilters({ ...filters, type: e.target.value })}
                >
                  <MenuItem value="all">All Types</MenuItem>
                  <MenuItem value="strength">Strength</MenuItem>
                  <MenuItem value="cardio">Cardio</MenuItem>
                  <MenuItem value="hiit">HIIT</MenuItem>
                  <MenuItem value="flexibility">Flexibility</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Intensity</InputLabel>
                <Select
                  value={filters.intensity}
                  label="Intensity"
                  onChange={(e) => setFilters({ ...filters, intensity: e.target.value })}
                >
                  <MenuItem value="all">All Intensities</MenuItem>
                  <MenuItem value="low">Low</MenuItem>
                  <MenuItem value="moderate">Moderate</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={4}>
              <FormControl fullWidth size="small">
                <InputLabel>Duration</InputLabel>
                <Select
                  value={filters.duration}
                  label="Duration"
                  onChange={(e) => setFilters({ ...filters, duration: e.target.value })}
                >
                  <MenuItem value="all">All Durations</MenuItem>
                  <MenuItem value="15">15 minutes</MenuItem>
                  <MenuItem value="30">30 minutes</MenuItem>
                  <MenuItem value="45">45 minutes</MenuItem>
                  <MenuItem value="60">60 minutes</MenuItem>
                  <MenuItem value="90">90+ minutes</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Paper>

        <Grid container spacing={3}>
          {isLoading ? (
            <Grid item xs={12}>
              <Typography>Loading recommendations...</Typography>
            </Grid>
          ) : recommendations?.length === 0 ? (
            <Grid item xs={12}>
              <Typography>No recommendations found for the selected filters.</Typography>
            </Grid>
          ) : (
            recommendations?.map((recommendation) => (
              <Grid item xs={12} key={recommendation.id}>
                <RecommendationCard
                  recommendation={recommendation}
                  onFeedback={handleFeedback}
                  onGenerateNew={handleGenerateNew}
                />
              </Grid>
            ))
          )}
        </Grid>
      </Box>
    </Container>
  );
};

export default WorkoutRecommendations;