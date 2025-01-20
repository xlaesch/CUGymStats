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
        const d = new Date();
        let day = d.getDay();
        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        document.getElementById('dayOfWeek').innerText = `Data for: ${daysOfWeek[day]}`;

        const response = await fetch(`http://127.0.0.1:5000/api/average-occupancy?dayofweek=${day}`, {
            headers: {
                'x-api-key': 'your_generated_api_key'
            }
        });
        const data = await response.json();

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