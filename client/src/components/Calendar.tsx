import { FC, useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Calendar as BigCalendar,
  momentLocalizer,
  Views,
  View
} from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import { Appointment } from '../types';
import AppointmentForm from './AppointmentForm';

const localizer = momentLocalizer(moment);

interface CalendarProps {
  appointments: Appointment[];
  onAppointmentUpdate: (appointment: Appointment) => void;
}

const Calendar: FC<CalendarProps> = ({ appointments, onAppointmentUpdate }) => {
  const [view, setView] = useState<View>(Views.MONTH);
  const [date, setDate] = useState(new Date());
  const [selectedAppointment, setSelectedAppointment] = useState<Appointment | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  const handleNavigate = useCallback((newDate: Date) => {
    setDate(newDate);
  }, []);

  const handleViewChange = useCallback((newView: View) => {
    setView(newView);
  }, []);

  const handleSelectEvent = useCallback((event: Appointment) => {
    setSelectedAppointment(event);
    setIsFormOpen(true);
  }, []);

  const handleSelectSlot = useCallback(
    ({ start, end }: { start: Date; end: Date }) => {
      setSelectedAppointment({
        id: 0, // temporary ID
        start,
        end,
        title: 'New Appointment',
        status: 'scheduled'
      } as Appointment);
      setIsFormOpen(true);
    },
    []
  );

  const handleFormClose = () => {
    setIsFormOpen(false);
    setSelectedAppointment(null);
  };

  const handleFormSubmit = (appointment: Appointment) => {
    onAppointmentUpdate(appointment);
    handleFormClose();
  };

  const eventStyleGetter = useCallback(
    (event: Appointment) => {
      let backgroundColor = '#3174ad';
      let borderColor = '#2c6493';

      switch (event.status) {
        case 'confirmed':
          backgroundColor = '#4caf50';
          borderColor = '#388e3c';
          break;
        case 'cancelled':
          backgroundColor = '#f44336';
          borderColor = '#d32f2f';
          break;
        case 'completed':
          backgroundColor = '#9e9e9e';
          borderColor = '#757575';
          break;
        case 'no_show':
          backgroundColor = '#ff9800';
          borderColor = '#f57c00';
          break;
      }

      return {
        style: {
          backgroundColor,
          borderColor,
          opacity: 0.8,
          color: 'white',
          borderRadius: '3px',
          border: 'none',
          display: 'block'
        }
      };
    },
    []
  );

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Schedule</Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() =>
            handleSelectSlot({
              start: new Date(),
              end: new Date(new Date().getTime() + 60 * 60 * 1000)
            })
          }
        >
          New Appointment
        </Button>
      </Box>

      <Paper sx={{ height: 'calc(100vh - 200px)', p: 2 }}>
        <BigCalendar
          localizer={localizer}
          events={appointments}
          startAccessor="start"
          endAccessor="end"
          view={view}
          views={[Views.MONTH, Views.WEEK, Views.DAY, Views.AGENDA]}
          date={date}
          onNavigate={handleNavigate}
          onView={handleViewChange}
          onSelectEvent={handleSelectEvent}
          onSelectSlot={handleSelectSlot}
          selectable
          eventPropGetter={eventStyleGetter}
          popup
          tooltipAccessor={(event) => event.title}
          messages={{
            today: 'Today',
            previous: 'Previous',
            next: 'Next',
            month: 'Month',
            week: 'Week',
            day: 'Day',
            agenda: 'Agenda'
          }}
        />
      </Paper>

      <Dialog open={isFormOpen} onClose={handleFormClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedAppointment?.id ? 'Edit Appointment' : 'New Appointment'}
        </DialogTitle>
        <DialogContent>
          {selectedAppointment && (
            <AppointmentForm
              appointment={selectedAppointment}
              onSubmit={handleFormSubmit}
              onCancel={handleFormClose}
            />
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default Calendar;