import React, { useState } from 'react';
import { Modal, Box, Typography, TextField, Button, Fade } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

function AddAccountModal({ open, onClose, onAddAccount }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    // In the next step, this will trigger an API call
    console.log({ username, password });
    onAddAccount({ username, password });
    onClose(); // Close modal after submission
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Fade in={open}>
        <Box sx={style}>
          <Typography variant="h6" component="h2" mb={2}>
            Add New Account
          </Typography>
          <TextField
            fullWidth
            label="Instagram Username"
            variant="outlined"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth
            label="Password"
            type="password"
            variant="outlined"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ mb: 3 }}
          />
          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button onClick={onClose} sx={{ mr: 1 }}>Cancel</Button>
            <Button variant="contained" onClick={handleSubmit}>Add Account</Button>
          </Box>
        </Box>
      </Fade>
    </Modal>
  );
}

export default AddAccountModal;
