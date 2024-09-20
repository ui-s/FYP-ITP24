// Global variables to store chart instances
let muscleGroupChart, bmiChart, totalRepsChart, workoutDurationChart;

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

// Function to create BMI Chart
function createBMIChart(chartData) {
    const ctx = document.getElementById('bmiChart').getContext('2d');
    bmiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Your BMI'],
            datasets: [{
                label: 'BMI',
                data: [chartData.bmi],
                backgroundColor: 'rgba(153, 102, 255, 0.6)'
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 40
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Your BMI'
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

// Function to update Muscle Group Chart
function updateMuscleGroupChart(chartData) {
    muscleGroupChart.data.datasets[0].data = chartData.muscle_group_sets;
    muscleGroupChart.update();
}

// Function to fetch data and update chart
function fetchDataAndUpdateChart(timePeriod) {
    fetch(`/get_chart_data?time_period=${timePeriod}`)
        .then(response => response.json())
        .then(data => {
            updateMuscleGroupChart(data);
        })
        .catch(error => console.error('Error:', error));
}

// Function to create all charts
function createCharts(chartData) {
    createMuscleGroupChart(chartData);
    createBMIChart(chartData);
    createTotalRepsChart(chartData);
    createWorkoutDurationChart(chartData);
}

// Event listeners for time period buttons
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-group button').forEach(button => {
        button.addEventListener('click', function() {
            const period = this.getAttribute('data-period');
            fetchDataAndUpdateChart(period);
        });
    });

    // Initial chart creation
    fetch('/get_chart_data')
        .then(response => response.json())
        .then(data => {
            createCharts(data);
        })
        .catch(error => console.error('Error:', error));
});