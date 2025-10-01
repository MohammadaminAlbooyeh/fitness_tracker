import React from 'react';
import {
  Card,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
  useTheme
} from '@mui/material';
import {
  AccessTime as TimeIcon,
  Room as LocationIcon,
  Repeat as RecurringIcon,
  FitnessCenter as WorkoutIcon,
  Group as ClassIcon,
  Assessment as AssessmentIcon,
  SelfImprovement as RecoveryIcon,
  Person as ConsultationIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const eventTypeIcons = {
  workout: WorkoutIcon,
  class: ClassIcon,
  assessment: AssessmentIcon,
  recovery: RecoveryIcon,
  consultation: ConsultationIcon
};

const eventTypeColors = {
  workout: 'primary',
  class: 'secondary',
  assessment: 'info',
  recovery: 'success',
  consultation: 'warning'
};

const EventCard = ({ event, onClick }) => {
  const theme = useTheme();
  const Icon = eventTypeIcons[event.event_type] || WorkoutIcon;

  return (
    <Card
      sx={{
        p: 1,
        mb: 1,
        cursor: 'pointer',
        '&:hover': {
          bgcolor: theme.palette.action.hover
        },
        borderLeft: 4,
        borderColor: theme.palette[eventTypeColors[event.event_type]].main
      }}
      onClick={onClick}
    >
      <Box display="flex" alignItems="center" gap={1}>
        <Icon
          color={eventTypeColors[event.event_type]}
          sx={{ fontSize: 20 }}
        />
        <Typography variant="subtitle2" noWrap>
          {event.title}
        </Typography>
      </Box>

      <Box display="flex" alignItems="center" gap={1} mt={0.5}>
        <TimeIcon sx={{ fontSize: 16 }} color="action" />
        <Typography variant="caption" color="textSecondary">
          {format(new Date(event.start_time), 'HH:mm')} -
          {format(new Date(event.end_time), 'HH:mm')}
        </Typography>
      </Box>

      {event.location && (
        <Box display="flex" alignItems="center" gap={1}>
          <LocationIcon sx={{ fontSize: 16 }} color="action" />
          <Typography variant="caption" color="textSecondary" noWrap>
            {event.location}
          </Typography>
        </Box>
      )}

      {event.recurrence_pattern && (
        <Tooltip title="Recurring event">
          <IconButton size="small" sx={{ opacity: 0.7 }}>
            <RecurringIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      )}

      {event.metadata?.intensity_level && (
        <Chip
          label={event.metadata.intensity_level}
          size="small"
          color={
            event.metadata.intensity_level === 'high'
              ? 'error'
              : event.metadata.intensity_level === 'medium'
              ? 'warning'
              : 'success'
          }
          sx={{ ml: 1 }}
        />
      )}
    </Card>
  );
};

export default EventCard;