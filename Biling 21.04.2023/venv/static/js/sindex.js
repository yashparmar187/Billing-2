/**
 * Main JavaScript for Ministore Seller Dashboard
 * Handles chart initialization and product interactions.
 */
(function($) {
  "use strict";

  $(document).ready(function() {
    // Initialize Sales Chart
    if (typeof Chart !== 'undefined') {
      var ctx = document.getElementById('salesChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr'],
          datasets: [{
            label: 'Sales ($)',
            data: [1000, 1500, 2000, 2500],
            borderColor: '#72AEC8',
            backgroundColor: 'rgba(114, 174, 200, 0.2)',
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }

    // Product Card Hover Effect
    $('.product-card').hover(
      function() {
        $(this).find('.btn').css('visibility', 'visible');
      },
      function() {
        $(this).find('.btn').css('visibility', 'hidden');
      }
    );
  });
})(jQuery);