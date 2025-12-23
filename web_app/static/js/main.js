// AI Study Pal - Main JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Smooth scrolling for anchor links
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

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add loading states to buttons (but allow form submission)
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        const form = button.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                const originalText = button.innerHTML;
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
                button.disabled = true;
                
                // Re-enable after 30 seconds as fallback
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.disabled = false;
                }, 30000);
            });
        }
    });
});

// Quiz functionality
function checkQuizAnswers() {
    const form = document.getElementById('quizForm');
    if (!form) return;

    const formData = new FormData(form);
    const answers = {};
    
    // Collect answers
    for (let [key, value] of formData.entries()) {
        const questionIndex = key.split('_')[1];
        answers[questionIndex] = parseInt(value);
    }
    
    // Validate that all questions are answered
    const totalQuestions = form.querySelectorAll('.question-block').length;
    if (Object.keys(answers).length < totalQuestions) {
        showAlert('Please answer all questions before checking results.', 'warning');
        return;
    }
    
    // Show loading state
    const checkButton = document.querySelector('button[onclick="checkQuizAnswers()"]');
    const originalText = checkButton.innerHTML;
    checkButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Checking...';
    checkButton.disabled = true;
    
    // Send to server for checking
    fetch('/api/quiz_check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({answers: answers})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayQuizResults(data);
        highlightAnswers(data.results);
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error checking answers. Please try again.', 'danger');
    })
    .finally(() => {
        // Restore button state
        checkButton.innerHTML = originalText;
        checkButton.disabled = false;
    });
}

function displayQuizResults(data) {
    const resultsDiv = document.getElementById('quizResults');
    if (!resultsDiv) return;

    const scorePercentage = Math.round(data.score * 100);
    let alertClass = 'success';
    let icon = 'fas fa-trophy';
    let message = 'Excellent work!';
    
    if (scorePercentage < 50) {
        alertClass = 'danger';
        icon = 'fas fa-times-circle';
        message = 'Keep practicing!';
    } else if (scorePercentage < 70) {
        alertClass = 'warning';
        icon = 'fas fa-exclamation-triangle';
        message = 'Good effort!';
    }
    
    let html = `
        <div class="alert alert-${alertClass} fade-in-up">
            <h5><i class="${icon} me-2"></i>Quiz Results - ${message}</h5>
            <div class="row">
                <div class="col-md-6">
                    <p class="mb-2">
                        <strong>Score:</strong> ${data.correct_count}/${data.total_questions} (${scorePercentage}%)
                    </p>
                    <div class="progress mb-2">
                        <div class="progress-bar bg-${alertClass}" role="progressbar" 
                             style="width: ${scorePercentage}%" 
                             aria-valuenow="${scorePercentage}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                            ${scorePercentage}%
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <p class="mb-0">
                        <i class="fas fa-lightbulb me-2"></i>
                        ${getStudyTip(scorePercentage)}
                    </p>
                </div>
            </div>
        </div>
        
        <div class="results-breakdown fade-in-up">
            <h6><i class="fas fa-list-check me-2"></i>Answer Breakdown:</h6>
            <div class="row">
    `;
    
    data.results.forEach((result, index) => {
        const icon = result.is_correct ? 'fas fa-check-circle text-success' : 'fas fa-times-circle text-danger';
        const status = result.is_correct ? 'Correct' : 'Incorrect';
        
        html += `
            <div class="col-md-6 mb-2">
                <div class="d-flex align-items-center">
                    <i class="${icon} me-2"></i>
                    <span><strong>Question ${index + 1}:</strong> ${status}</span>
                </div>
                ${!result.is_correct ? `
                    <div class="small text-muted ms-4">
                        Correct answer: ${result.correct_option}
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    html += `
            </div>
            <div class="mt-3 text-center">
                <button class="btn btn-primary" onclick="retakeQuiz()">
                    <i class="fas fa-redo me-2"></i>Retake Quiz
                </button>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Scroll to results with smooth animation
    setTimeout(() => {
        resultsDiv.scrollIntoView({ 
            behavior: 'smooth',
            block: 'center'
        });
    }, 100);
}

function highlightAnswers(results) {
    results.forEach((result, index) => {
        const questionBlock = document.querySelector(`.question-block:nth-child(${index + 1})`);
        if (!questionBlock) return;

        const radioButtons = questionBlock.querySelectorAll('input[type="radio"]');
        radioButtons.forEach((radio, optionIndex) => {
            const label = radio.nextElementSibling;
            
            // Reset styles
            label.classList.remove('text-success', 'text-danger', 'fw-bold');
            
            // Highlight correct answer
            if (optionIndex === result.correct_answer) {
                label.classList.add('text-success', 'fw-bold');
                label.innerHTML = `<i class="fas fa-check me-2"></i>${label.textContent}`;
            }
            
            // Highlight incorrect user answer
            if (optionIndex === result.user_answer && !result.is_correct) {
                label.classList.add('text-danger');
                label.innerHTML = `<i class="fas fa-times me-2"></i>${label.textContent}`;
            }
        });
    });
}

function retakeQuiz() {
    // Reset form
    const form = document.getElementById('quizForm');
    if (form) {
        form.reset();
    }
    
    // Hide results
    const resultsDiv = document.getElementById('quizResults');
    if (resultsDiv) {
        resultsDiv.style.display = 'none';
    }
    
    // Reset question highlighting
    const labels = document.querySelectorAll('.question-block label');
    labels.forEach(label => {
        label.classList.remove('text-success', 'text-danger', 'fw-bold');
        label.innerHTML = label.textContent; // Remove icons
    });
    
    // Scroll back to quiz
    const quizForm = document.getElementById('quizForm');
    if (quizForm) {
        quizForm.scrollIntoView({ behavior: 'smooth' });
    }
    
    showAlert('Quiz reset! You can now retake it.', 'info');
}

function getStudyTip(score) {
    if (score >= 90) {
        return "Outstanding! You've mastered this topic. Consider helping others or exploring advanced concepts.";
    } else if (score >= 70) {
        return "Great job! Review the questions you missed and practice similar problems.";
    } else if (score >= 50) {
        return "Good start! Focus on understanding the fundamental concepts before moving forward.";
    } else {
        return "Don't give up! Review the study materials and try breaking down complex topics into smaller parts.";
    }
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertDiv, main.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Download functionality
function downloadStudyPlan() {
    const downloadBtn = document.querySelector('a[href*="download_plan"]');
    if (downloadBtn) {
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Preparing Download...';
        
        setTimeout(() => {
            downloadBtn.innerHTML = '<i class="fas fa-download me-2"></i>Download CSV';
        }, 3000);
    }
}

// Tab switching with URL hash
function initializeTabSwitching() {
    const tabTriggerList = [].slice.call(document.querySelectorAll('#resultTabs button'));
    tabTriggerList.forEach(function (tabTriggerEl) {
        tabTriggerEl.addEventListener('click', function (event) {
            const target = event.target.getAttribute('data-bs-target');
            if (target) {
                window.location.hash = target.substring(1);
            }
        });
    });
    
    // Activate tab based on URL hash
    if (window.location.hash) {
        const targetTab = document.querySelector(`button[data-bs-target="${window.location.hash}"]`);
        if (targetTab) {
            const tab = new bootstrap.Tab(targetTab);
            tab.show();
        }
    }
}

// Initialize tab switching when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTabSwitching);

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }, function(err) {
        console.error('Could not copy text: ', err);
        showAlert('Failed to copy to clipboard', 'danger');
    });
}

function formatTime(hours) {
    const h = Math.floor(hours);
    const m = Math.round((hours - h) * 60);
    return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

// Export functions for global use
window.checkQuizAnswers = checkQuizAnswers;
window.retakeQuiz = retakeQuiz;
window.downloadStudyPlan = downloadStudyPlan;
window.showAlert = showAlert;
window.copyToClipboard = copyToClipboard;