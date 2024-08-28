// Muscle Group Chart
function createMuscleGroupChart(chartData) {
    new Chart(document.getElementById('muscleGroupChart'), {
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
            plugins: {
                title: {
                    display: true,
                    text: 'Muscle Groups Worked This Week'
                }
            }
        }
    });
}

// Workout Duration Chart
function createWorkoutDurationChart(chartData) {
    new Chart(document.getElementById('workoutDurationChart'), {
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

// Total Reps Chart
function createTotalRepsChart(chartData) {
    new Chart(document.getElementById('totalRepsChart'), {
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

// BMI Chart
function createBMIChart(chartData) {
    new Chart(document.getElementById('bmiChart'), {
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

// Function to create all charts
function createCharts(chartData) {
    createMuscleGroupChart(chartData);
    createWorkoutDurationChart(chartData);
    createTotalRepsChart(chartData);
    createBMIChart(chartData);
}