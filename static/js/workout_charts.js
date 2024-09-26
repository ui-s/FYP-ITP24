// Global variables to store chart instances

console.log("JavaScript is loaded!");

let muscleGroupChart, averageWeightChart, totalRepsChart, workoutDurationChart, bodyweightChart, benchPRChart, squatPRChart, deadliftPRChart, afterWorkoutWeightChart, totalWeightChart;
let selectedCharts = [
    'muscleGroupChart',
    'averageWeightChart', 
    'totalRepsChart', 
    'workoutDurationChart',
    'bodyweightChart',
    'benchPRChart',
    'squatPRChart',
    'deadliftPRChart',
    'afterWorkoutWeightChart',
    'totalWeightChart'
    
];

// Common chart options
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
};

// Function to create Muscle Group Chart
function createMuscleGroupChart(chartData) {
    const ctx = document.getElementById('muscleGroupChart').getContext('2d');
    muscleGroupChart = new Chart(ctx, {
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
    new Chart(ctx, {
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
    totalRepsChart = new Chart(ctx, {
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
    workoutDurationChart = new Chart(ctx, {
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

// Function to create Bodyweight Line Chart
function createBodyweightChart(chartData) {
    const ctx = document.getElementById('bodyweightChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.bodyweight_data.map(d => d.Date),
            datasets: [{
                label: 'Bodyweight (kg)',
                data: chartData.bodyweight_data.map(d => d.aftworkout_weight),
                borderColor: 'rgb(75, 192, 192)',
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
                    text: 'Bodyweight Progression'
                }
            }
        }
    });
}

// Function to create Bench Press PR Chart
function createBenchPRChart(chartData) {
    const ctx = document.getElementById('benchPRChart').getContext('2d');
    new Chart(ctx, {
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
    new Chart(ctx, {
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
    new Chart(ctx, {
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
    afterWorkoutWeightChart = new Chart(ctx, {
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
    totalWeightChart = new Chart(ctx, {
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

function createCharts(chartData) {
    createMuscleGroupChart(chartData);
    createAverageWeightChart(chartData);
    createTotalRepsChart(chartData);
    createWorkoutDurationChart(chartData);
    createBodyweightChart(chartData);
    createBenchPRChart(chartData);
    createSquatPRChart(chartData);
    createDeadliftPRChart(chartData);
    createAfterWorkoutWeightChart(chartData);
    createTotalWeightChart(chartData);
}

console.log("JavaScript is loaded!");
console.log("JavaScript is loaded!");

function fetchDataAndUpdateCharts(userId, timePeriod) {
    console.log(`Fetching data for user ${userId} and time period ${timePeriod}`);
    fetch(`/get_chart_data?user_id=${userId}&time_period=${timePeriod}`)
        .then(response => {
            if (!response.ok) {
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
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching data. Please try again.');
        });
}

    console.log("JavaScript is loaded!");

    document.addEventListener('DOMContentLoaded', function() {
        const applyFilterBtn = document.getElementById('applyFilterBtn');
        const resetFilterBtn = document.getElementById('resetFilterBtn');
        const timePeriodSelect = document.getElementById('timePeriodSelect');
        const userIdInput = document.getElementById('userIdInput');
        const chartSelect = document.getElementById('chartSelect');
        const applyChartSelection = document.getElementById('applyChartSelection');
    
        // Check if 'applyFilterBtn' exists before adding the event listener
        if (applyFilterBtn) {
            applyFilterBtn.addEventListener('click', function() {
                console.log('Apply Filter button clicked!'); // Debug log
    
                const userId = userIdInput ? userIdInput.value : null;
                const timePeriod = timePeriodSelect ? timePeriodSelect.value : '7days';
                const selectedChart = chartSelect ? chartSelect.value : 'all';
    
                console.log(`User ID: ${userId}, Time Period: ${timePeriod}, Selected Chart: ${selectedChart}`);
    
                // Call to update charts
                fetchDataAndUpdateCharts(userId, timePeriod);
    
                // Show/hide charts based on selection
                document.querySelectorAll('.chart-container').forEach(container => {
                    const chartId = container.querySelector('canvas').id;
                    if (selectedChart === 'all') {
                        container.style.display = 'block';
                    } else {
                        container.style.display = chartId === selectedChart ? 'block' : 'none';
                    }
                });
            });
        } else {
            console.error('Apply Filter button not found');
        }
    
        // Add the reset button logic
        if (resetFilterBtn) {
            resetFilterBtn.addEventListener('click', function() {
                console.log('Reset Filter button clicked!');
                if (userIdInput) userIdInput.value = '';
                if (timePeriodSelect) timePeriodSelect.value = '7days';
                if (chartSelect) chartSelect.value = 'all';
    
                fetchDataAndUpdateCharts('', '7days');
    
                document.querySelectorAll('.chart-container').forEach(container => {
                    container.style.display = 'block';
                });
            });
        } else {
            console.error('Reset Filter button not found');
        }
    
        // Chart selection logic
        if (applyChartSelection) {
            applyChartSelection.addEventListener('click', function() {
                selectedCharts = Array.from(document.querySelectorAll('#filterModal input[type="checkbox"]:checked'))
                                     .map(checkbox => checkbox.value);
                document.querySelectorAll('.chart-container').forEach(container => {
                    const chartId = container.querySelector('canvas').id;
                    container.style.display = selectedCharts.includes(chartId) ? 'block' : 'none';
                });
            });
        } else {
            console.error('Apply Chart Selection button not found');
        }
    
        // Fetch initial chart data on load
        fetch('/get_chart_data')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            createCharts(data);
        })
        .catch(error => {
            console.error('Error fetching chart data:', error);
            alert('An error occurred while loading initial chart data. Please refresh the page.');
        });
    
        console.log("JavaScript is loaded!");
    });
    
    function updateCharts(chartData) {
    console.log("Updating charts with data:", chartData);

    if (selectedCharts.includes('muscleGroupChart') && chartData.muscle_group_sets) {
        if (muscleGroupChart) {
            muscleGroupChart.data.datasets[0].data = chartData.muscle_group_sets;
            muscleGroupChart.update();
        } else {
            console.log("Creating muscleGroupChart as it doesn't exist");
            createMuscleGroupChart(chartData);
        }
    }

    if (selectedCharts.includes('averageWeightChart') && chartData.avg_weight !== undefined) {
        if (averageWeightChart) {
            averageWeightChart.data.datasets[0].data = [chartData.avg_weight];
            averageWeightChart.update();
        } else {
            console.log("Creating averageWeightChart as it doesn't exist");
            createAverageWeightChart(chartData);
        }
    }

    if (selectedCharts.includes('totalRepsChart') && chartData.workout_days && chartData.total_reps) {
        if (totalRepsChart) {
            totalRepsChart.data.labels = chartData.workout_days.map(formatDate);
            totalRepsChart.data.datasets[0].data = chartData.total_reps;
            totalRepsChart.update();
        } else {
            console.log("Creating totalRepsChart as it doesn't exist");
            createTotalRepsChart(chartData);
        }
    }

    if (selectedCharts.includes('workoutDurationChart') && chartData.workout_days && chartData.workout_durations) {
        if (workoutDurationChart) {
            workoutDurationChart.data.labels = chartData.workout_days.map(formatDate);
            workoutDurationChart.data.datasets[0].data = chartData.workout_durations;
            workoutDurationChart.update();
        } else {
            console.log("Creating workoutDurationChart as it doesn't exist");
            createWorkoutDurationChart(chartData);
        }
    }

    if (selectedCharts.includes('bodyweightChart') && chartData.bodyweight_data) {
        if (bodyweightChart) {
            bodyweightChart.data.labels = chartData.bodyweight_data.map(d => formatDate(d.Date));
            bodyweightChart.data.datasets[0].data = chartData.bodyweight_data.map(d => d.aftworkout_weight);
            bodyweightChart.update();
        } else {
            console.log("Creating bodyweightChart as it doesn't exist");
            createBodyweightChart(chartData);
        }
    }

    if (selectedCharts.includes('benchPRChart') && chartData.bench_pr_data) {
        if (benchPRChart) {
            benchPRChart.data.labels = chartData.bench_pr_data.map(d => formatDate(d.Date));
            benchPRChart.data.datasets[0].data = chartData.bench_pr_data.map(d => d['Bench_pr(kg)']);
            benchPRChart.update();
        } else {
            console.log("Creating benchPRChart as it doesn't exist");
            createBenchPRChart(chartData);
        }
    }

    if (selectedCharts.includes('squatPRChart') && chartData.squat_pr_data) {
        if (squatPRChart) {
            squatPRChart.data.labels = chartData.squat_pr_data.map(d => formatDate(d.Date));
            squatPRChart.data.datasets[0].data = chartData.squat_pr_data.map(d => d['Squat_pr(kg)']);
            squatPRChart.update();
        } else {
            console.log("Creating squatPRChart as it doesn't exist");
            createSquatPRChart(chartData);
        }
    }

    if (selectedCharts.includes('deadliftPRChart') && chartData.deadlift_pr_data) {
        if (deadliftPRChart) {
            deadliftPRChart.data.labels = chartData.deadlift_pr_data.map(d => formatDate(d.Date));
            deadliftPRChart.data.datasets[0].data = chartData.deadlift_pr_data.map(d => d['Deadlift_pr(kg)']);
            deadliftPRChart.update();
        } else {
            console.log("Creating deadliftPRChart as it doesn't exist");
            createDeadliftPRChart(chartData);
        }
    }

    if (selectedCharts.includes('afterWorkoutWeightChart') && chartData.after_workout_weight_data) {
        if (afterWorkoutWeightChart) {
            afterWorkoutWeightChart.data.labels = chartData.after_workout_weight_data.map(d => formatDate(d.Date));
            afterWorkoutWeightChart.data.datasets[0].data = chartData.after_workout_weight_data.map(d => d.aftworkout_weight);
            afterWorkoutWeightChart.update();
        } else {
            console.log("Creating afterWorkoutWeightChart as it doesn't exist");
            createAfterWorkoutWeightChart(chartData);
        }
    }

    if (selectedCharts.includes('totalWeightChart') && chartData.workout_days && chartData.total_weights) {
        if (totalWeightChart) {
            totalWeightChart.data.labels = chartData.workout_days.map(formatDate);
            totalWeightChart.data.datasets[0].data = chartData.total_weights;
            totalWeightChart.update();
        } else {
            console.log("Creating totalWeightChart as it doesn't exist");
            createTotalWeightChart(chartData);
        }
    }
}
    
    function fetchDataAndUpdateCharts(userId, timePeriod) {
        console.log(`Fetching data for user ${userId} and time period ${timePeriod}`);
        fetch(`/get_chart_data?user_id=${userId}&time_period=${timePeriod}`)
            .then(response => {
                if (!response.ok) {
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
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching data. Please try again.');
            });
    }


