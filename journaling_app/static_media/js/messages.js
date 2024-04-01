document.addEventListener('DOMContentLoaded', function () {
    // Initialize all toasts
    var toasts = document.querySelectorAll('.toast');
    var toastList = Array.prototype.map.call(toasts, function (toastEl) {
      return new bootstrap.Toast(toastEl);
    });
  
    // Show toasts when they are in the DOM
    toastList.forEach(function (toast) {
      toast.show();
    });
});