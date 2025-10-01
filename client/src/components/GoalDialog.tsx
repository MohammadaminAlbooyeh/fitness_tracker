import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  MenuItem,
} from '@mui/material';

interface GoalDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (goal: {
    metric: string;
    target: number;
    deadline: string;
  }) => void;
  availableMetrics: string[];
  initialData?: {
    metric: string;
    target: number;
    deadline: string;
  };
}

export const GoalDialog: React.FC<GoalDialogProps> = ({
  open,
  onClose,
  onSubmit,
  availableMetrics,
  initialData,
}) => {
  const [formData, setFormData] = React.useState(
    initialData || {
      metric: '',
      target: '',
      deadline: '',
    }
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...formData,
      target: Number(formData.target),
    });
  };

  const handleChange = (field: string) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <DialogTitle>
          {initialData ? 'Edit Goal' : 'Set New Goal'}
        </DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Metric"
            value={formData.metric}
            onChange={handleChange('metric')}
            margin="normal"
            required
          >
            {availableMetrics.map((metric) => (
              <MenuItem key={metric} value={metric}>
                {metric}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            fullWidth
            label="Target Value"
            type="number"
            value={formData.target}
            onChange={handleChange('target')}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Target Date"
            type="date"
            value={formData.deadline}
            onChange={handleChange('deadline')}
            margin="normal"
            required
            InputLabelProps={{
              shrink: true,
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" color="primary">
            Save Goal
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};