const ctx = document.getElementById('myChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Average Occupancy',
            data: [],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/average-occupancy?dayofweek=0');
        console.log('Response:', response);
        const data = await response.json();
        console.log('Data:', data);

        const labels = data.map(item => item.hour);
        const avgPercentages = data.map(item => item.avg_percentage);

        myChart.data.labels = labels;
        myChart.data.datasets[0].data = avgPercentages;
        myChart.update();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetchData();