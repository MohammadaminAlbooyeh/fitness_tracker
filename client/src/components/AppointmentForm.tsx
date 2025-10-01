import { FC, useState, useEffect } from 'react';
import {
  Box,
  TextField,
  MenuItem,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  FormHelperText
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { Appointment, ConsultationType, Client } from '../types';

interface AppointmentFormProps {
  appointment: Appointment;
  onSubmit: (appointment: Appointment) => void;
  onCancel: () => void;
}

const validationSchema = yup.object({
  clientId: yup.number().required('Client is required'),
  serviceId: yup.number().required('Service is required'),
  startTime: yup.date().required('Start time is required'),
  endTime: yup
    .date()
    .required('End time is required')
    .min(
      yup.ref('startTime'),
      'End time must be later than start time'
    ),
  consultationType: yup.string().required('Consultation type is required'),
  location: yup.string().when('consultationType', {
    is: ConsultationType.IN_PERSON,
    then: yup.string().required('Location is required for in-person consultations')
  }),
  meetingUrl: yup.string().when('consultationType', {
    is: ConsultationType.VIRTUAL,
    then: yup.string().required('Meeting URL is required for virtual consultations')
  }),
  notes: yup.string()
});

const AppointmentForm: FC<AppointmentFormProps> = ({
  appointment,
  onSubmit,
  onCancel
}) => {
  const [clients, setClients] = useState<Client[]>([]);
  const [services, setServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [clientsRes, servicesRes] = await Promise.all([
          fetch('/api/professional/clients'),
          fetch('/api/professional/services')
        ]);

        const [clientsData, servicesData] = await Promise.all([
          clientsRes.json(),
          servicesRes.json()
        ]);

        setClients(clientsData);
        setServices(servicesData);
      } catch (error) {
        console.error('Error fetching form data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formik = useFormik({
    initialValues: {
      clientId: appointment.clientId || '',
      serviceId: appointment.serviceId || '',
      startTime: appointment.start || new Date(),
      endTime: appointment.end || new Date(),
      consultationType: appointment.consultationType || ConsultationType.VIRTUAL,
      location: appointment.location || '',
      meetingUrl: appointment.meetingUrl || '',
      notes: appointment.notes || ''
    },
    validationSchema,
    onSubmit: (values) => {
      onSubmit({
        ...appointment,
        ...values
      });
    }
  });

  if (loading) {
    return <Box>Loading...</Box>;
  }

  return (
    <form onSubmit={formik.handleSubmit}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth error={Boolean(formik.errors.clientId)}>
            <InputLabel>Client</InputLabel>
            <Select
              name="clientId"
              value={formik.values.clientId}
              onChange={formik.handleChange}
            >
              {clients.map((client) => (
                <MenuItem key={client.id} value={client.id}>
                  {client.name}
                </MenuItem>
              ))}
            </Select>
            {formik.errors.clientId && (
              <FormHelperText>{formik.errors.clientId}</FormHelperText>
            )}
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth error={Boolean(formik.errors.serviceId)}>
            <InputLabel>Service</InputLabel>
            <Select
              name="serviceId"
              value={formik.values.serviceId}
              onChange={formik.handleChange}
            >
              {services.map((service) => (
                <MenuItem key={service.id} value={service.id}>
                  {service.name}
                </MenuItem>
              ))}
            </Select>
            {formik.errors.serviceId && (
              <FormHelperText>{formik.errors.serviceId}</FormHelperText>
            )}
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DateTimePicker
              label="Start Time"
              value={formik.values.startTime}
              onChange={(value) => formik.setFieldValue('startTime', value)}
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: Boolean(formik.errors.startTime),
                  helperText: formik.errors.startTime
                }
              }}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12} md={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DateTimePicker
              label="End Time"
              value={formik.values.endTime}
              onChange={(value) => formik.setFieldValue('endTime', value)}
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: Boolean(formik.errors.endTime),
                  helperText: formik.errors.endTime
                }
              }}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth error={Boolean(formik.errors.consultationType)}>
            <InputLabel>Consultation Type</InputLabel>
            <Select
              name="consultationType"
              value={formik.values.consultationType}
              onChange={formik.handleChange}
            >
              <MenuItem value={ConsultationType.VIRTUAL}>Virtual</MenuItem>
              <MenuItem value={ConsultationType.IN_PERSON}>In Person</MenuItem>
            </Select>
            {formik.errors.consultationType && (
              <FormHelperText>{formik.errors.consultationType}</FormHelperText>
            )}
          </FormControl>
        </Grid>

        {formik.values.consultationType === ConsultationType.IN_PERSON && (
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Location"
              name="location"
              value={formik.values.location}
              onChange={formik.handleChange}
              error={Boolean(formik.errors.location)}
              helperText={formik.errors.location}
            />
          </Grid>
        )}

        {formik.values.consultationType === ConsultationType.VIRTUAL && (
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Meeting URL"
              name="meetingUrl"
              value={formik.values.meetingUrl}
              onChange={formik.handleChange}
              error={Boolean(formik.errors.meetingUrl)}
              helperText={formik.errors.meetingUrl}
            />
          </Grid>
        )}

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Notes"
            name="notes"
            multiline
            rows={4}
            value={formik.values.notes}
            onChange={formik.handleChange}
            error={Boolean(formik.errors.notes)}
            helperText={formik.errors.notes}
          />
        </Grid>

        <Grid item xs={12}>
          <Box display="flex" justifyContent="flex-end" gap={2}>
            <Button onClick={onCancel}>Cancel</Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={formik.isSubmitting}
            >
              {appointment.id ? 'Update' : 'Create'} Appointment
            </Button>
          </Box>
        </Grid>
      </Grid>
    </form>
  );
};

export default AppointmentForm;