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

async function fetchData(day) {
    try {
        const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        document.getElementById('dayOfWeek').innerText = `Data for: ${daysOfWeek[day]}`;

        // Remove API key request - send request directly
        const response = await fetch(`http://127.0.0.1:5000/api/average-occupancy?dayofweek=${day}`);
        
        // Handle unauthorized error
        if (response.status === 401) {
            console.error('Unauthorized access');
            return;
        }
        
        const data = await response.json();

        const labels = data.map(item => item.hour);
        const avgPercentages = data.map(item => item.avg_percentage);

        // Find optimal time (lowest occupancy)
        let lowestIndex = 0;
        for (let i = 1; i < avgPercentages.length; i++) {
            if (avgPercentages[i] < avgPercentages[lowestIndex]) {
                lowestIndex = i;
            }
        }
        
        // Format the hour properly (convert 24h to 12h format)
        const optimalHour = labels[lowestIndex];
        const formattedHour = formatHour(optimalHour);
        const optimalPercentage = avgPercentages[lowestIndex].toFixed(1);
        
        // Display optimal time info
        document.getElementById('optimalTimeInfo').innerHTML = 
            `<strong>Optimal Time:</strong> The gym is least busy on ${daysOfWeek[day]} at <strong>${formattedHour}</strong> with average occupancy of <strong>${optimalPercentage}%</strong>.`;

        myChart.data.labels = labels;
        myChart.data.datasets[0].data = avgPercentages;
        myChart.update();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Helper function to format hours from 24h to 12h format
function formatHour(hour) {
    const hourNum = parseInt(hour);
    if (hourNum === 0) return '12 AM';
    if (hourNum === 12) return '12 PM';
    if (hourNum < 12) return `${hourNum} AM`;
    return `${hourNum - 12} PM`;
}

// Set up dropdown and initial fetch
window.addEventListener('DOMContentLoaded', () => {
    const daySelector = document.getElementById('daySelector');
    const today = new Date().getDay();
    daySelector.value = today;
    fetchData(today);

    daySelector.addEventListener('change', (e) => {
        fetchData(Number(e.target.value));
    });
});