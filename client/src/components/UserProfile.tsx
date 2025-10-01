import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Avatar,
  Box,
  Grid,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import api from '../api/api';

interface UserData {
  username: string;
  email: string;
  height?: number;
  weight?: number;
  fitnessGoals?: string;
}

const UserProfile = () => {
  const { user } = useAuth();
  const [userData, setUserData] = useState<UserData | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get('/users/profile');
        setUserData(response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };
    fetchUserData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userData) return;

    setIsSaving(true);
    try {
      await api.put('/users/profile', userData);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    } finally {
      setIsSaving(false);
    }
  };

  if (!userData) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
            <Avatar
              sx={{
                width: 120,
                height: 120,
                margin: '0 auto',
                mb: 2,
                bgcolor: 'primary.main',
              }}
            >
              {userData.username[0].toUpperCase()}
            </Avatar>
            <Typography variant="h5" gutterBottom>
              {userData.username}
            </Typography>
          </Grid>
          <Grid item xs={12} md={8}>
            <form onSubmit={handleSubmit}>
              <Box sx={{ mb: 2 }}>
                <TextField
                  fullWidth
                  label="Email"
                  value={userData.email}
                  disabled={!isEditing}
                  onChange={(e) =>
                    setUserData({ ...userData, email: e.target.value })
                  }
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Height (cm)"
                  type="number"
                  value={userData.height || ''}
                  disabled={!isEditing}
                  onChange={(e) =>
                    setUserData({
                      ...userData,
                      height: parseInt(e.target.value),
                    })
                  }
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Weight (kg)"
                  type="number"
                  value={userData.weight || ''}
                  disabled={!isEditing}
                  onChange={(e) =>
                    setUserData({
                      ...userData,
                      weight: parseInt(e.target.value),
                    })
                  }
                  margin="normal"
                />
                <TextField
                  fullWidth
                  label="Fitness Goals"
                  multiline
                  rows={4}
                  value={userData.fitnessGoals || ''}
                  disabled={!isEditing}
                  onChange={(e) =>
                    setUserData({
                      ...userData,
                      fitnessGoals: e.target.value,
                    })
                  }
                  margin="normal"
                />
              </Box>
              {isEditing ? (
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    disabled={isSaving}
                  >
                    {isSaving ? 'Saving...' : 'Save Changes'}
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={() => setIsEditing(false)}
                    disabled={isSaving}
                  >
                    Cancel
                  </Button>
                </Box>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => setIsEditing(true)}
                >
                  Edit Profile
                </Button>
              )}
            </form>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default UserProfile;