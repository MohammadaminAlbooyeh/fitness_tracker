import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Box,
  TextField,
  Button,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CalendarToday as CalendarIcon,
  RestaurantMenu as MenuIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format, addDays, startOfWeek } from 'date-fns';
import {
  fetchMealPlan,
  createMealPlan,
  updateMealPlan,
  deleteMealPlan,
  fetchRecipes
} from '../../api/nutrition';

const MEAL_TYPES = ['breakfast', 'lunch', 'dinner', 'snack'];
const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const MealPlanForm = ({ initialData, onSubmit, onClose }) => {
  const [formData, setFormData] = useState(initialData || {
    name: '',
    start_date: format(startOfWeek(new Date()), 'yyyy-MM-dd'),
    end_date: format(addDays(startOfWeek(new Date()), 6), 'yyyy-MM-dd'),
    daily_calories: 2000,
    macros: { protein: 30, carbs: 40, fat: 30 },
    planned_meals: DAYS.map(day => MEAL_TYPES.map(type => ({
      day_of_week: DAYS.indexOf(day),
      meal_type: type,
      foods: []
    }))).flat()
  });

  const { data: recipes } = useQuery('recipes', fetchRecipes);

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleMacroChange = (macro) => (event) => {
    setFormData(prev => ({
      ...prev,
      macros: {
        ...prev.macros,
        [macro]: Number(event.target.value)
      }
    }));
  };

  const updateMealPlan = (dayIndex, mealType, foods) => {
    setFormData(prev => ({
      ...prev,
      planned_meals: prev.planned_meals.map(meal => 
        meal.day_of_week === dayIndex && meal.meal_type === mealType
          ? { ...meal, foods }
          : meal
      )
    }));
  };

  return (
    <Dialog open={true} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {initialData ? 'Edit Meal Plan' : 'Create New Meal Plan'}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Plan Name"
              value={formData.name}
              onChange={handleChange('name')}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="date"
              label="Start Date"
              value={formData.start_date}
              onChange={handleChange('start_date')}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="date"
              label="End Date"
              value={formData.end_date}
              onChange={handleChange('end_date')}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              type="number"
              label="Daily Calories Target"
              value={formData.daily_calories}
              onChange={handleChange('daily_calories')}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle1" gutterBottom>
              Macro Split (%)
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  type="number"
                  label="Protein"
                  value={formData.macros.protein}
                  onChange={handleMacroChange('protein')}
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  type="number"
                  label="Carbs"
                  value={formData.macros.carbs}
                  onChange={handleMacroChange('carbs')}
                />
              </Grid>
              <Grid item xs={4}>
                <TextField
                  fullWidth
                  type="number"
                  label="Fat"
                  value={formData.macros.fat}
                  onChange={handleMacroChange('fat')}
                />
              </Grid>
            </Grid>
          </Grid>

          <Grid item xs={12}>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Day</TableCell>
                    {MEAL_TYPES.map(type => (
                      <TableCell key={type}>
                        {type.charAt(0).toUpperCase() + type.slice(1)}
                      </TableCell>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {DAYS.map((day, dayIndex) => (
                    <TableRow key={day}>
                      <TableCell>{day}</TableCell>
                      {MEAL_TYPES.map(type => {
                        const meal = formData.planned_meals.find(
                          m => m.day_of_week === dayIndex && m.meal_type === type
                        );
                        return (
                          <TableCell key={`${day}-${type}`}>
                            <TextField
                              select
                              fullWidth
                              SelectProps={{ multiple: true }}
                              value={meal?.foods || []}
                              onChange={(e) => updateMealPlan(dayIndex, type, e.target.value)}
                            >
                              {recipes?.map(recipe => (
                                <option key={recipe.id} value={recipe.id}>
                                  {recipe.name}
                                </option>
                              ))}
                            </TextField>
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={() => onSubmit(formData)}
          variant="contained"
          color="primary"
        >
          {initialData ? 'Update Plan' : 'Create Plan'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const MealPlanning = () => {
  const queryClient = useQueryClient();
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'));

  const { data: mealPlan, isLoading } = useQuery(
    ['mealPlan', selectedDate],
    () => fetchMealPlan(selectedDate)
  );

  const createMutation = useMutation(createMealPlan, {
    onSuccess: () => {
      queryClient.invalidateQueries('mealPlan');
      setCreateDialogOpen(false);
    }
  });

  const updateMutation = useMutation(updateMealPlan, {
    onSuccess: () => {
      queryClient.invalidateQueries('mealPlan');
      setEditingPlan(null);
    }
  });

  const deleteMutation = useMutation(deleteMealPlan, {
    onSuccess: () => {
      queryClient.invalidateQueries('mealPlan');
    }
  });

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">
              Meal Planning
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setCreateDialogOpen(true)}
            >
              Create Meal Plan
            </Button>
          </Grid>

          <Grid item xs={12}>
            <TextField
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              sx={{ width: 200 }}
            />
          </Grid>

          {isLoading ? (
            <Grid item xs={12} textAlign="center">
              <CircularProgress />
            </Grid>
          ) : mealPlan ? (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                  <Typography variant="h5">
                    {mealPlan.name}
                  </Typography>
                  <Box>
                    <IconButton onClick={() => setEditingPlan(mealPlan)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => deleteMutation.mutate(mealPlan.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>

                <Box display="flex" gap={3} mb={3}>
                  <Typography variant="body1">
                    <CalendarIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    {format(new Date(mealPlan.start_date), 'MMM d')} - 
                    {format(new Date(mealPlan.end_date), 'MMM d, yyyy')}
                  </Typography>
                  <Typography variant="body1">
                    <MenuIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    {mealPlan.daily_calories} calories/day
                  </Typography>
                </Box>

                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Day</TableCell>
                        {MEAL_TYPES.map(type => (
                          <TableCell key={type}>
                            {type.charAt(0).toUpperCase() + type.slice(1)}
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {DAYS.map((day, index) => (
                        <TableRow key={day}>
                          <TableCell>{day}</TableCell>
                          {MEAL_TYPES.map(type => {
                            const meal = mealPlan.planned_meals.find(
                              m => m.day_of_week === index && m.meal_type === type
                            );
                            return (
                              <TableCell key={`${day}-${type}`}>
                                {meal?.foods.map(food => food.name).join(', ')}
                              </TableCell>
                            );
                          })}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>
          ) : (
            <Grid item xs={12}>
              <Typography>No meal plan found for this week</Typography>
            </Grid>
          )}
        </Grid>

        {createDialogOpen && (
          <MealPlanForm
            onSubmit={(data) => createMutation.mutate(data)}
            onClose={() => setCreateDialogOpen(false)}
          />
        )}

        {editingPlan && (
          <MealPlanForm
            initialData={editingPlan}
            onSubmit={(data) => updateMutation.mutate({ id: editingPlan.id, ...data })}
            onClose={() => setEditingPlan(null)}
          />
        )}
      </Box>
    </Container>
  );
};

export default MealPlanning;