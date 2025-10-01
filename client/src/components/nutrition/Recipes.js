import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardMedia,
  Box,
  Button,
  TextField,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Autocomplete,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Timer as TimerIcon,
  Restaurant as RestaurantIcon,
  LocalDining as DiningIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import { 
  fetchRecipes,
  createRecipe,
  updateRecipe,
  deleteRecipe,
  searchFoods
} from '../../api/nutrition';

const RecipeForm = ({ initialData, onSubmit, onClose }) => {
  const [formData, setFormData] = useState(initialData || {
    name: '',
    description: '',
    ingredients: [],
    instructions: [''],
    prep_time: 0,
    cook_time: 0,
    servings: 1,
    tags: [],
  });

  const [newIngredient, setNewIngredient] = useState({
    food: null,
    amount: '',
    unit: 'g'
  });

  const [search, setSearch] = useState('');
  const { data: searchResults, isLoading: searchLoading } = useQuery(
    ['foodSearch', search],
    () => searchFoods(search),
    { enabled: search.length > 2 }
  );

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const addIngredient = () => {
    if (newIngredient.food && newIngredient.amount) {
      setFormData(prev => ({
        ...prev,
        ingredients: [...prev.ingredients, { ...newIngredient }]
      }));
      setNewIngredient({ food: null, amount: '', unit: 'g' });
    }
  };

  const removeIngredient = (index) => {
    setFormData(prev => ({
      ...prev,
      ingredients: prev.ingredients.filter((_, i) => i !== index)
    }));
  };

  const addInstruction = () => {
    setFormData(prev => ({
      ...prev,
      instructions: [...prev.instructions, '']
    }));
  };

  const updateInstruction = (index, value) => {
    setFormData(prev => ({
      ...prev,
      instructions: prev.instructions.map((inst, i) => 
        i === index ? value : inst
      )
    }));
  };

  const removeInstruction = (index) => {
    setFormData(prev => ({
      ...prev,
      instructions: prev.instructions.filter((_, i) => i !== index)
    }));
  };

  return (
    <Dialog open={true} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {initialData ? 'Edit Recipe' : 'Create New Recipe'}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Recipe Name"
              value={formData.name}
              onChange={handleChange('name')}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Description"
              value={formData.description}
              onChange={handleChange('description')}
            />
          </Grid>

          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Ingredients
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={6}>
                <Autocomplete
                  options={searchResults || []}
                  getOptionLabel={(option) => `${option.name} (${option.brand || 'Generic'})`}
                  loading={searchLoading}
                  value={newIngredient.food}
                  onChange={(_, newValue) => setNewIngredient(prev => ({
                    ...prev,
                    food: newValue
                  }))}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Search Ingredient"
                      onChange={(e) => setSearch(e.target.value)}
                      InputProps={{
                        ...params.InputProps,
                        endAdornment: (
                          <>
                            {searchLoading ? <CircularProgress color="inherit" size={20} /> : null}
                            {params.InputProps.endAdornment}
                          </>
                        ),
                      }}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={3}>
                <TextField
                  fullWidth
                  type="number"
                  label="Amount"
                  value={newIngredient.amount}
                  onChange={(e) => setNewIngredient(prev => ({
                    ...prev,
                    amount: e.target.value
                  }))}
                />
              </Grid>
              <Grid item xs={2}>
                <TextField
                  select
                  fullWidth
                  label="Unit"
                  value={newIngredient.unit}
                  onChange={(e) => setNewIngredient(prev => ({
                    ...prev,
                    unit: e.target.value
                  }))}
                >
                  {['g', 'ml', 'oz', 'cup', 'tbsp', 'tsp'].map(unit => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={1}>
                <IconButton onClick={addIngredient} color="primary">
                  <AddIcon />
                </IconButton>
              </Grid>
            </Grid>

            <List>
              {formData.ingredients.map((ingredient, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={ingredient.food.name}
                    secondary={`${ingredient.amount} ${ingredient.unit}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton edge="end" onClick={() => removeIngredient(index)}>
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Instructions
            </Typography>
            {formData.instructions.map((instruction, index) => (
              <Box key={index} sx={{ mb: 2, display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  multiline
                  label={`Step ${index + 1}`}
                  value={instruction}
                  onChange={(e) => updateInstruction(index, e.target.value)}
                />
                <IconButton onClick={() => removeInstruction(index)}>
                  <DeleteIcon />
                </IconButton>
              </Box>
            ))}
            <Button
              startIcon={<AddIcon />}
              onClick={addInstruction}
              sx={{ mt: 1 }}
            >
              Add Step
            </Button>
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="number"
              label="Prep Time (minutes)"
              value={formData.prep_time}
              onChange={handleChange('prep_time')}
            />
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="number"
              label="Cook Time (minutes)"
              value={formData.cook_time}
              onChange={handleChange('cook_time')}
            />
          </Grid>

          <Grid item xs={12} sm={4}>
            <TextField
              fullWidth
              type="number"
              label="Servings"
              value={formData.servings}
              onChange={handleChange('servings')}
            />
          </Grid>

          <Grid item xs={12}>
            <Autocomplete
              multiple
              freeSolo
              options={[]}
              value={formData.tags}
              onChange={(_, newValue) => setFormData(prev => ({
                ...prev,
                tags: newValue
              }))}
              renderTags={(value, getTagProps) =>
                value.map((option, index) => (
                  <Chip
                    label={option}
                    {...getTagProps({ index })}
                  />
                ))
              }
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Tags"
                  placeholder="Add tags"
                />
              )}
            />
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
          {initialData ? 'Update Recipe' : 'Create Recipe'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const Recipes = () => {
  const queryClient = useQueryClient();
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editingRecipe, setEditingRecipe] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const { data: recipes, isLoading } = useQuery('recipes', fetchRecipes);

  const createMutation = useMutation(createRecipe, {
    onSuccess: () => {
      queryClient.invalidateQueries('recipes');
      setCreateDialogOpen(false);
    }
  });

  const updateMutation = useMutation(updateRecipe, {
    onSuccess: () => {
      queryClient.invalidateQueries('recipes');
      setEditingRecipe(null);
    }
  });

  const deleteMutation = useMutation(deleteRecipe, {
    onSuccess: () => {
      queryClient.invalidateQueries('recipes');
    }
  });

  const filteredRecipes = recipes?.filter(recipe =>
    recipe.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    recipe.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">
              Recipes
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setCreateDialogOpen(true)}
            >
              Create Recipe
            </Button>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              placeholder="Search recipes by name or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              sx={{ mb: 3 }}
            />
          </Grid>

          {isLoading ? (
            <Grid item xs={12}>
              <CircularProgress />
            </Grid>
          ) : (
            <Grid container spacing={3}>
              {filteredRecipes?.map((recipe) => (
                <Grid item xs={12} sm={6} md={4} key={recipe.id}>
                  <Card>
                    {recipe.image_url && (
                      <CardMedia
                        component="img"
                        height="200"
                        image={recipe.image_url}
                        alt={recipe.name}
                      />
                    )}
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {recipe.name}
                      </Typography>
                      
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {recipe.description}
                      </Typography>

                      <Box display="flex" gap={2} mb={2}>
                        <Box display="flex" alignItems="center">
                          <TimerIcon sx={{ mr: 0.5, fontSize: 16 }} />
                          <Typography variant="body2" color="text.secondary">
                            {recipe.prep_time + recipe.cook_time} min
                          </Typography>
                        </Box>
                        <Box display="flex" alignItems="center">
                          <RestaurantIcon sx={{ mr: 0.5, fontSize: 16 }} />
                          <Typography variant="body2" color="text.secondary">
                            {recipe.servings} servings
                          </Typography>
                        </Box>
                      </Box>

                      <Box display="flex" gap={1} flexWrap="wrap" mb={2}>
                        {recipe.tags.map((tag, index) => (
                          <Chip
                            key={index}
                            label={tag}
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        ))}
                      </Box>

                      <Box display="flex" justifyContent="flex-end" gap={1}>
                        <IconButton
                          onClick={() => setEditingRecipe(recipe)}
                          size="small"
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          onClick={() => deleteMutation.mutate(recipe.id)}
                          size="small"
                          color="error"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </Grid>

        {createDialogOpen && (
          <RecipeForm
            onSubmit={(data) => createMutation.mutate(data)}
            onClose={() => setCreateDialogOpen(false)}
          />
        )}

        {editingRecipe && (
          <RecipeForm
            initialData={editingRecipe}
            onSubmit={(data) => updateMutation.mutate({ id: editingRecipe.id, ...data })}
            onClose={() => setEditingRecipe(null)}
          />
        )}
      </Box>
    </Container>
  );
};

export default Recipes;