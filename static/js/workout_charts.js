// Global variables to store chart instances
let muscleGroupChart, bmiChart, totalRepsChart, workoutDurationChart;
let selectedCharts = ['muscleGroupChart',
    'bmiChart',
    'totalRepsChart',
    'workoutDurationChart',
    'muscleGroupChart',
    'averageWeightChart', 
    'totalRepsChart', 
    'workoutDurationChart',
    'bodyweightChart',
    'benchPRChart',
    'squatPRChart',
    'deadliftPRChart']

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

// Function to create Average Weight Chart (replacing BMI Chart)
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

// Function to create Workout Duration Chart
function createWorkoutDurationChart(chartData) {
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
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true
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

// Function to update charts
function updateCharts(chartData) {
    if (selectedCharts.includes('muscleGroupChart')) {
        muscleGroupChart.data.datasets[0].data = chartData.muscle_group_sets;
        muscleGroupChart.update();
    }
    if (selectedCharts.includes('averageWeightChart')) {
        averageWeightChart.data.datasets[0].data = [chartData.avg_weight];
        averageWeightChart.update();
    }
    if (selectedCharts.includes('totalRepsChart')) {
        totalRepsChart.data.labels = chartData.workout_days;
        totalRepsChart.data.datasets[0].data = chartData.total_reps;
        totalRepsChart.update();
    }
    if (selectedCharts.includes('workoutDurationChart')) {
        workoutDurationChart.data.labels = chartData.workout_days;
        workoutDurationChart.data.datasets[0].data = chartData.workout_durations;
        workoutDurationChart.update();
    }
    if (selectedCharts.includes('bodyweightChart')) {
        bodyweightChart.data.labels = chartData.bodyweight_data.map(d => d.Date);
        bodyweightChart.data.datasets[0].data = chartData.bodyweight_data.map(d => d.aftworkout_weight);
        bodyweightChart.update();
    }
    if (selectedCharts.includes('benchPRChart')) {
        benchPRChart.data.labels = chartData.bench_pr_data.map(d => d.Date);
        benchPRChart.data.datasets[0].data = chartData.bench_pr_data.map(d => d['Bench_pr(kg)']);
        benchPRChart.update();
    }
    if (selectedCharts.includes('squatPRChart')) {
        squatPRChart.data.labels = chartData.squat_pr_data.map(d => d.Date);
        squatPRChart.data.datasets[0].data = chartData.squat_pr_data.map(d => d['Squat_pr(kg)']);
        squatPRChart.update();
    }
    if (selectedCharts.includes('deadliftPRChart')) {
        deadliftPRChart.data.labels = chartData.deadlift_pr_data.map(d => d.Date);
        deadliftPRChart.data.datasets[0].data = chartData.deadlift_pr_data.map(d => d['Deadlift_pr(kg)']);
        deadliftPRChart.update();
    }
}

// Function to fetch data and update charts
function fetchDataAndUpdateCharts(timePeriod) {
    fetch(`/get_chart_data?time_period=${timePeriod}`)
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
        })
        .catch(error => console.error('Error:', error));
}

// Update the createCharts function to include the new charts
function createCharts(chartData) {
    createMuscleGroupChart(chartData);
    createAverageWeightChart(chartData);
    createTotalRepsChart(chartData);
    createWorkoutDurationChart(chartData);
    createBodyweightChart(chartData);
    createBenchPRChart(chartData);
    createSquatPRChart(chartData);
    createDeadliftPRChart(chartData);
}
// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const applyFilterBtn = document.getElementById('applyFilterBtn');
    const resetFilterBtn = document.getElementById('resetFilterBtn');
    const timePeriodSelect = document.getElementById('timePeriodSelect');
    const applyChartSelection = document.getElementById('applyChartSelection');

    applyFilterBtn.addEventListener('click', function() {
        const timePeriod = timePeriodSelect.value;
        fetchDataAndUpdateCharts(timePeriod);
    });

    resetFilterBtn.addEventListener('click', function() {
        timePeriodSelect.value = 'week';
        selectedCharts = ['muscleGroupChart', 'bmiChart', 'totalRepsChart', 'workoutDurationChart'];
        document.querySelectorAll('#filterModal input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = true;
        });
        fetchDataAndUpdateCharts('week');
    });

    applyChartSelection.addEventListener('click', function() {
        selectedCharts = Array.from(document.querySelectorAll('#filterModal input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
    });

    // Initial chart creation
    fetch('/get_chart_data')
        .then(response => response.json())
        .then(data => {
            createCharts(data);
        })
        .catch(error => console.error('Error:', error));
});