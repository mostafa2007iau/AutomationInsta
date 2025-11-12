import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip, IconButton, Tooltip } from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import PauseCircleOutlineIcon from '@mui/icons-material/PauseCircleOutline';
import SettingsIcon from '@mui/icons-material/Settings';
import LoginIcon from '@mui/icons-material/Login';
import SettingsModal from './SettingsModal'; // Import the modal
import { startTasks, stopTasks, loginAccount, updateAccountTasks } from '../api.js';

function getStatusChip(status) {
  let color = 'default';
  let label = status.replace(/_/g, ' ');

  if (status === 'logged_in') color = 'primary';
  else if (status === 'running_tasks') color = 'success';
  else if (status.startsWith('error')) color = 'error';
  else if (status === 'added') {
    color = 'secondary';
    label = 'Pending Login';
  }
  return <Chip label={label} color={color} size="small" />;
}

function AccountsTable({ accounts, refreshAccounts }) {
  const [isSettingsOpen, setSettingsOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState(null);

  const handleAction = async (action, username, successMessage, errorMessage) => {
    try {
      await action(username);
      refreshAccounts();
    } catch (error) {
      alert(error.response?.data?.detail || errorMessage);
    }
  };

  const openSettings = (account) => {
    setSelectedAccount(account);
    setSettingsOpen(true);
  };

  const handleSaveSettings = async (tasks) => {
    if (!selectedAccount) return;
    try {
      await updateAccountTasks(selectedAccount.username, tasks);
      setSettingsOpen(false);
      refreshAccounts();
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to save settings.');
    }
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="accounts table">
          <TableHead>
            <TableRow>
              <TableCell>Username</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {accounts.map((account) => (
              <TableRow key={account.username}>
                <TableCell component="th" scope="row">{account.username}</TableCell>
                <TableCell>{getStatusChip(account.status)}</TableCell>
                <TableCell align="right">
                  {(account.status === 'added' || account.status.startsWith('error')) && (
                    <Tooltip title="Login"><IconButton color="success" onClick={() => handleAction(loginAccount, account.username, "Login successful!", "Login failed.")}><LoginIcon /></IconButton></Tooltip>
                  )}
                  <Tooltip title="Start Automation"><span><IconButton color="primary" disabled={account.status !== 'logged_in'} onClick={() => handleAction(startTasks, account.username, "Tasks started!", "Failed to start tasks.")}><PlayCircleOutlineIcon /></IconButton></span></Tooltip>
                  <Tooltip title="Stop Automation"><span><IconButton color="warning" disabled={account.status !== 'running_tasks'} onClick={() => handleAction(stopTasks, account.username, "Tasks stopped!", "Failed to stop tasks.")}><PauseCircleOutlineIcon /></IconButton></span></Tooltip>
                  <Tooltip title="Settings"><IconButton color="secondary" onClick={() => openSettings(account)}><SettingsIcon /></IconButton></Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <SettingsModal open={isSettingsOpen} onClose={() => setSettingsOpen(false)} account={selectedAccount} onSave={handleSaveSettings} />
    </>
  );
}

export default AccountsTable;
