// --- Tabbing logic for login page ---
function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    const tablinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/api';

    // Sections
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');

    // Forms
    const credsLoginForm = document.getElementById('credentials-login-form');
    const sessionLoginForm = document.getElementById('session-login-form');
    const taskForm = document.getElementById('task-form');
    const webhookForm = document.getElementById('webhook-form');

    // Display Elements
    const statusDiv = document.getElementById('status');
    const usernameDisplay = document.getElementById('username-display');
    const taskList = document.getElementById('task-list');
    const webhookList = document.getElementById('webhook-list');

    // Buttons
    const logoutBtn = document.getElementById('logout-btn');

    // --- Main Logic ---
    async function apiRequest(endpoint, method = 'GET', body = null) {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' },
        };
        if (body) {
            options.body = JSON.stringify(body);
        }
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'An unknown error occurred');
        }
        return response.json();
    }

    function updateStatus(message, isError = false) {
        statusDiv.textContent = message;
        statusDiv.className = isError ? 'status-message error' : 'status-message';
    }

    function showDashboard(username) {
        loginSection.style.display = 'none';
        dashboardSection.style.display = 'block';
        usernameDisplay.textContent = username;
        loadTasks();
        loadWebhooks();
    }

    function showLogin() {
        loginSection.style.display = 'block';
        dashboardSection.style.display = 'none';
        updateStatus("Please log in to continue.");
    }

    // --- Event Handlers ---
    credsLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            updateStatus('Logging in...');
            const data = await apiRequest('/login/credentials', 'POST', { username, password });
            updateStatus(data.message);
            showDashboard(username);
        } catch (error) {
            updateStatus(`Login failed: ${error.message}`, true);
        }
    });

    sessionLoginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const sessionJson = document.getElementById('sessionJson').value;
        try {
            updateStatus('Logging in...');
            const data = await apiRequest('/login/session', 'POST', { session_json: sessionJson });
            updateStatus(data.message);
            // After session login, we need to get the username
            const statusData = await apiRequest('/status');
            showDashboard(statusData.username);
        } catch (error) {
            updateStatus(`Login failed: ${error.message}`, true);
        }
    });

    logoutBtn.addEventListener('click', async () => {
        try {
            const data = await apiRequest('/logout', 'POST');
            updateStatus(data.message);
        } catch (error) {
            updateStatus(`Logout failed: ${error.message}`, true);
        } finally {
            showLogin();
        }
    });

    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const post_url = document.getElementById('postUrl').value;
        const keywords = document.getElementById('keywords').value.split(',').map(k => k.trim()).filter(Boolean);
        const comment_replies = document.getElementById('commentReplies').value.split('\n').filter(Boolean);
        const dm_replies = document.getElementById('dmReplies').value.split('\n').filter(Boolean);
        const followers_only = document.getElementById('mustFollow').checked;

        try {
            const data = await apiRequest('/automations', 'POST', { post_url, keywords, comment_replies, dm_replies, followers_only });
            updateStatus('Task added successfully!');
            taskForm.reset();
            loadTasks();
        } catch (error) {
            updateStatus(`Error adding task: ${error.message}`, true);
        }
    });

    webhookForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('webhookUrl').value;
        try {
            await apiRequest('/webhooks', 'POST', { url });
            updateStatus('Webhook added successfully!');
            webhookForm.reset();
            loadWebhooks();
        } catch (error) {
            updateStatus(`Error adding webhook: ${error.message}`, true);
        }
    });

    async function loadTasks() {
        try {
            const tasks = await apiRequest('/automations');
            taskList.innerHTML = ''; // Clear
            Object.entries(tasks).forEach(([taskId, task]) => {
                const row = document.createElement('tr');
                // Add a class to the status cell based on the task status for styling
                row.innerHTML = `
                    <td><a href="${task.post_url}" target="_blank">${task.post_url.substring(0, 40)}...</a></td>
                    <td>${task.keywords.join(', ')}</td>
                    <td class="status-${task.status}">${task.status}</td>
                    <td><button class="btn btn-danger delete-task-btn" data-task-id="${taskId}">Delete</button></td>
                `;
                taskList.appendChild(row);
            });
            document.querySelectorAll('.delete-task-btn').forEach(btn => btn.addEventListener('click', handleDeleteTask));
        } catch (error) {
            updateStatus(`Could not load tasks: ${error.message}`, true);
        }
    }

    async function handleDeleteTask(e) {
        const taskId = e.target.dataset.taskId;
        if (confirm('Are you sure you want to delete this task?')) {
            try {
                await apiRequest(`/automations/${taskId}`, 'DELETE');
                updateStatus(`Task ${taskId} deleted.`);
                loadTasks();
            } catch (error) {
                updateStatus(`Error deleting task: ${error.message}`, true);
            }
        }
    }

    async function loadWebhooks() {
        try {
            const data = await apiRequest('/webhooks');
            webhookList.innerHTML = ''; // Clear
            data.webhooks.forEach(url => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${url}</span> <button class="btn btn-danger delete-webhook-btn" data-url="${url}">&times;</button>`;
                webhookList.appendChild(li);
            });
            document.querySelectorAll('.delete-webhook-btn').forEach(btn => btn.addEventListener('click', handleDeleteWebhook));
        } catch (error) {
            updateStatus(`Could not load webhooks: ${error.message}`, true);
        }
    }

    async function handleDeleteWebhook(e) {
        const url = e.target.dataset.url;
        if (confirm('Are you sure you want to delete this webhook?')) {
            try {
                await apiRequest('/webhooks', 'DELETE', { url });
                updateStatus('Webhook removed.');
                loadWebhooks();
            } catch (error) {
                updateStatus(`Error removing webhook: ${error.message}`, true);
            }
        }
    }

    // --- Initial Check ---
    (async () => {
        try {
            const data = await apiRequest('/status');
            if (data.status === 'logged_in') {
                showDashboard(data.username);
            } else {
                showLogin();
            }
        } catch (error) {
            showLogin();
            updateStatus('Server is offline or unreachable.', true);
        }
    })();
});
