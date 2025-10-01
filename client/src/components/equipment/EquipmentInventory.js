import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Card,
  CardContent,
  CardActions,
  Chip,
  Tooltip,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  QrCode2 as QrCodeIcon,
  FilterList as FilterIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getEquipment, createEquipment, updateEquipment, deleteEquipment } from '../../api/equipment';

const statusColors = {
  available: 'success',
  in_use: 'primary',
  maintenance: 'warning',
  out_of_order: 'error'
};

const EquipmentInventory = ({ onAlert }) => {
  const [filters, setFilters] = useState({
    category: '',
    status: '',
    location: ''
  });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingEquipment, setEditingEquipment] = useState(null);
  const [showFilters, setShowFilters] = useState(false);
  const queryClient = useQueryClient();

  // Fetch equipment data
  const { data: equipment, isLoading } = useQuery(
    ['equipment', filters],
    () => getEquipment(filters)
  );

  // Mutations
  const createMutation = useMutation(createEquipment, {
    onSuccess: () => {
      queryClient.invalidateQueries('equipment');
      onAlert('Equipment added successfully');
      handleCloseDialog();
    },
    onError: (error) => {
      onAlert(error.message, 'error');
    }
  });

  const updateMutation = useMutation(updateEquipment, {
    onSuccess: () => {
      queryClient.invalidateQueries('equipment');
      onAlert('Equipment updated successfully');
      handleCloseDialog();
    },
    onError: (error) => {
      onAlert(error.message, 'error');
    }
  });

  const deleteMutation = useMutation(deleteEquipment, {
    onSuccess: () => {
      queryClient.invalidateQueries('equipment');
      onAlert('Equipment deleted successfully');
    },
    onError: (error) => {
      onAlert(error.message, 'error');
    }
  });

  const handleAddEquipment = () => {
    setEditingEquipment(null);
    setDialogOpen(true);
  };

  const handleEditEquipment = (equipment) => {
    setEditingEquipment(equipment);
    setDialogOpen(true);
  };

  const handleDeleteEquipment = async (id) => {
    if (window.confirm('Are you sure you want to delete this equipment?')) {
      await deleteMutation.mutateAsync(id);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      name: formData.get('name'),
      description: formData.get('description'),
      category_id: parseInt(formData.get('category')),
      model_number: formData.get('model_number'),
      serial_number: formData.get('serial_number'),
      location: formData.get('location'),
      max_usage_hours: parseFloat(formData.get('max_usage_hours'))
    };

    if (editingEquipment) {
      await updateMutation.mutateAsync({ id: editingEquipment.id, ...data });
    } else {
      await createMutation.mutateAsync(data);
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingEquipment(null);
  };

  const handleFilterChange = (field) => (event) => {
    setFilters((prev) => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6" component="h2">
          Equipment Inventory
        </Typography>
        <Box>
          <IconButton onClick={() => setShowFilters(!showFilters)} sx={{ mr: 1 }}>
            <FilterIcon />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddEquipment}
          >
            Add Equipment
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      {showFilters && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={filters.category}
                  onChange={handleFilterChange('category')}
                  label="Category"
                >
                  <MenuItem value="">All</MenuItem>
                  {/* Add categories dynamically */}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filters.status}
                  onChange={handleFilterChange('status')}
                  label="Status"
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="available">Available</MenuItem>
                  <MenuItem value="in_use">In Use</MenuItem>
                  <MenuItem value="maintenance">Maintenance</MenuItem>
                  <MenuItem value="out_of_order">Out of Order</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Location"
                value={filters.location}
                onChange={handleFilterChange('location')}
              />
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Equipment Grid */}
      <Grid container spacing={3}>
        {equipment?.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                  <Typography variant="h6" component="h3" gutterBottom>
                    {item.name}
                  </Typography>
                  <Chip
                    label={item.status}
                    color={statusColors[item.status]}
                    size="small"
                  />
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  {item.category.name}
                </Typography>
                <Typography variant="body2" paragraph>
                  {item.description}
                </Typography>
                <Typography variant="body2">
                  Location: {item.location}
                </Typography>
                <Typography variant="body2">
                  Usage: {item.current_usage_hours}/{item.max_usage_hours} hours
                </Typography>
              </CardContent>
              <CardActions>
                <Tooltip title="Edit">
                  <IconButton onClick={() => handleEditEquipment(item)}>
                    <EditIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Delete">
                  <IconButton onClick={() => handleDeleteEquipment(item.id)}>
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="View QR Code">
                  <IconButton>
                    <QrCodeIcon />
                  </IconButton>
                </Tooltip>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {editingEquipment ? 'Edit Equipment' : 'Add New Equipment'}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Name"
                  name="name"
                  required
                  defaultValue={editingEquipment?.name}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  multiline
                  rows={3}
                  defaultValue={editingEquipment?.description}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Category</InputLabel>
                  <Select
                    name="category"
                    label="Category"
                    required
                    defaultValue={editingEquipment?.category_id || ''}
                  >
                    {/* Add categories dynamically */}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Location"
                  name="location"
                  defaultValue={editingEquipment?.location}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Model Number"
                  name="model_number"
                  defaultValue={editingEquipment?.model_number}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Serial Number"
                  name="serial_number"
                  required
                  defaultValue={editingEquipment?.serial_number}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Maximum Usage Hours"
                  name="max_usage_hours"
                  type="number"
                  defaultValue={editingEquipment?.max_usage_hours}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              disabled={createMutation.isLoading || updateMutation.isLoading}
            >
              {createMutation.isLoading || updateMutation.isLoading ? (
                <CircularProgress size={24} />
              ) : (
                editingEquipment ? 'Update' : 'Add'
              )}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default EquipmentInventory;