// Global variables
let mainChart = null;
let currentIndicator = 'gdp';
let currentTimeRange = '1Y';

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Indicator mapping
const indicatorMap = {
    gdp: { name: 'GDP Growth Rate', unit: '%', source: 'RBI' },
    cpi: { name: 'Consumer Price Index', unit: '%', source: 'MOSPI' },
    gst: { name: 'GST Collections', unit: '₹ Lakh Cr', source: 'CBIC' },
    unemployment: { name: 'Unemployment Rate', unit: '%', source: 'CMIE' },
    forex: { name: 'Foreign Exchange Reserves', unit: 'Billion USD', source: 'RBI' },
    iip: { name: 'Index of Industrial Production', unit: '%', source: 'MOSPI' }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeChart();
    setupEventListeners();
    loadIndicatorData(currentIndicator, currentTimeRange);
});

// API Functions
async function fetchIndicatorData(indicator, timeRange = '1Y') {
    try {
        const response = await fetch(`${API_BASE_URL}/data/${indicator}?range=${timeRange}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching indicator data:', error);
        return null;
    }
}

async function loadIndicatorData(indicator, timeRange) {
    const data = await fetchIndicatorData(indicator, timeRange);
    
    if (data) {
        updateChart(data);
        updateStats(data.stats, indicator);
        updateHeader(data.indicator, timeRange);
    } else {
        // Fallback to sample data if API fails
        console.warn('Using fallback data due to API error');
        loadFallbackData(indicator, timeRange);
    }
}

function loadFallbackData(indicator, timeRange) {
    // Fallback data for when API is not available
    const fallbackData = {
        gdp: {
            labels: ['FY23 Q1', 'FY23 Q2', 'FY23 Q3', 'FY23 Q4'],
            data: [13.1, 6.2, 4.5, 6.0],
            stats: { latest: 6.0, highest: 13.1, lowest: 4.5, average: 7.45, change: -7.1 }
        },
        cpi: {
            labels: ['FY23 Q1', 'FY23 Q2', 'FY23 Q3', 'FY23 Q4'],
            data: [7.3, 7.0, 6.1, 5.9],
            stats: { latest: 5.9, highest: 7.3, lowest: 5.9, average: 6.575, change: -1.4 }
        }
    };
    
    const data = fallbackData[indicator] || fallbackData.gdp;
    updateChart(data);
    updateStats(data.stats, indicator);
    updateHeader(indicator, timeRange);
}

// Chart Functions
function initializeChart() {
    const ctx = document.getElementById('mainChart').getContext('2d');
    
    const chartConfig = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '',
                data: [],
                borderColor: '#ff8c42',
                backgroundColor: 'rgba(255, 140, 66, 0.1)',
                borderWidth: 3,
                pointRadius: 6,
                pointBackgroundColor: '#ff8c42',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            const indicator = indicatorMap[currentIndicator];
                            const unit = indicator ? indicator.unit : '%';
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}${unit}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#a0a9c5',
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#a0a9c5',
                        font: {
                            size: 12
                        },
                        callback: function(value) {
                            const indicator = indicatorMap[currentIndicator];
                            const unit = indicator ? indicator.unit : '%';
                            return value.toFixed(2) + (unit === '%' ? '%' : '');
                        }
                    }
                }
            }
        }
    };

    mainChart = new Chart(ctx, chartConfig);
}

function updateChart(data) {
    if (!mainChart || !data) return;
    
    const indicator = indicatorMap[currentIndicator];
    const unit = indicator ? indicator.unit : '%';
    
    mainChart.data.labels = data.labels || [];
    mainChart.data.datasets[0].data = data.data || [];
    mainChart.data.datasets[0].label = `${indicator ? indicator.name : 'Data'} (${unit})`;
    
    // Update Y-axis scale based on data
    const values = data.data.filter(v => v !== null && v !== undefined);
    if (values.length > 0) {
        const min = Math.min(...values);
        const max = Math.max(...values);
        const padding = (max - min) * 0.1;
        mainChart.options.scales.y.min = Math.max(0, min - padding);
        mainChart.options.scales.y.max = max + padding;
    }
    
    mainChart.update('active');
}

function updateStats(stats, indicator) {
    if (!stats) return;
    
    const indicatorInfo = indicatorMap[indicator];
    const unit = indicatorInfo ? indicatorInfo.unit : '%';
    
    // Update stat cards
    const statElements = document.querySelectorAll('.stat-value');
    if (statElements.length >= 4) {
        statElements[0].textContent = `${stats.latest}${unit === '%' ? '%' : ''}`;
        statElements[1].textContent = `${stats.highest}${unit === '%' ? '%' : ''}`;
        statElements[2].textContent = `${stats.lowest}${unit === '%' ? '%' : ''}`;
        statElements[3].textContent = `${stats.average}${unit === '%' ? '%' : ''}`;
        
        // Update change indicator
        if (statElements.length >= 5) {
            const changeElement = statElements[4];
            const changeValue = stats.change || 0;
            changeElement.textContent = `${changeValue >= 0 ? '+' : ''}${changeValue.toFixed(2)}${unit === '%' ? '%' : ''}`;
            changeElement.className = `stat-value change-indicator ${changeValue >= 0 ? 'positive' : 'negative'}`;
        }
    }
}

function updateHeader(indicator, timeRange) {
    const indicatorInfo = indicatorMap[indicator];
    if (indicatorInfo) {
        document.querySelector('.indicator-title').textContent = indicatorInfo.name;
        
        // Update date range based on time range
        const dateRange = getDateRangeLabel(timeRange);
        document.querySelector('.date-range').textContent = dateRange;
        
        // Update source
        const sourceElement = document.querySelector('.source-link');
        if (sourceElement) {
            sourceElement.textContent = `${getFrequencyLabel(timeRange)} • ${indicatorInfo.source}`;
        }
    }
}

function getDateRangeLabel(timeRange) {
    const now = new Date();
    const labels = {
        '3M': 'Last 3 Quarters',
        '1Y': 'Last 1 Year',
        '2Y': 'Last 2 Years',
        '5Y': 'Last 5 Years'
    };
    return labels[timeRange] || 'Recent Data';
}

function getFrequencyLabel(timeRange) {
    const labels = {
        '3M': 'Quarterly',
        '1Y': 'Quarterly',
        '2Y': 'Quarterly',
        '5Y': 'Quarterly'
    };
    return labels[timeRange] || 'Quarterly';
}

// Event Handlers
function setupEventListeners() {
    // Time range buttons
    document.querySelectorAll('.time-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.time-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const timeRange = this.getAttribute('data-range');
            currentTimeRange = timeRange;
            loadIndicatorData(currentIndicator, timeRange);
        });
    });

    // Indicator selector
    document.getElementById('indicatorSelect').addEventListener('change', function() {
        currentIndicator = this.value;
        loadIndicatorData(currentIndicator, currentTimeRange);
    });

    // Chart type selector
    document.getElementById('chartTypeSelect').addEventListener('change', function() {
        const chartType = this.value;
        updateChartType(chartType);
    });

    // Category pills
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', function() {
            document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function updateChartType(chartType) {
    if (!mainChart) return;
    
    switch(chartType) {
        case 'line':
            mainChart.config.type = 'line';
            mainChart.data.datasets[0].fill = false;
            break;
        case 'bar':
            mainChart.config.type = 'bar';
            mainChart.data.datasets[0].fill = false;
            break;
        case 'area':
            mainChart.config.type = 'line';
            mainChart.data.datasets[0].fill = true;
            break;
        case 'scatter':
            mainChart.config.type = 'scatter';
            mainChart.data.datasets[0].fill = false;
            break;
        default:
            mainChart.config.type = 'line';
            mainChart.data.datasets[0].fill = false;
    }
    
    mainChart.update();
}

function updateChart() {
    // This function is called by the Update Chart button
    loadIndicatorData(currentIndicator, currentTimeRange);
}

// Theme Functions
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    updateChartTheme(newTheme);
}

function updateChartTheme(theme) {
    if (!mainChart) return;
    
    const isLight = theme === 'light';
    const lineColor = isLight ? '#ea580c' : '#ff8c42';
    const bgColor = isLight ? 'rgba(234, 88, 12, 0.1)' : 'rgba(255, 140, 66, 0.1)';
    const gridColor = isLight ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.05)';
    const textColor = isLight ? '#475569' : '#a0a9c5';
    
    mainChart.data.datasets[0].borderColor = lineColor;
    mainChart.data.datasets[0].backgroundColor = bgColor;
    mainChart.data.datasets[0].pointBackgroundColor = lineColor;
    
    mainChart.options.scales.x.grid.color = gridColor;
    mainChart.options.scales.x.ticks.color = textColor;
    mainChart.options.scales.y.grid.color = gridColor;
    mainChart.options.scales.y.ticks.color = textColor;
    
    mainChart.update();
}

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateChartTheme(savedTheme);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 't') {
        e.preventDefault();
        toggleTheme();
    }
});