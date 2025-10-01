import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Avatar,
  TextField,
  Button,
  IconButton,
  Divider,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
} from '@mui/material';
import {
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  Comment as CommentIcon,
  Share as ShareIcon,
} from '@mui/icons-material';
import { useNotification } from '../context/NotificationContext';
import { socialApi } from '../api/social';

interface Post {
  id: number;
  content: string;
  user: {
    id: number;
    username: string;
    profile_picture: string;
  };
  created_at: string;
  likes_count: number;
  comments_count: number;
  workout_id?: number;
  achievement_id?: number;
}

interface Comment {
  id: number;
  content: string;
  user: {
    id: number;
    username: string;
    profile_picture: string;
  };
  created_at: string;
}

export const SocialFeed: React.FC = () => {
  const { showNotification } = useNotification();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [newPost, setNewPost] = useState('');
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [commentsLoading, setCommentsLoading] = useState(false);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const data = await socialApi.getFeed();
      setPosts(data);
    } catch (error) {
      console.error('Error fetching posts:', error);
      showNotification('Failed to load posts', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handlePostSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      await socialApi.createPost({ content: newPost });
      showNotification('Post created successfully', 'success');
      setNewPost('');
      fetchPosts();
    } catch (error) {
      console.error('Error creating post:', error);
      showNotification('Failed to create post', 'error');
    }
  };

  const handleLike = async (postId: number) => {
    try {
      await socialApi.likePost(postId);
      setPosts(posts.map(post => 
        post.id === postId 
          ? { ...post, likes_count: post.likes_count + 1 }
          : post
      ));
      showNotification('Post liked', 'success');
    } catch (error) {
      console.error('Error liking post:', error);
      showNotification('Failed to like post', 'error');
    }
  };

  const handleCommentClick = async (post: Post) => {
    setSelectedPost(post);
    setCommentsLoading(true);
    try {
      const comments = await socialApi.getComments(post.id);
      setComments(comments);
    } catch (error) {
      console.error('Error fetching comments:', error);
      showNotification('Failed to load comments', 'error');
    } finally {
      setCommentsLoading(false);
    }
  };

  const handleCommentSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!selectedPost) return;

    try {
      const comment = await socialApi.createComment(selectedPost.id, { content: newComment });
      setComments([...comments, comment]);
      setNewComment('');
      setPosts(posts.map(post =>
        post.id === selectedPost.id
          ? { ...post, comments_count: post.comments_count + 1 }
          : post
      ));
    } catch (error) {
      console.error('Error posting comment:', error);
      showNotification('Failed to post comment', 'error');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Paper sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Create Post
        </Typography>
        <form onSubmit={handlePostSubmit}>
          <TextField
            fullWidth
            multiline
            rows={3}
            placeholder="What's on your mind?"
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={!newPost.trim()}
          >
            Post
          </Button>
        </form>
      </Paper>

      {posts.map((post) => (
        <Card key={post.id} sx={{ mb: 2 }}>
          <CardContent>
            <Box display="flex" alignItems="center" mb={2}>
              <Avatar src={post.user.profile_picture} sx={{ mr: 2 }}>
                {post.user.username[0]}
              </Avatar>
              <Box>
                <Typography variant="subtitle1">
                  {post.user.username}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {new Date(post.created_at).toLocaleString()}
                </Typography>
              </Box>
            </Box>
            <Typography variant="body1" sx={{ mb: 2 }}>
              {post.content}
            </Typography>
          </CardContent>
          <CardActions>
            <IconButton onClick={() => handleLike(post.id)}>
              <FavoriteBorderIcon />
            </IconButton>
            <Typography variant="caption" sx={{ mr: 2 }}>
              {post.likes_count}
            </Typography>
            <IconButton onClick={() => handleCommentClick(post)}>
              <CommentIcon />
            </IconButton>
            <Typography variant="caption" sx={{ mr: 2 }}>
              {post.comments_count}
            </Typography>
            <IconButton>
              <ShareIcon />
            </IconButton>
          </CardActions>
        </Card>
      ))}

      <Dialog
        open={!!selectedPost}
        onClose={() => setSelectedPost(null)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Comments</DialogTitle>
        <DialogContent>
          {commentsLoading ? (
            <Box display="flex" justifyContent="center" my={2}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              <List>
                {comments.map((comment) => (
                  <ListItem key={comment.id}>
                    <ListItemAvatar>
                      <Avatar src={comment.user.profile_picture}>
                        {comment.user.username[0]}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={comment.content}
                      secondary={`${comment.user.username} • ${new Date(
                        comment.created_at
                      ).toLocaleString()}`}
                    />
                  </ListItem>
                ))}
              </List>
              <Divider sx={{ my: 2 }} />
              <form onSubmit={handleCommentSubmit}>
                <TextField
                  fullWidth
                  placeholder="Write a comment..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  sx={{ mb: 2 }}
                />
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={!newComment.trim()}
                >
                  Comment
                </Button>
              </form>
            </>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  );
};