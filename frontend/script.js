document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/api'; // Use a relative path to go through the Nginx proxy
    const loginForm = document.getElementById('login-form');
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const statusDiv = document.getElementById('status');

    // --- Check login status on page load ---
    checkLoginStatus();

    // --- Event Listeners ---
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    if (taskForm) {
        taskForm.addEventListener('submit', handleAddTask);
    }

    // --- Functions ---
    async function checkLoginStatus() {
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            if (response.ok) {
                const data = await response.json();
                if (data.status === 'logged_in') {
                    showDashboard(data.username);
                    loadTasks();
                } else {
                    showLogin();
                }
            } else {
                showLogin();
            }
        } catch (error) {
            console.error('Error checking login status:', error);
            statusDiv.textContent = 'Error connecting to the server.';
            showLogin();
        }
    }

    async function handleLogin(event) {
        event.preventDefault();
        const username = event.target.username.value;
        const password = event.target.password.value;
        statusDiv.textContent = 'Logging in...';

        try {
            const response = await fetch(`${API_BASE_URL}/login/credentials`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (response.ok) {
                statusDiv.textContent = `Logged in as ${username}`;
                showDashboard(username);
                loadTasks();
            } else {
                statusDiv.textContent = `Login failed: ${data.message}`;
            }
        } catch (error) {
            console.error('Login error:', error);
            statusDiv.textContent = 'An error occurred during login.';
        }
    }

    async function handleAddTask(event) {
        event.preventDefault();
        const postUrl = document.getElementById('postUrl').value;
        const keywords = document.getElementById('keywords').value.split(',').map(k => k.trim());
        const replyMessage = document.getElementById('replyMessage').value;
        const dmMessage = document.getElementById('dmMessage').value;
        const mustFollow = document.getElementById('mustFollow').checked;

        const taskData = {
            post_url: postUrl,
            keywords: keywords,
            comment_replies: [replyMessage], // API expects a list
            dm_replies: [dmMessage],       // API expects a list
            followers_only: mustFollow,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/automations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData),
            });

            if (response.ok) {
                statusDiv.textContent = 'Task added successfully!';
                loadTasks();
                taskForm.reset();
            } else {
                const errorData = await response.json();
                statusDiv.textContent = `Error adding task: ${errorData.message}`;
            }
        } catch (error) {
            console.error('Error adding task:', error);
            statusDiv.textContent = 'An error occurred while adding the task.';
        }
    }

    async function loadTasks() {
        try {
            const response = await fetch(`${API_BASE_URL}/automations`);
            if (response.ok) {
                const tasks = await response.json();
                renderTasks(tasks);
            } else {
                statusDiv.textContent = 'Could not load tasks.';
            }
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    function renderTasks(tasks) {
        taskList.innerHTML = ''; // Clear existing list
        for (const taskId in tasks) {
            const task = tasks[taskId];
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><a href="${task.post_url}" target="_blank">${task.post_url.substring(0, 40)}...</a></td>
                <td>${task.keywords.join(', ')}</td>
                <td>${task.is_running ? 'Running' : 'Stopped'}</td>
                <td><button class="delete-btn" data-task-id="${taskId}">Delete</button></td>
            `;
            taskList.appendChild(row);
        }

        // Add event listeners to delete buttons
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', handleDeleteTask);
        });
    }

    async function handleDeleteTask(event) {
        const taskId = event.target.dataset.taskId;
        if (!confirm(`Are you sure you want to delete task ${taskId}?`)) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/automations/${taskId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                statusDiv.textContent = `Task ${taskId} deleted.`;
                loadTasks();
            } else {
                const errorData = await response.json();
                statusDiv.textContent = `Error deleting task: ${errorData.message}`;
            }
        } catch (error) {
            console.error('Error deleting task:', error);
            statusDiv.textContent = 'An error occurred while deleting the task.';
        }
    }

    function showDashboard(username) {
        loginSection.style.display = 'none';
        dashboardSection.style.display = 'block';
        document.getElementById('username-display').textContent = username;
    }

    function showLogin() {
        loginSection.style.display = 'block';
        dashboardSection.style.display = 'none';
    }
});
