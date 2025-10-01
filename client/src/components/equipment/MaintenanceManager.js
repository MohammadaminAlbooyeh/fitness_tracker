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
  List,
  ListItem,
  ListItemText,
  ListItemSecondary,
  Divider,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  Build as MaintenanceIcon,
  Schedule as ScheduleIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  getMaintenanceRecords,
  createMaintenanceRecord,
  getMaintenanceAlerts
} from '../../api/equipment';
import { format } from 'date-fns';

const MaintenanceManager = ({ onAlert }) => {
  const [selectedEquipment, setSelectedEquipment] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const queryClient = useQueryClient();

  // Fetch maintenance data
  const { data: maintenanceRecords, isLoading: isLoadingRecords } = useQuery(
    ['maintenanceRecords', selectedEquipment?.id],
    () => selectedEquipment ? getMaintenanceRecords(selectedEquipment.id) : null
  );

  const { data: alerts, isLoading: isLoadingAlerts } = useQuery(
    'maintenanceAlerts',
    getMaintenanceAlerts
  );

  // Mutations
  const createMutation = useMutation(createMaintenanceRecord, {
    onSuccess: () => {
      queryClient.invalidateQueries('maintenanceRecords');
      queryClient.invalidateQueries('maintenanceAlerts');
      onAlert('Maintenance record added successfully');
      handleCloseDialog();
    },
    onError: (error) => {
      onAlert(error.message, 'error');
    }
  });

  const handleAddMaintenance = (equipment) => {
    setSelectedEquipment(equipment);
    setDialogOpen(true);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      equipment_id: selectedEquipment.id,
      maintenance_type: formData.get('maintenance_type'),
      performed_by: formData.get('performed_by'),
      description: formData.get('description'),
      cost: parseFloat(formData.get('cost')),
      next_maintenance_date: formData.get('next_maintenance_date'),
      parts_replaced: formData.get('parts_replaced')
    };

    await createMutation.mutateAsync(data);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedEquipment(null);
  };

  if (isLoadingAlerts) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      {/* Maintenance Alerts */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Maintenance Alerts
        </Typography>
        {alerts?.length === 0 ? (
          <Alert severity="success">No maintenance alerts at this time</Alert>
        ) : (
          <List>
            {alerts?.map((alert) => (
              <React.Fragment key={`${alert.equipment_id}-${alert.alert_type}`}>
                <ListItem>
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center">
                        <WarningIcon color="warning" sx={{ mr: 1 }} />
                        {alert.equipment_name}
                      </Box>
                    }
                    secondary={alert.message}
                  />
                  <Button
                    variant="outlined"
                    startIcon={<MaintenanceIcon />}
                    onClick={() => handleAddMaintenance({
                      id: alert.equipment_id,
                      name: alert.equipment_name
                    })}
                  >
                    Schedule
                  </Button>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        )}
      </Paper>

      {/* Maintenance History */}
      {selectedEquipment && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Maintenance History - {selectedEquipment.name}
          </Typography>
          {isLoadingRecords ? (
            <CircularProgress />
          ) : (
            <List>
              {maintenanceRecords?.map((record) => (
                <React.Fragment key={record.id}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center">
                          <MaintenanceIcon sx={{ mr: 1 }} />
                          {record.maintenance_type}
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2">
                            {format(new Date(record.date_performed), 'PPp')}
                          </Typography>
                          <Typography variant="body2">
                            {record.description}
                          </Typography>
                          {record.parts_replaced && (
                            <Typography variant="body2">
                              Parts replaced: {record.parts_replaced}
                            </Typography>
                          )}
                        </>
                      }
                    />
                    <Box>
                      <Typography variant="body2" color="textSecondary">
                        Cost: ${record.cost}
                      </Typography>
                      {record.next_maintenance_date && (
                        <Chip
                          icon={<ScheduleIcon />}
                          label={`Next: ${format(new Date(record.next_maintenance_date), 'PP')}`}
                          size="small"
                          color="primary"
                        />
                      )}
                    </Box>
                  </ListItem>
                  <Divider />
                </React.Fragment>
              ))}
            </List>
          )}
        </Paper>
      )}

      {/* Add Maintenance Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            Add Maintenance Record - {selectedEquipment?.name}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <FormControl fullWidth required>
                  <InputLabel>Maintenance Type</InputLabel>
                  <Select
                    name="maintenance_type"
                    label="Maintenance Type"
                    defaultValue=""
                  >
                    <MenuItem value="routine">Routine</MenuItem>
                    <MenuItem value="repair">Repair</MenuItem>
                    <MenuItem value="replacement">Replacement</MenuItem>
                    <MenuItem value="inspection">Inspection</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Performed By"
                  name="performed_by"
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  multiline
                  rows={3}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Cost"
                  name="cost"
                  type="number"
                  inputProps={{ step: "0.01" }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <DatePicker
                  label="Next Maintenance Date"
                  name="next_maintenance_date"
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Parts Replaced"
                  name="parts_replaced"
                  multiline
                  rows={2}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              disabled={createMutation.isLoading}
            >
              {createMutation.isLoading ? (
                <CircularProgress size={24} />
              ) : (
                'Add Record'
              )}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default MaintenanceManager;