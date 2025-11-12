import React, { useState, useEffect, useCallback } from 'react';
import { Paper, Typography, Button, Box, Alert } from '@mui/material';
import AccountsTable from './AccountsTable';
import AddAccountModal from './AddAccountModal';
import { getAccounts, addAccount } from '../api.js';

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false);

  const fetchAccounts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getAccounts();
      setAccounts(response.data);
    } catch (err) {
      setError('Failed to fetch accounts. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleAddAccount = async ({ username, password }) => {
    try {
      await addAccount(username, password);
      fetchAccounts(); // Refresh the list after adding
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add account.');
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5">Accounts</Typography>
        <Button variant="contained" onClick={() => setModalOpen(true)}>
          Add Account
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <Typography>Loading accounts...</Typography>
      ) : (
        <AccountsTable accounts={accounts} refreshAccounts={fetchAccounts} />
      )}

      <AddAccountModal open={isModalOpen} onClose={() => setModalOpen(false)} onAddAccount={handleAddAccount} />
    </Paper>
  );
}

export default Dashboard;
