// Global variables to store chart instances

console.log("JavaScript is loaded!");

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0]; // Returns 'YYYY-MM-DD'
}

let muscleGroupChart, averageWeightChart, totalRepsChart, workoutDurationChart, bodyweightChart, benchPRChart, squatPRChart, deadliftPRChart, afterWorkoutWeightChart, totalWeightChart;
let selectedCharts = [
    'muscleGroupChart', 'workoutDurationChart', 'totalWeightChart', 'caloriesBurnedChart',
    'totalRepsChart', 'deadliftPRChart', 'benchPRChart', 'squatPRChart',
    'averageWeightChart', 'afterWorkoutWeightChart'
];

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
};

const chartInstances = {};

// Add the updateChartVisibility function here
function updateChartVisibility() {
    document.querySelectorAll('.chart-container').forEach(container => {
        const chartId = container.querySelector('canvas').id;
        container.style.display = selectedCharts.includes(chartId) ? 'block' : 'none';
    });
}

// Function to create Muscle Group Chart
function createMuscleGroupChart(chartData) {
    const ctx = document.getElementById('muscleGroupChart').getContext('2d');
    if (chartInstances.muscleGroupChart) {
        chartInstances.muscleGroupChart.destroy();
    }
    chartInstances.muscleGroupChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: chartData.muscle_groups,
            datasets: [{
                label: 'Sets per Muscle Group',
                data: chartData.muscle_group_sets,
                fill: true,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                pointBackgroundColor: 'rgb(54, 162, 235)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(54, 162, 235)'
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                title: {
                    display: true,
                    text: 'Muscle Groups Worked'
                }
            }
        }
    });
}


// Function to create Average Weight Chart 
function createAverageWeightChart(chartData) {
    const ctx = document.getElementById('averageWeightChart').getContext('2d');
    if (chartInstances.averageWeightChart) {
        chartInstances.averageWeightChart.destroy();
    }

    chartInstances.averageWeightChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Average Weight'],
            datasets: [{
                label: 'Weight (kg)',
                data: [chartData.avg_weight],
                backgroundColor: 'rgba(153, 102, 255, 0.6)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Average Weight After Workout'
                }
            }
        }
    });
}


// Function to create Total Reps Chart
function createTotalRepsChart(chartData) {
    const ctx = document.getElementById('totalRepsChart').getContext('2d');
    if (chartInstances.totalRepsChart) {
        chartInstances.totalRepsChart.destroy();
    }
    chartInstances.totalRepsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.workout_days,
            datasets: [{
                label: 'Total Reps',
                data: chartData.total_reps,
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Total Reps by Day'
                }
            }
        }
    });
}

function createWorkoutDurationChart(chartData) {
    console.log("Creating Workout Duration Chart with data:", chartData.workout_days, chartData.workout_durations);
    
    if (!chartData.workout_days || !chartData.workout_durations || chartData.workout_durations.length === 0) {
        console.warn('No workout duration data available');
        return;
    }

        const ctx = document.getElementById('workoutDurationChart').getContext('2d');
        if (chartInstances.workoutDurationChart) {
            chartInstances.workoutDurationChart.destroy();
        }
        chartInstances.workoutDurationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.workout_days,
            datasets: [{
                label: 'Workout Duration (minutes)',
                data: chartData.workout_durations,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Duration (minutes)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Workout Duration by Day'
                }
            }
        }
    });
}

// Function to create Bench Press PR Chart
function createBenchPRChart(chartData) {
    const ctx = document.getElementById('benchPRChart').getContext('2d');
    if (chartInstances.benchPRChart) {
        chartInstances.benchPRChart.destroy();
    }
    chartInstances.benchPRChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.bench_pr_data.map(d => d.Date),
            datasets: [{
                label: 'Bench Press PR (kg)',
                data: chartData.bench_pr_data.map(d => d['Bench_pr(kg)']),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Bench Press PR Progression'
                }
            }
        }
    });
}

// Function to create Squat PR Chart
function createSquatPRChart(chartData) {
    const ctx = document.getElementById('squatPRChart').getContext('2d');
    if (chartInstances.squatPRChart) {
        chartInstances.squatPRChart.destroy();
    }
    chartInstances.squatPRChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.squat_pr_data.map(d => d.Date),
            datasets: [{
                label: 'Squat PR (kg)',
                data: chartData.squat_pr_data.map(d => d['Squat_pr(kg)']),
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Squat PR Progression'
                }
            }
        }
    });
}

// Function to create Deadlift PR Chart
function createDeadliftPRChart(chartData) {
    const ctx = document.getElementById('deadliftPRChart').getContext('2d');
    if (chartInstances.deadliftPRChart) {
        chartInstances.deadliftPRChart.destroy();
    }
    chartInstances.deadliftPRChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.deadlift_pr_data.map(d => d.Date),
            datasets: [{
                label: 'Deadlift PR (kg)',
                data: chartData.deadlift_pr_data.map(d => d['Deadlift_pr(kg)']),
                borderColor: 'rgb(255, 206, 86)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Deadlift PR Progression'
                }
            }
        }
    });
}

function createAfterWorkoutWeightChart(chartData) {
    if (!chartData.after_workout_weight_data || chartData.after_workout_weight_data.length === 0) {
        console.warn('No after workout weight data available');
        return;
    }
        const ctx = document.getElementById('afterWorkoutWeightChart').getContext('2d');
        if (chartInstances.afterWorkoutWeightChart) {
            chartInstances.afterWorkoutWeightChart.destroy();
        }
        chartInstances.afterWorkoutWeightChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.after_workout_weight_data.map(d => d.Date),
            datasets: [{
                label: 'After-Workout Weight (kg)',
                data: chartData.after_workout_weight_data.map(d => d.aftworkout_weight),
                borderColor: 'rgb(153, 102, 255)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'After-Workout Weight Progression'
                }
            }
        }
    });
}

function createTotalWeightChart(chartData) {
    if (!chartData.workout_days || !chartData.total_weights || chartData.total_weights.length === 0) {
        console.warn('No total weight data available');
        return;
    }
        const ctx = document.getElementById('totalWeightChart').getContext('2d');
        if (chartInstances.totalWeightChart) {
            chartInstances.totalWeightChart.destroy();
        }
        chartInstances.totalWeightChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.workout_days,
            datasets: [{
                label: 'Total Weight (kg)',
                data: chartData.total_weights,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Total Weight Lifted by Day'
                }
            }
        }
    });
}

function createCaloriesBurnedChart(chartData) {
    if (!chartData.workout_days || !chartData.calories_burned || chartData.calories_burned.length === 0) {
        console.warn('No calories burned data available');
        return;
    }

    const ctx = document.getElementById('caloriesBurnedChart').getContext('2d');
    if (chartInstances.caloriesBurnedChart) {
        chartInstances.caloriesBurnedChart.destroy();
    }
    chartInstances.caloriesBurnedChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.workout_days,
            datasets: [{
                label: 'Calories Burned',
                data: chartData.calories_burned,
                borderColor: 'rgb(255, 159, 64)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Calories'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Calories Burned per Workout'
                }
            }
        }
    });
}

function createCharts(chartData) {
    console.log("Creating charts with data:", chartData);
    try {
        if (!chartData || typeof chartData !== 'object') {
            throw new Error('Invalid chart data received');
        }

        const chartCreationFunctions = {
            muscleGroupChart: createMuscleGroupChart,
            workoutDurationChart: createWorkoutDurationChart,
            totalWeightChart: createTotalWeightChart,
            caloriesBurnedChart: createCaloriesBurnedChart,
            totalRepsChart: createTotalRepsChart,
            deadliftPRChart: createDeadliftPRChart,
            benchPRChart: createBenchPRChart,
            squatPRChart: createSquatPRChart,
            averageWeightChart: createAverageWeightChart,
            afterWorkoutWeightChart: createAfterWorkoutWeightChart
        };

        for (const [chartId, createFunction] of Object.entries(chartCreationFunctions)) {
            if (document.getElementById(chartId)) {
                try {
                    createFunction(chartData);
                    console.log(`Successfully created/updated ${chartId}`);
                } catch (error) {
                    console.error(`Error creating/updating ${chartId}:`, error);
                }
            } else {
                console.warn(`Chart container for ${chartId} not found in the DOM`);
            }
        }

        document.getElementById('chartsContainer').style.display = 'block';
        updateChartVisibility();
    } catch (error) {
        console.error("Error in createCharts:", error);
        alert("An error occurred while creating the charts. Please check the console for more details.");
    }
}

function updateCharts(chartData) {
    console.log("Updating charts with data:", chartData);
    createCharts(chartData);  // Reuse createCharts to update or create as needed
}

function loadCharts() {
    const usernameInput = document.getElementById('usernameInput');
    const timePeriodSelect = document.getElementById('timePeriodSelect');
    const username = usernameInput.value.trim();
    const timePeriod = timePeriodSelect.value;
    
    if (username) {
        console.log(`Loading charts for Username: ${username}, Time Period: ${timePeriod}`);
        fetchDataAndUpdateCharts(username, timePeriod);
    } else {
        console.log('No username provided');
        chartsContainer.style.display = 'none';
    }
}

function fetchDataAndUpdateCharts(username, timePeriod) {
    console.log(`Fetching data for username ${username} and time period ${timePeriod}`);
    fetch(`/get_chart_data?username=${encodeURIComponent(username)}&time_period=${timePeriod}`)
        .then(response => {
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('No workout data found for this user.');
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);
            if (data.error) {
                throw new Error(data.error);
            }
            updateCharts(data);
            chartsContainer.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`An error occurred while fetching data: ${error.message}`);
            chartsContainer.style.display = 'none';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const applyFilterBtn = document.getElementById('applyFilterBtn');
    const resetFilterBtn = document.getElementById('resetFilterBtn');
    const timePeriodSelect = document.getElementById('timePeriodSelect');
    const usernameInput = document.getElementById('usernameInput');
    const applyChartSelection = document.getElementById('applyChartSelection');
    const chartsContainer = document.getElementById('chartsContainer');
    
    if (!chartsContainer) {
        console.log('No charts container found. User might not have workout data yet.');
        return;  // Exit early if there's no charts container
    }

    // Auto-load charts if username is present
    const sessionUsername = usernameInput.dataset.sessionUsername;
    if (sessionUsername) {
        console.log(`Session username found: ${sessionUsername}`);
        usernameInput.value = sessionUsername;
        loadCharts();
    } else {
        console.log('No session username found');
    }

    // Apply filter button event listener
    if (applyFilterBtn) {
        applyFilterBtn.addEventListener('click', loadCharts);
    }

    // Reset filter button event listener
    if (resetFilterBtn) {
        resetFilterBtn.addEventListener('click', function() {
            usernameInput.value = sessionUsername || '';  // Reset to session username or empty string
            timePeriodSelect.value = '7days';
            selectedCharts = [
                'muscleGroupChart', 'workoutDurationChart', 'totalWeightChart', 'caloriesBurnedChart',
                'totalRepsChart', 'deadliftPRChart', 'benchPRChart', 'squatPRChart',
                'averageWeightChart', 'afterWorkoutWeightChart'
            ];
            document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = true;
            });
            if (sessionUsername) {
                loadCharts();  // Reload charts if session username exists
            } else {
                chartsContainer.style.display = 'none';
            }
            updateChartVisibility();  // Add this line to update chart visibility after reset
        });
    }

    if (applyChartSelection) {
        applyChartSelection.addEventListener('click', function() {
            selectedCharts = Array.from(document.querySelectorAll('#filterModal input[type="checkbox"]:checked'))
                                 .map(checkbox => checkbox.value);
            updateChartVisibility();
        });
    }
});