import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CssBaseline, Box } from '@mui/material';
import { ThemeProvider } from './context/ThemeContext';
import { NotificationProvider } from './context/NotificationContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import CreateWorkout from './components/CreateWorkout';
import CreateExercise from './components/CreateExercise';
import WorkoutProgress from './components/WorkoutProgress';
import UserProfile from './components/UserProfile';
import LandingPage from './components/LandingPage';
import Navigation from './components/Navigation';
import MainLayout from './components/MainLayout';
import { Achievements } from './components/Achievements';

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Navigation />
      <MainLayout>{children}</MainLayout>
    </>
  );
}

function App() {
  return (
    <ThemeProvider>
      <NotificationProvider>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <Box sx={{ display: 'flex' }}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/" element={<LandingPage />} />
                <Route
                  path="/dashboard"
                  element={
                    <PrivateRoute>
                      <AuthenticatedLayout>
                        <Dashboard />
                      </AuthenticatedLayout>
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <PrivateRoute>
                      <AuthenticatedLayout>
                        <UserProfile />
                      </AuthenticatedLayout>
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/create-workout"
                  element={
                    <PrivateRoute>
                      <AuthenticatedLayout>
                        <CreateWorkout />
                      </AuthenticatedLayout>
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/create-exercise"
                  element={
                    <PrivateRoute>
                      <AuthenticatedLayout>
                        <CreateExercise />
                      </AuthenticatedLayout>
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/workout/:id"
                  element={
                    <PrivateRoute>
                      <AuthenticatedLayout>
                        <WorkoutProgress />
                      </AuthenticatedLayout>
                    </PrivateRoute>
                  }
                />
              </Routes>
            </Box>
          </Router>
        </AuthProvider>
      </NotificationProvider>
    </ThemeProvider>
  );
