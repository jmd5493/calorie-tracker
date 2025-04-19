google.charts.load('current', { 'packages': ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  const data = new google.visualization.DataTable();
  data.addColumn('string', 'Time');
  data.addColumn('number', 'Human');
  data.addColumn('number', 'Vampire');

  // Example: Simulating data over time (e.g., days or sessions)
  data.addRows([
    ['Day 1', 60, 5],
    ['Day 2', 62, 6],
    ['Day 3', 63, 6],
    ['Day 4', 65, 7],
    ['Day 5', 66, 7]
  ]);

  const options = {
    title: 'Human vs Vampire Count Over Time',
    curveType: 'function',
    legend: { position: 'bottom' },
    width: 600,
    height: 400
  };

  const chart = new google.visualization.LineChart(document.getElementById('myChart'));
  chart.draw(data, options);
}