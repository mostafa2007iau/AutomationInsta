document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const loginSection = document.getElementById('login-section');
    const mainContent = document.getElementById('main-content');
    const loginStatusEl = document.getElementById('login-status');
    const logoutBtn = document.getElementById('logout-btn');

    const credentialsForm = document.getElementById('credentials-form');
    const sessionForm = document.getElementById('session-form');
    const automationForm = document.getElementById('automation-form');

    const automationsList = document.getElementById('automations-list');
    const refreshTasksBtn = document.getElementById('refresh-tasks-btn');

    const messageArea = document.getElementById('message-area');
    const loadingSpinner = document.getElementById('loading-spinner');

    const API_BASE_URL = 'http://localhost:8000'; // Adjust if your backend runs elsewhere

    // --- Helper Functions ---
    const showLoading = (show) => {
        loadingSpinner.classList.toggle('hidden', !show);
    };

    const showMessage = (message, isError = false) => {
        messageArea.textContent = message;
        messageArea.className = isError ? 'message-error' : 'message-success';
        setTimeout(() => messageArea.textContent = '', 5000);
    };

    const updateUIForLoginStatus = (isLoggedIn, username = '') => {
        if (isLoggedIn) {
            loginSection.classList.add('hidden');
            mainContent.classList.remove('hidden');
            logoutBtn.classList.remove('hidden');
            loginStatusEl.textContent = `Logged in as ${username}`;
            loginStatusEl.style.color = '#28a745';
            fetchActiveAutomations();
        } else {
            loginSection.classList.remove('hidden');
            mainContent.classList.add('hidden');
            logoutBtn.classList.add('hidden');
            loginStatusEl.textContent = 'Logged Out';
            loginStatusEl.style.color = '#e44d26';
            automationsList.innerHTML = '';
        }
    };

    // --- API Calls ---
    const checkLoginStatus = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            if (!response.ok) throw new Error('Could not connect to server.');
            const data = await response.json();
            updateUIForLoginStatus(data.status === 'logged_in', data.username);
        } catch (error) {
            showMessage(error.message, true);
        }
    };

    const fetchActiveAutomations = async () => {
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/automations`);
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || 'Failed to fetch automations.');
            }
            const tasks = await response.json();
            automationsList.innerHTML = ''; // Clear list
            Object.entries(tasks).forEach(([taskId, task]) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>Post: <a href="${task.post_url}" target="_blank">${task.post_url.substring(0, 40)}...</a> | Keywords: ${task.keywords.join(', ')}</span>
                    <button class="delete-btn" data-task-id="${taskId}">Delete</button>
                `;
                automationsList.appendChild(li);
            });
        } catch (error) {
            showMessage(error.message, true);
        } finally {
            showLoading(false);
        }
    };

    // --- Event Handlers ---
    credentialsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        showLoading(true);
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch(`${API_BASE_URL}/login/credentials`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Login failed.');
            showMessage(data.message);
            checkLoginStatus();
        } catch (error) {
            showMessage(error.message, true);
        } finally {
            showLoading(false);
        }
    });

    sessionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        showLoading(true);
        const sessionDataRaw = document.getElementById('session-data').value;
        try {
            const session_data = JSON.parse(sessionDataRaw);
            const response = await fetch(`${API_BASE_URL}/login/session`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_data }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Login failed.');
            showMessage(data.message);
            checkLoginStatus();
        } catch (error) {
            showMessage('Invalid JSON or login failed: ' + error.message, true);
        } finally {
            showLoading(false);
        }
    });

    logoutBtn.addEventListener('click', async () => {
        showLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/logout`, { method: 'POST' });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Logout failed.');
            showMessage(data.message);
        } catch (error) {
            showMessage(error.message, true);
        } finally {
            showLoading(false);
            checkLoginStatus();
        }
    });

    automationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        showLoading(true);
        const post_url = document.getElementById('post-url').value;
        const keywords = document.getElementById('keywords').value.split(',').map(k => k.trim());
        const comment_replies = document.getElementById('comment-replies').value.split('\n');
        const dm_replies = document.getElementById('dm-replies').value.split('\n');
        const followers_only = document.getElementById('followers-only').checked;
        const follow_message = document.getElementById('follow-message').value;

        try {
            const response = await fetch(`${API_BASE_URL}/automations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ post_url, keywords, comment_replies, dm_replies, followers_only, follow_message }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Failed to start automation.');
            showMessage(data.message);
            automationForm.reset();
            fetchActiveAutomations();
        } catch (error) {
            showMessage(error.message, true);
        } finally {
            showLoading(false);
        }
    });

    automationsList.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-btn')) {
            const taskId = e.target.dataset.taskId;
            if (confirm(`Are you sure you want to delete task ${taskId}?`)) {
                showLoading(true);
                try {
                    const response = await fetch(`${API_BASE_URL}/automations/${taskId}`, { method: 'DELETE' });
                    const data = await response.json();
                    if (!response.ok) throw new Error(data.message || 'Failed to delete task.');
                    showMessage(data.message);
                    fetchActiveAutomations();
                } catch (error) {
                    showMessage(error.message, true);
                } finally {
                    showLoading(false);
                }
            }
        }
    });

    refreshTasksBtn.addEventListener('click', fetchActiveAutomations);

    // Tab switching logic
    document.querySelectorAll('.tab-link').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-link').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            button.classList.add('active');
            document.getElementById(button.dataset.tab).classList.add('active');
        });
    });

    // --- Initial Load ---
    checkLoginStatus();
});
