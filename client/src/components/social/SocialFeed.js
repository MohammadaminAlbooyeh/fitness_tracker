import React, { useState } from 'react';
import {
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardHeader,
  CardActions,
  Avatar,
  IconButton,
  Button,
  Box,
  Divider,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar
} from '@mui/material';
import {
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  Share as ShareIcon,
  Comment as CommentIcon,
  Send as SendIcon
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { format } from 'date-fns';
import { 
  fetchSocialFeed,
  likeWorkout,
  commentOnWorkout,
  shareWorkout
} from '../../api/social';

const WorkoutPost = ({ post }) => {
  const [showComments, setShowComments] = useState(false);
  const [comment, setComment] = useState('');
  const queryClient = useQueryClient();

  const likeMutation = useMutation(likeWorkout, {
    onSuccess: () => {
      queryClient.invalidateQueries('socialFeed');
    }
  });

  const commentMutation = useMutation(commentOnWorkout, {
    onSuccess: () => {
      queryClient.invalidateQueries('socialFeed');
      setComment('');
    }
  });

  const handleComment = () => {
    if (!comment.trim()) return;
    commentMutation.mutate({
      workoutId: post.id,
      content: comment
    });
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardHeader
        avatar={
          <Avatar src={post.user.avatar_url} alt={post.user.name}>
            {post.user.name[0]}
          </Avatar>
        }
        title={post.user.name}
        subheader={format(new Date(post.created_at), 'MMM d, yyyy')}
      />

      <CardContent>
        <Typography variant="h6" gutterBottom>
          {post.workout.name}
        </Typography>
        
        {post.caption && (
          <Typography variant="body1" color="text.secondary" paragraph>
            {post.caption}
          </Typography>
        )}

        <Box sx={{ my: 2 }}>
          <Typography variant="body2" color="text.secondary">
            🎯 {post.workout.exercises.length} exercises
          </Typography>
          <Typography variant="body2" color="text.secondary">
            ⏱️ {post.workout.duration} minutes
          </Typography>
          {post.workout.calories_burned && (
            <Typography variant="body2" color="text.secondary">
              🔥 {post.workout.calories_burned} calories
            </Typography>
          )}
        </Box>
      </CardContent>

      <Divider />

      <CardActions disableSpacing>
        <IconButton 
          onClick={() => likeMutation.mutate(post.id)}
          color={post.liked ? "primary" : "default"}
        >
          {post.liked ? <FavoriteIcon /> : <FavoriteBorderIcon />}
        </IconButton>
        <Typography variant="body2" color="text.secondary">
          {post.likes} likes
        </Typography>

        <IconButton onClick={() => setShowComments(!showComments)}>
          <CommentIcon />
        </IconButton>
        <Typography variant="body2" color="text.secondary">
          {post.comments.length} comments
        </Typography>

        <IconButton>
          <ShareIcon />
        </IconButton>
      </CardActions>

      {showComments && (
        <CardContent>
          <List>
            {post.comments.map((comment) => (
              <ListItem key={comment.id} alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar src={comment.user.avatar_url} alt={comment.user.name}>
                    {comment.user.name[0]}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={comment.user.name}
                  secondary={
                    <>
                      <Typography component="span" variant="body2">
                        {comment.content}
                      </Typography>
                      <Typography component="span" variant="caption" display="block">
                        {format(new Date(comment.created_at), 'MMM d, yyyy')}
                      </Typography>
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>

          <Box sx={{ display: 'flex', mt: 2 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Add a comment..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              variant="outlined"
            />
            <IconButton 
              color="primary"
              onClick={handleComment}
              disabled={!comment.trim()}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </CardContent>
      )}
    </Card>
  );
};

const SocialFeed = () => {
  const { data: posts, isLoading } = useQuery('socialFeed', fetchSocialFeed);

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Social Feed
        </Typography>

        {isLoading ? (
          <Typography>Loading feed...</Typography>
        ) : (
          posts?.map((post) => (
            <WorkoutPost key={post.id} post={post} />
          ))
        )}
      </Box>
    </Container>
  );
};

export default SocialFeed;