import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Grid,
  Typography,
  Button,
  CircularProgress,
  ImageList,
  ImageListItem,
  Dialog,
  DialogContent,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useNotification } from '../context/NotificationContext';
import { progressApi } from '../api/progress';

interface ProgressPhoto {
  id: number;
  date: string;
  photo_url: string;
  photo_type: 'front' | 'back' | 'side';
}

export const ProgressPhotos: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const { showNotification } = useNotification();
  const [photos, setPhotos] = useState<ProgressPhoto[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [uploadLoading, setUploadLoading] = useState(false);

  useEffect(() => {
    fetchPhotos();
  }, []);

  const fetchPhotos = async () => {
    try {
      const data = await progressApi.getProgressPhotos();
      setPhotos(data);
    } catch (error) {
      console.error('Error fetching photos:', error);
      showNotification('Failed to load progress photos', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = async (event: React.ChangeEvent<HTMLInputElement>, photoType: 'front' | 'back' | 'side') => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('photo', file);
    formData.append('photo_type', photoType);

    setUploadLoading(true);
    try {
      await progressApi.uploadProgressPhoto(formData);
      showNotification('Photo uploaded successfully', 'success');
      fetchPhotos();
    } catch (error) {
      console.error('Error uploading photo:', error);
      showNotification('Failed to upload photo', 'error');
    } finally {
      setUploadLoading(false);
    }
  };

  const handlePhotoClick = (photoUrl: string) => {
    setSelectedPhoto(photoUrl);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  const groupPhotosByDate = () => {
    const grouped: { [key: string]: ProgressPhoto[] } = {};
    photos.forEach((photo) => {
      const date = new Date(photo.date).toLocaleDateString();
      if (!grouped[date]) {
        grouped[date] = [];
      }
      grouped[date].push(photo);
    });
    return grouped;
  };

  const groupedPhotos = groupPhotosByDate();

  const [comparisonMode, setComparisonMode] = useState(false);
  const [selectedDates, setSelectedDates] = useState<string[]>([]);

  const toggleComparisonMode = () => {
    setComparisonMode(!comparisonMode);
    setSelectedDates([]);
  };

  const handleDateSelection = (date: string) => {
    if (selectedDates.includes(date)) {
      setSelectedDates(selectedDates.filter(d => d !== date));
    } else if (selectedDates.length < 2) {
      setSelectedDates([...selectedDates, date].sort());
    }
  };

  const getPhotosByType = (date: string, type: 'front' | 'back' | 'side') => {
    return photos.find(p => 
      new Date(p.date).toLocaleDateString() === date && 
      p.photo_type === type
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Progress Photos
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Button
          variant={comparisonMode ? "contained" : "outlined"}
          color="primary"
          onClick={toggleComparisonMode}
          sx={{ mr: 2 }}
        >
          Comparison Mode
        </Button>
        {comparisonMode && (
          <Typography variant="body2" color="text.secondary">
            Select two dates to compare ({selectedDates.length}/2 selected)
          </Typography>
        )}
      </Box>

      {/* Comparison View */}
      {comparisonMode && selectedDates.length === 2 && (
        <Paper sx={{ p: 2, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Comparing {selectedDates[0]} vs {selectedDates[1]}
          </Typography>
          {['front', 'back', 'side'].map((type) => (
            <Box key={type} sx={{ mb: 4 }}>
              <Typography variant="subtitle1" gutterBottom>
                {type.charAt(0).toUpperCase() + type.slice(1)} View
              </Typography>
              <Grid container spacing={2}>
                {selectedDates.map((date) => (
                  <Grid item xs={12} sm={6} key={date}>
                    <Typography variant="body2" gutterBottom>
                      {date}
                    </Typography>
                    {getPhotosByType(date, type as 'front' | 'back' | 'side') ? (
                      <img
                        src={getPhotosByType(date, type as 'front' | 'back' | 'side')?.photo_url}
                        alt={`${type} view - ${date}`}
                        style={{ width: '100%', borderRadius: 4 }}
                      />
                    ) : (
                      <Paper
                        sx={{
                          p: 2,
                          textAlign: 'center',
                          backgroundColor: 'grey.100'
                        }}
                      >
                        No {type} view photo for this date
                      </Paper>
                    )}
                  </Grid>
                ))}
              </Grid>
            </Box>
          ))}
        </Paper>
      )}

      {/* Upload Buttons */}
      <Paper sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Add New Photos
        </Typography>
        <Grid container spacing={2}>
          {['front', 'back', 'side'].map((type) => (
            <Grid item xs={12} sm={4} key={type}>
              <input
                accept="image/*"
                style={{ display: 'none' }}
                id={`photo-upload-${type}`}
                type="file"
                onChange={(e) => handlePhotoUpload(e, type as 'front' | 'back' | 'side')}
              />
              <label htmlFor={`photo-upload-${type}`}>
                <Button
                  variant="outlined"
                  component="span"
                  fullWidth
                  startIcon={<AddIcon />}
                  disabled={uploadLoading}
                >
                  Upload {type.charAt(0).toUpperCase() + type.slice(1)} View
                </Button>
              </label>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Photo Gallery */}
      {Object.entries(groupedPhotos).map(([date, datePhotos]) => (
        <Paper 
          key={date} 
          sx={{ 
            p: 2, 
            mb: 4,
            border: comparisonMode && selectedDates.includes(date) 
              ? '2px solid' 
              : 'none',
            borderColor: 'primary.main',
            cursor: comparisonMode ? 'pointer' : 'default',
          }}
          onClick={() => comparisonMode && handleDateSelection(date)}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">
              {date}
            </Typography>
            {comparisonMode && (
              <Typography variant="body2" color="text.secondary">
                {selectedDates.includes(date) ? 'Selected' : 'Click to select'}
              </Typography>
            )}
          </Box>
          <ImageList cols={isMobile ? 1 : 3} gap={16}>
            {datePhotos.map((photo) => (
              <ImageListItem
                key={photo.id}
                sx={{ cursor: comparisonMode ? 'default' : 'pointer' }}
                onClick={(e) => {
                  if (!comparisonMode) {
                    e.stopPropagation();
                    handlePhotoClick(photo.photo_url);
                  }
                }}
              >
                <img
                  src={photo.photo_url}
                  alt={`Progress photo - ${photo.photo_type} view`}
                  loading="lazy"
                  style={{ borderRadius: 4 }}
                />
                <Typography variant="caption" sx={{ mt: 1 }}>
                  {photo.photo_type.charAt(0).toUpperCase() + photo.photo_type.slice(1)} View
                </Typography>
              </ImageListItem>
            ))}
          </ImageList>
        </Paper>
      ))}

      {/* Photo Preview Dialog */}
      <Dialog
        open={!!selectedPhoto}
        onClose={() => setSelectedPhoto(null)}
        maxWidth="md"
        fullWidth
      >
        <DialogContent sx={{ p: 0 }}>
          {selectedPhoto && (
            <img
              src={selectedPhoto}
              alt="Progress photo"
              style={{ width: '100%', height: 'auto' }}
            />
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};