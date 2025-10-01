import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  CircularProgress,
  useTheme
} from '@mui/material';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Add as AddIcon
} from '@mui/icons-material';
import { format, addMonths, subMonths, startOfMonth, endOfMonth, eachDayOfInterval } from 'date-fns';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getEvents, createEvent } from '../../api/scheduling';
import EventDialog from './EventDialog';
import EventCard from './EventCard';

const Calendar = () => {
  const theme = useTheme();
  const queryClient = useQueryClient();
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [isEventDialogOpen, setIsEventDialogOpen] = useState(false);
  
  const startDate = startOfMonth(currentDate);
  const endDate = endOfMonth(currentDate);
  
  // Fetch events for the current month
  const { data: events, isLoading } = useQuery(
    ['events', format(startDate, 'yyyy-MM')],
    () => getEvents(startDate, endDate)
  );

  const createEventMutation = useMutation(createEvent, {
    onSuccess: () => {
      queryClient.invalidateQueries(['events', format(startDate, 'yyyy-MM')]);
      setIsEventDialogOpen(false);
    }
  });

  const handlePreviousMonth = () => {
    setCurrentDate(subMonths(currentDate, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(addMonths(currentDate, 1));
  };

  const handleDateClick = (date) => {
    setSelectedDate(date);
    setIsEventDialogOpen(true);
  };

  const handleCreateEvent = (eventData) => {
    createEventMutation.mutate(eventData);
  };

  const renderCalendarHeader = () => (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="space-between"
      p={2}
      bgcolor={theme.palette.primary.main}
      color={theme.palette.primary.contrastText}
    >
      <IconButton onClick={handlePreviousMonth} color="inherit">
        <ChevronLeftIcon />
      </IconButton>
      <Typography variant="h6">
        {format(currentDate, 'MMMM yyyy')}
      </Typography>
      <IconButton onClick={handleNextMonth} color="inherit">
        <ChevronRightIcon />
      </IconButton>
    </Box>
  );

  const renderDayHeader = () => (
    <Box
      display="grid"
      gridTemplateColumns="repeat(7, 1fr)"
      gap={1}
      p={1}
      bgcolor={theme.palette.background.default}
    >
      {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
        <Box
          key={day}
          p={1}
          textAlign="center"
          fontWeight="bold"
          color={theme.palette.text.secondary}
        >
          <Typography variant="subtitle2">{day}</Typography>
        </Box>
      ))}
    </Box>
  );

  const renderCalendarGrid = () => {
    const days = eachDayOfInterval({ start: startDate, end: endDate });
    const weeks = [];
    let week = [];

    days.forEach((day, index) => {
      week.push(
        <Box
          key={day.toISOString()}
          p={1}
          border={1}
          borderColor={theme.palette.divider}
          bgcolor={theme.palette.background.paper}
          minHeight={150}
          sx={{
            cursor: 'pointer',
            '&:hover': {
              bgcolor: theme.palette.action.hover
            }
          }}
          onClick={() => handleDateClick(day)}
        >
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography
              color={
                format(day, 'MM') !== format(currentDate, 'MM')
                  ? theme.palette.text.disabled
                  : theme.palette.text.primary
              }
            >
              {format(day, 'd')}
            </Typography>
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                handleDateClick(day);
              }}
            >
              <AddIcon fontSize="small" />
            </IconButton>
          </Box>
          
          {/* Render events for this day */}
          {events?.filter(event =>
            format(new Date(event.start_time), 'yyyy-MM-dd') ===
            format(day, 'yyyy-MM-dd')
          ).map(event => (
            <EventCard
              key={event.id}
              event={event}
              onClick={(e) => {
                e.stopPropagation();
                // Handle event click
              }}
            />
          ))}
        </Box>
      );

      if ((index + 1) % 7 === 0 || index === days.length - 1) {
        weeks.push(
          <Box
            key={`week-${index}`}
            display="grid"
            gridTemplateColumns="repeat(7, 1fr)"
            gap={1}
          >
            {week}
          </Box>
        );
        week = [];
      }
    });

    return weeks;
  };

  return (
    <Paper elevation={3}>
      {renderCalendarHeader()}
      {renderDayHeader()}
      
      {isLoading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Box p={2}>
          <Box display="flex" flexDirection="column" gap={1}>
            {renderCalendarGrid()}
          </Box>
        </Box>
      )}

      <EventDialog
        open={isEventDialogOpen}
        onClose={() => setIsEventDialogOpen(false)}
        onSubmit={handleCreateEvent}
        selectedDate={selectedDate}
        isSubmitting={createEventMutation.isLoading}
      />
    </Paper>
  );
};

export default Calendar;