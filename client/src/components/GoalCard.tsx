import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Box,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import { MoreVert as MoreVertIcon } from '@mui/icons-material';

interface Goal {
  id: number;
  metric: string;
  target: number;
  deadline: string;
  current_value: number;
  progress: number;
}

interface GoalCardProps {
  goal: Goal;
  onEdit: () => void;
  onDelete: () => void;
}

export const GoalCard: React.FC<GoalCardProps> = ({ goal, onEdit, onDelete }) => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    handleMenuClose();
    onEdit();
  };

  const handleDelete = () => {
    handleMenuClose();
    onDelete();
  };

  const daysRemaining = Math.ceil(
    (new Date(goal.deadline).getTime() - new Date().getTime()) / (1000 * 3600 * 24)
  );

  const getProgressColor = () => {
    if (goal.progress >= 100) return 'success';
    if (daysRemaining < 0) return 'error';
    if (goal.progress >= 50) return 'primary';
    return 'warning';
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" gutterBottom>
            {goal.metric}
          </Typography>
          <IconButton size="small" onClick={handleMenuOpen}>
            <MoreVertIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleEdit}>Edit</MenuItem>
            <MenuItem onClick={handleDelete}>Delete</MenuItem>
          </Menu>
        </Box>

        <Box sx={{ mt: 2, mb: 1 }}>
          <LinearProgress
            variant="determinate"
            value={Math.min(goal.progress, 100)}
            color={getProgressColor()}
          />
        </Box>

        <Box display="flex" justifyContent="space-between" mt={1}>
          <Typography variant="body2" color="text.secondary">
            Current: {goal.current_value.toFixed(1)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Target: {goal.target.toFixed(1)}
          </Typography>
        </Box>

        <Typography
          variant="body2"
          color={daysRemaining < 0 ? 'error' : 'text.secondary'}
          sx={{ mt: 1 }}
        >
          {daysRemaining < 0
            ? `Overdue by ${Math.abs(daysRemaining)} days`
            : `${daysRemaining} days remaining`}
        </Typography>
      </CardContent>
    </Card>
  );
};