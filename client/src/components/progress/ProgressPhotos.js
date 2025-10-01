import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Box,
  ImageList,
  ImageListItem,
  IconButton
} from '@mui/material';
import {
  Add as AddIcon,
  ZoomIn as ZoomInIcon,
  CalendarToday as CalendarIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import { uploadProgressPhoto, fetchProgressPhotos } from '../../api/progress';

const PHOTO_TYPES = [
  { value: 'front', label: 'Front View' },
  { value: 'side', label: 'Side View' },
  { value: 'back', label: 'Back View' }
];

const ProgressPhotos = () => {
  const queryClient = useQueryClient();
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [photoFile, setPhotoFile] = useState(null);
  const [formData, setFormData] = useState({
    photo_type: 'front',
    notes: '',
    measurements: {}
  });

  const { data: photos, isLoading } = useQuery(
    'progressPhotos',
    fetchProgressPhotos
  );

  const uploadMutation = useMutation(uploadProgressPhoto, {
    onSuccess: () => {
      queryClient.invalidateQueries('progressPhotos');
      setUploadDialogOpen(false);
      setPhotoFile(null);
      setFormData({
        photo_type: 'front',
        notes: '',
        measurements: {}
      });
    }
  });

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setPhotoFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!photoFile) return;

    const formDataObj = new FormData();
    formDataObj.append('photo', photoFile);
    formDataObj.append('data', JSON.stringify(formData));
    
    uploadMutation.mutate(formDataObj);
  };

  const handleChange = (field) => (event) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const groupPhotosByDate = (photos) => {
    const grouped = {};
    photos?.forEach(photo => {
      const date = format(new Date(photo.date), 'yyyy-MM-dd');
      if (!grouped[date]) {
        grouped[date] = [];
      }
      grouped[date].push(photo);
    });
    return grouped;
  };

  const groupedPhotos = groupPhotosByDate(photos);

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4" gutterBottom>
              Progress Photos
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setUploadDialogOpen(true)}
            >
              Add Photo
            </Button>
          </Grid>

          {isLoading ? (
            <Grid item xs={12}>
              <Typography>Loading...</Typography>
            </Grid>
          ) : (
            Object.entries(groupedPhotos).map(([date, datePhotos]) => (
              <Grid item xs={12} key={date}>
                <Paper sx={{ p: 3, mb: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>
                    <CalendarIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    {format(new Date(date), 'MMMM d, yyyy')}
                  </Typography>
                  
                  <ImageList cols={3} gap={16}>
                    {datePhotos.map((photo) => (
                      <ImageListItem key={photo.id}>
                        <img
                          src={photo.photo_url}
                          alt={`Progress photo - ${photo.photo_type}`}
                          loading="lazy"
                          style={{ cursor: 'pointer' }}
                          onClick={() => setSelectedPhoto(photo)}
                        />
                        <Box
                          sx={{
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            right: 0,
                            bgcolor: 'rgba(0, 0, 0, 0.5)',
                            color: 'white',
                            p: 1
                          }}
                        >
                          <Typography variant="caption">
                            {PHOTO_TYPES.find(t => t.value === photo.photo_type)?.label}
                          </Typography>
                          <IconButton
                            size="small"
                            sx={{ color: 'white', float: 'right' }}
                            onClick={() => setSelectedPhoto(photo)}
                          >
                            <ZoomInIcon />
                          </IconButton>
                        </Box>
                      </ImageListItem>
                    ))}
                  </ImageList>
                </Paper>
              </Grid>
            ))
          )}
        </Grid>

        {/* Upload Dialog */}
        <Dialog open={uploadDialogOpen} onClose={() => setUploadDialogOpen(false)}>
          <DialogTitle>Upload Progress Photo</DialogTitle>
          <DialogContent>
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <Button
                  variant="outlined"
                  component="label"
                  fullWidth
                >
                  Choose Photo
                  <input
                    type="file"
                    hidden
                    accept="image/*"
                    onChange={handleFileChange}
                  />
                </Button>
                {photoFile && (
                  <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                    Selected: {photoFile.name}
                  </Typography>
                )}
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  select
                  fullWidth
                  label="Photo Type"
                  value={formData.photo_type}
                  onChange={handleChange('photo_type')}
                >
                  {PHOTO_TYPES.map(type => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Notes"
                  value={formData.notes}
                  onChange={handleChange('notes')}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setUploadDialogOpen(false)}>Cancel</Button>
            <Button
              onClick={handleSubmit}
              variant="contained"
              color="primary"
              disabled={!photoFile || uploadMutation.isLoading}
            >
              Upload
            </Button>
          </DialogActions>
        </Dialog>

        {/* Photo Preview Dialog */}
        <Dialog
          open={Boolean(selectedPhoto)}
          onClose={() => setSelectedPhoto(null)}
          maxWidth="md"
          fullWidth
        >
          {selectedPhoto && (
            <>
              <DialogTitle>
                {PHOTO_TYPES.find(t => t.value === selectedPhoto.photo_type)?.label} - 
                {format(new Date(selectedPhoto.date), 'MMMM d, yyyy')}
              </DialogTitle>
              <DialogContent>
                <img
                  src={selectedPhoto.photo_url}
                  alt="Progress"
                  style={{
                    width: '100%',
                    maxHeight: '70vh',
                    objectFit: 'contain'
                  }}
                />
                {selectedPhoto.notes && (
                  <Typography sx={{ mt: 2 }}>
                    Notes: {selectedPhoto.notes}
                  </Typography>
                )}
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setSelectedPhoto(null)}>Close</Button>
              </DialogActions>
            </>
          )}
        </Dialog>
      </Box>
    </Container>
  );
};

export default ProgressPhotos;