// Global variables
let priceChart = null;
let predictionHistory = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    initializeChart();
    
    // Form submission
    document.getElementById('predictionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        predictPrice();
    });
});

// Predict price function
async function predictPrice() {
    const location = document.getElementById('location').value;
    const sqft = document.getElementById('sqft').value;
    const bath = document.getElementById('bath').value;
    const bhk = document.getElementById('bhk').value;
    
    if (!location || !sqft || !bath || !bhk) {
        showAlert('Please fill all fields', 'warning');
        return;
    }
    
    const resultCard = document.getElementById('resultCard');
    resultCard.innerHTML = '<div class="text-center p-5"><div class="loading"></div><p class="mt-3">Calculating...</p></div>';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                sqft: parseFloat(sqft),
                bath: parseInt(bath),
                bhk: parseInt(bhk)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data);
            predictionHistory.push(data.predicted_price);
            updateChart();
        } else {
            showAlert('Error: ' + data.error, 'danger');
            resultCard.innerHTML = '<div class="result-placeholder"><i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i><p class="text-danger">Prediction failed</p></div>';
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
        resultCard.innerHTML = '<div class="result-placeholder"><i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i><p class="text-danger">Network error</p></div>';
    }
}

// Display prediction result
function displayResult(data) {
    const resultCard = document.getElementById('resultCard');
    resultCard.innerHTML = `
        <div class="result-content">
            <i class="fas fa-check-circle fa-3x text-success mb-3"></i>
            <h5>Estimated Price</h5>
            <div class="price-display">₹${data.predicted_price.toFixed(2)} L</div>
            <div class="price-per-sqft">
                <i class="fas fa-chart-line"></i> ₹${data.price_per_sqft.toFixed(2)} per sqft
            </div>
            <div class="mt-4">
                <small class="text-muted">
                    <i class="fas fa-info-circle"></i> Price in Lakhs (1L = 100,000)
                </small>
            </div>
        </div>
    `;
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('totalRecords').textContent = data.stats.total_records.toLocaleString();
            document.getElementById('totalLocations').textContent = data.stats.locations;
            document.getElementById('avgPrice').textContent = '₹' + data.stats.avg_price.toFixed(2) + 'L';
            document.getElementById('priceRange').textContent = 
                '₹' + data.stats.price_range.min.toFixed(0) + 'L - ₹' + data.stats.price_range.max.toFixed(0) + 'L';
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Initialize chart
function initializeChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Predicted Prices (Lakhs)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Your Prediction History'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Price (Lakhs)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Prediction Number'
                    }
                }
            }
        }
    });
}

// Update chart with new prediction
function updateChart() {
    if (predictionHistory.length > 10) {
        predictionHistory.shift();
    }
    
    priceChart.data.labels = predictionHistory.map((_, i) => `#${i + 1}`);
    priceChart.data.datasets[0].data = predictionHistory;
    priceChart.update();
}

// Show alert message
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Run DSA Demo
async function runDSADemo() {
    const resultsDiv = document.getElementById('dsaResults');
    const outputPre = document.getElementById('dsaOutput');
    
    // Check if we have prediction history
    if (predictionHistory.length === 0) {
        outputPre.textContent = '⚠️  No predictions yet!\n\nPlease make some price predictions first, then run this demo to see DSA algorithms in action on your prediction data.';
        resultsDiv.style.display = 'block';
        return;
    }
    
    resultsDiv.style.display = 'block';
    outputPre.textContent = 'Running algorithms on your predictions...\n';
    
    try {
        const response = await fetch('/dsa-demo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prices: predictionHistory,
                target: predictionHistory[0] // Search for first prediction
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            let output = '';
            output += '═══════════════════════════════════════════\n';
            output += '  DSA ALGORITHMS ON YOUR PREDICTIONS\n';
            output += '═══════════════════════════════════════════\n\n';
            
            output += `📊 Your ${data.original.length} Predictions (Lakhs):\n`;
            output += `   ${data.original.map(p => p.toFixed(2)).join(', ')}\n\n`;
            
            output += '🔄 HEAP SORT - O(n log n)\n';
            output += `   Sorted: ${data.sorted.map(p => p.toFixed(2)).join(', ')}\n`;
            output += '   ✓ Predictions sorted from lowest to highest\n\n';
            
            output += '🔍 BINARY SEARCH - O(log n)\n';
            output += `   Searching for: ₹${data.binary_search.target.toFixed(2)} Lakhs\n`;
            if (data.binary_search.found) {
                output += `   ✓ Found at index: ${data.binary_search.found_at_index}\n`;
                output += `   This was your ${data.original.indexOf(data.binary_search.target) + 1}${getOrdinalSuffix(data.original.indexOf(data.binary_search.target) + 1)} prediction\n`;
            } else {
                output += `   ✗ Not found in sorted array\n`;
            }
            output += '\n';
            
            output += '🏆 KTH LARGEST ELEMENT\n';
            if (data.original.length >= 3) {
                output += `   3rd Highest Price: ₹${data.top_3_price.toFixed(2)} Lakhs\n`;
                output += '   ✓ Found using Heap Sort algorithm\n';
            } else {
                output += `   Highest Price: ₹${data.sorted[data.sorted.length - 1].toFixed(2)} Lakhs\n`;
                output += `   (Need at least 3 predictions for 3rd highest)\n`;
            }
            output += '\n';
            
            output += '📈 ANALYSIS:\n';
            output += `   Lowest:  ₹${data.sorted[0].toFixed(2)} Lakhs\n`;
            output += `   Highest: ₹${data.sorted[data.sorted.length - 1].toFixed(2)} Lakhs\n`;
            output += `   Range:   ₹${(data.sorted[data.sorted.length - 1] - data.sorted[0]).toFixed(2)} Lakhs\n\n`;
            
            output += '═══════════════════════════════════════════\n';
            output += '  All algorithms executed successfully!\n';
            output += '═══════════════════════════════════════════\n';
            
            outputPre.textContent = output;
        } else {
            outputPre.textContent = 'Error: ' + data.error;
        }
    } catch (error) {
        outputPre.textContent = 'Error running demo: ' + error.message;
    }
}

// Helper function for ordinal suffix
function getOrdinalSuffix(num) {
    const j = num % 10;
    const k = num % 100;
    if (j === 1 && k !== 11) return 'st';
    if (j === 2 && k !== 12) return 'nd';
    if (j === 3 && k !== 13) return 'rd';
    return 'th';
}
