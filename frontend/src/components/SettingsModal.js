import React, { useState, useEffect } from 'react';
import { Modal, Box, Typography, TextField, Button, Fade } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 600,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'column',
  gap: 2
};

function SettingsModal({ open, onClose, account, onSave }) {
  const [task, setTask] = useState({
    post_url: '',
    keywords: '',
    comment_replies: '',
    dm_replies: ''
  });

  useEffect(() => {
    // When the modal opens, populate the form with the first task's data, if it exists.
    if (account && account.tasks && account.tasks.length > 0) {
      const currentTask = account.tasks[0];
      setTask({
        post_url: currentTask.post_url || '',
        keywords: (currentTask.keywords || []).join(', '),
        comment_replies: (currentTask.comment_replies || []).join('\\n'),
        dm_replies: (currentTask.dm_replies || []).join('\\n')
      });
    } else {
      // Reset form if no task data
      setTask({ post_url: '', keywords: '', comment_replies: '', dm_replies: '' });
    }
  }, [account, open]);

  const handleChange = (e) => {
    setTask({ ...task, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    const formattedTask = {
      post_url: task.post_url,
      keywords: task.keywords.split(',').map(k => k.trim()).filter(Boolean),
      comment_replies: task.comment_replies.split('\\n').filter(Boolean),
      dm_replies: task.dm_replies.split('\\n').filter(Boolean)
    };
    // We pass an array of tasks to the save function
    onSave([formattedTask]);
  };

  if (!account) return null;

  return (
    <Modal open={open} onClose={onClose}>
      <Fade in={open}>
        <Box sx={style}>
          <Typography variant="h6">Settings for {account.username}</Typography>
          <TextField name="post_url" label="Post URL" value={task.post_url} onChange={handleChange} fullWidth />
          <TextField name="keywords" label="Keywords (comma-separated)" value={task.keywords} onChange={handleChange} fullWidth />
          <TextField name="comment_replies" label="Comment Replies (one per line)" value={task.comment_replies} onChange={handleChange} multiline rows={3} fullWidth />
          <TextField name="dm_replies" label="DM Replies (one per line)" value={task.dm_replies} onChange={handleChange} multiline rows={3} fullWidth />
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
            <Button onClick={onClose} sx={{ mr: 1 }}>Cancel</Button>
            <Button variant="contained" onClick={handleSave}>Save</Button>
          </Box>
        </Box>
      </Fade>
    </Modal>
  );
}

export default SettingsModal;
