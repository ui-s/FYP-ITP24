// Global variables to store chart instances
let muscleGroupChart, bmiChart, totalRepsChart, workoutDurationChart;
let selectedCharts = ['muscleGroupChart', 'bmiChart', 'totalRepsChart', 'workoutDurationChart'];

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

// Function to update charts
function updateCharts(chartData) {
    if (selectedCharts.includes('muscleGroupChart')) {
        muscleGroupChart.data.datasets[0].data = chartData.muscle_group_sets;
        muscleGroupChart.update();
    }
    if (selectedCharts.includes('bmiChart')) {
        bmiChart.data.datasets[0].data = [chartData.bmi];
        bmiChart.update();
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

// Function to create all charts
function createCharts(chartData) {
    createMuscleGroupChart(chartData);
    createBMIChart(chartData);
    createTotalRepsChart(chartData);
    createWorkoutDurationChart(chartData);
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