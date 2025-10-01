import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  TextField,
  IconButton,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Autocomplete,
  CircularProgress,
  Card,
  CardContent
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  RestaurantMenu as MenuIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import {
  fetchDailyMeals,
  searchFoods,
  addMeal,
  updateMeal,
  deleteMeal
} from '../../api/nutrition';

const MacroCircle = ({ value, total, label, color }) => (
  <Box position="relative" display="inline-flex">
    <CircularProgress
      variant="determinate"
      value={(value / total) * 100}
      size={80}
      thickness={4}
      sx={{ color }}
    />
    <Box
      sx={{
        top: 0,
        left: 0,
        bottom: 0,
        right: 0,
        position: 'absolute',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="body2" component="div">
        {value}g
      </Typography>
    </Box>
  </Box>
);

const AddFoodDialog = ({ open, onClose, onAdd, mealType }) => {
  const [search, setSearch] = useState('');
  const [selectedFood, setSelectedFood] = useState(null);
  const [servings, setServings] = useState(1);

  const { data: searchResults, isLoading } = useQuery(
    ['foodSearch', search],
    () => searchFoods(search),
    { enabled: search.length > 2 }
  );

  const handleAdd = () => {
    if (selectedFood) {
      onAdd({
        food: selectedFood,
        servings,
        mealType
      });
      onClose();
      setSelectedFood(null);
      setServings(1);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Add Food to {mealType}</DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <Autocomplete
              options={searchResults || []}
              getOptionLabel={(option) => `${option.name} (${option.brand || 'Generic'})`}
              loading={isLoading}
              value={selectedFood}
              onChange={(_, newValue) => setSelectedFood(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Search Food"
                  onChange={(e) => setSearch(e.target.value)}
                  InputProps={{
                    ...params.InputProps,
                    endAdornment: (
                      <>
                        {isLoading ? <CircularProgress color="inherit" size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
            />
          </Grid>

          {selectedFood && (
            <>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="Servings"
                  value={servings}
                  onChange={(e) => setServings(Number(e.target.value))}
                  inputProps={{ min: 0.25, step: 0.25 }}
                />
              </Grid>
              <Grid item xs={12}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>
                      Nutrition per {servings} serving{servings !== 1 ? 's' : ''}:
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2">
                          Calories: {selectedFood.calories * servings}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2">
                          Protein: {selectedFood.protein * servings}g
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2">
                          Carbs: {selectedFood.carbs * servings}g
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2">
                          Fat: {selectedFood.fat * servings}g
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            </>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleAdd}
          variant="contained"
          disabled={!selectedFood}
        >
          Add Food
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const MealSection = ({ title, items, onAddFood, onDeleteFood }) => (
  <Paper sx={{ p: 3, mb: 3 }}>
    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
      <Typography variant="h6">{title}</Typography>
      <Button
        startIcon={<AddIcon />}
        onClick={() => onAddFood(title.toLowerCase())}
      >
        Add Food
      </Button>
    </Box>
    <List>
      {items.map((item) => (
        <React.Fragment key={item.id}>
          <ListItem>
            <ListItemText
              primary={item.food.name}
              secondary={`${item.servings} serving${item.servings !== 1 ? 's' : ''} • ${item.food.calories * item.servings} cal`}
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" onClick={() => onDeleteFood(item.id)}>
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
          <Divider />
        </React.Fragment>
      ))}
      {items.length === 0 && (
        <ListItem>
          <ListItemText
            secondary="No foods added yet"
            sx={{ textAlign: 'center' }}
          />
        </ListItem>
      )}
    </List>
  </Paper>
);

const DailyNutrition = () => {
  const queryClient = useQueryClient();
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [addFoodDialogOpen, setAddFoodDialogOpen] = useState(false);
  const [selectedMealType, setSelectedMealType] = useState(null);

  const { data: meals, isLoading } = useQuery(
    ['dailyMeals', selectedDate],
    () => fetchDailyMeals(selectedDate)
  );

  const addMealMutation = useMutation(addMeal, {
    onSuccess: () => {
      queryClient.invalidateQueries(['dailyMeals', selectedDate]);
    }
  });

  const deleteMealMutation = useMutation(deleteMeal, {
    onSuccess: () => {
      queryClient.invalidateQueries(['dailyMeals', selectedDate]);
    }
  });

  const handleAddFood = (mealType) => {
    setSelectedMealType(mealType);
    setAddFoodDialogOpen(true);
  };

  const handleSaveFood = (data) => {
    addMealMutation.mutate({
      date: selectedDate,
      mealType: data.mealType,
      foodId: data.food.id,
      servings: data.servings
    });
  };

  const totalNutrition = meals?.reduce(
    (acc, meal) => {
      meal.items.forEach((item) => {
        acc.calories += item.food.calories * item.servings;
        acc.protein += item.food.protein * item.servings;
        acc.carbs += item.food.carbs * item.servings;
        acc.fat += item.food.fat * item.servings;
      });
      return acc;
    },
    { calories: 0, protein: 0, carbs: 0, fat: 0 }
  ) || { calories: 0, protein: 0, carbs: 0, fat: 0 };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">
              Daily Nutrition
            </Typography>
            <TextField
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              sx={{ width: 200 }}
            />
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Daily Summary
              </Typography>
              <Grid container spacing={3} alignItems="center">
                <Grid item>
                  <Box textAlign="center" mb={1}>
                    <Typography variant="h4">
                      {Math.round(totalNutrition.calories)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      calories
                    </Typography>
                  </Box>
                </Grid>
                <Grid item>
                  <Divider orientation="vertical" />
                </Grid>
                <Grid item xs>
                  <Box display="flex" justifyContent="space-around">
                    <MacroCircle
                      value={Math.round(totalNutrition.protein)}
                      total={200}
                      label="Protein"
                      color="primary.main"
                    />
                    <MacroCircle
                      value={Math.round(totalNutrition.carbs)}
                      total={300}
                      label="Carbs"
                      color="secondary.main"
                    />
                    <MacroCircle
                      value={Math.round(totalNutrition.fat)}
                      total={100}
                      label="Fat"
                      color="warning.main"
                    />
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            {isLoading ? (
              <Typography>Loading meals...</Typography>
            ) : (
              <>
                <MealSection
                  title="Breakfast"
                  items={meals?.find(m => m.name === 'breakfast')?.items || []}
                  onAddFood={handleAddFood}
                  onDeleteFood={(id) => deleteMealMutation.mutate(id)}
                />
                <MealSection
                  title="Lunch"
                  items={meals?.find(m => m.name === 'lunch')?.items || []}
                  onAddFood={handleAddFood}
                  onDeleteFood={(id) => deleteMealMutation.mutate(id)}
                />
                <MealSection
                  title="Dinner"
                  items={meals?.find(m => m.name === 'dinner')?.items || []}
                  onAddFood={handleAddFood}
                  onDeleteFood={(id) => deleteMealMutation.mutate(id)}
                />
                <MealSection
                  title="Snacks"
                  items={meals?.find(m => m.name === 'snacks')?.items || []}
                  onAddFood={handleAddFood}
                  onDeleteFood={(id) => deleteMealMutation.mutate(id)}
                />
              </>
            )}
          </Grid>
        </Grid>

        <AddFoodDialog
          open={addFoodDialogOpen}
          onClose={() => setAddFoodDialogOpen(false)}
          onAdd={handleSaveFood}
          mealType={selectedMealType}
        />
      </Box>
    </Container>
  );
};

export default DailyNutrition;