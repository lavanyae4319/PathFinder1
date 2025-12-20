// Resume Analysis Page JavaScript

// Initialize file upload on page load
function initFileUpload() {
    const uploadBox = document.getElementById('uploadBox');
    const resumeFile = document.getElementById('resumeFile');
    const removeFileBtn = document.getElementById('removeFile');
    
    if (!uploadBox || !resumeFile) {
        console.error('Upload elements not found');
        return;
    }
    
    // Click handler for upload box
    uploadBox.style.cursor = 'pointer';
    uploadBox.addEventListener('click', function(e) {
        if (e.target.id !== 'removeFile' && !e.target.closest('#removeFile')) {
            console.log('Opening file dialog...');
            resumeFile.click();
        }
    });
    
    // File selection handler
    resumeFile.addEventListener('change', function(e) {
        console.log('File selected:', this.files.length);
        if (this.files.length > 0) {
            handleFileSelect(this.files[0]);
        }
    });
    
    // Remove file button
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            resumeFile.value = '';
            document.getElementById('selectedFile').style.display = 'none';
            document.querySelectorAll('#uploadBox i, #uploadBox h3, #uploadBox p, #uploadBox .file-info').forEach(el => {
                el.style.display = 'block';
            });
        });
    }
    
    // Drag and drop handlers
    uploadBox.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.style.borderColor = '#4F46E5';
        this.style.background = 'rgba(99, 102, 241, 0.05)';
    });
    
    uploadBox.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = '';
        this.style.background = '';
    });
    
    uploadBox.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.style.borderColor = '';
        this.style.background = '';
        
        if (e.dataTransfer.files.length > 0) {
            resumeFile.files = e.dataTransfer.files;
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });
}

function handleFileSelect(file) {
    console.log('Handling file:', file.name);
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('selectedFile').style.display = 'flex';
    document.querySelectorAll('#uploadBox i, #uploadBox h3, #uploadBox p, #uploadBox .file-info').forEach(el => {
        el.style.display = 'none';
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFileUpload);
} else {
    initFileUpload();
}

// jQuery ready for form submission
$(document).ready(function() {
    // Get file from the file input element
    $('#uploadForm').submit(function(e) {
        e.preventDefault();

        const fileInput = document.getElementById('resumeFile');
        if (!fileInput.files || fileInput.files.length === 0) {
            showNotification('Please select a resume file', 'error');
            return;
        }

        const uploadedFile = fileInput.files[0];
        const formData = new FormData();
        formData.append('resume', uploadedFile);
        formData.append('top_k', $('#topK').val());

        // Show loading state
        $('#uploadSection').hide();
        $('#loadingSection').show();

        // Animate progress steps
        setTimeout(() => $('#parsingStep').addClass('active'), 1000);
        setTimeout(() => $('#matchingStep').addClass('active'), 3000);

        // Submit to API
        $.ajax({
            url: '/api/analyze',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                setTimeout(() => {
                    $('#resultsStep').addClass('active');
                    setTimeout(() => {
                        displayResults(response);
                        $('#loadingSection').hide();
                        $('#resultsSection').show();
                        $('html, body').animate({
                            scrollTop: $('#resultsSection').offset().top - 100
                        }, 800);
                    }, 500);
                }, 1000);
            },
            error: function(xhr) {
                $('#loadingSection').hide();
                $('#uploadSection').show();
                $('.progress-step').removeClass('active');
                
                const error = xhr.responseJSON?.error || 'An error occurred during analysis';
                showNotification(error, 'error');
            }
        });
    });

    // Display Results
    function displayResults(data) {
        // Show AI provider status if available
        if (data.ai_meta && data.ai_meta.provider) {
            const provider = data.ai_meta.provider;
            if (provider !== 'gemini') {
                showNotification('Gemini unavailable: using local analysis', 'error');
            } else {
                const model = data.ai_meta.model || 'gemini';
                showNotification(`Analyzed with ${model}`, 'success');
            }
        }
        // Candidate Profile
        $('#candidateName').text(data.parsed_data.name);
        $('#candidateEmail').text(data.parsed_data.email);
        $('#candidatePhone').text(data.parsed_data.phone);
        $('#candidateLocation').text(data.parsed_data.location);
        $('#candidateExperience').text(data.parsed_data.experience_years + ' years');
        $('#predictedCategory').text(data.predictions?.predicted_category || data.ml_predictions?.predicted_category || 'N/A');
        $('#candidateSummary').text(data.parsed_data.summary);

        // Skills
        const skillsHtml = data.parsed_data.skills.map(skill => 
            `<span class="tag">${skill}</span>`
        ).join('');
        $('#skillsList').html(skillsHtml || '<p>No skills extracted</p>');

        // Education
        let educationHtml = '';
        if (data.parsed_data.education.length > 0) {
            educationHtml = data.parsed_data.education.map(edu => {
                if (typeof edu === 'string') {
                    return `<p>${edu}</p>`;
                }
                return `<p><strong>${edu.degree || edu.title}</strong><br>${edu.institution || ''} ${edu.year || ''}</p>`;
            }).join('');
        } else {
            educationHtml = '<p>No education information available</p>';
        }
        $('#educationList').html(educationHtml);

        // Display AI Analysis if available
        if (data.ai_analysis) {
            displayAIAnalysis(data.ai_analysis);
        }

        // Stats (use ml_predictions if available, fallback to predictions)
        const predictions = data.ml_predictions || data.predictions || {};
        $('#categoryConfidence').text((predictions.confidence || 0) + '%');
        $('#totalMatches').text(predictions.total_matches || 0);
        $('#avgMatchScore').text((predictions.avg_match_score || 0) + '%');

        // Job Matches (ML-based)
        if (data.matching_jobs && data.matching_jobs.length > 0) {
            const jobsHtml = data.matching_jobs.map((job, index) => {
                const matchPercent = job.match_percentage || (job.match_score ? Math.round(job.match_score * 100) : 0);
                const jobTitle = job.Job_Title || job.jobtitle || job.job_title || 'Position';
                const company = job.Company || job.company || 'Company';
                const location = job.Location || job.primary_location || job.location || 'N/A';
                
                // Create search URL for job applications
                const searchQuery = encodeURIComponent(`${jobTitle} ${company} ${location}`);
                const naukriLink = `https://www.naukri.com/jobs?keyword=${encodeURIComponent(jobTitle)}&location=${encodeURIComponent(location)}`;
                const linkedinLink = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(jobTitle)}`;
                const indeedLink = `https://www.indeed.com/jobs?q=${encodeURIComponent(jobTitle)}&l=${encodeURIComponent(location)}`;
                
                return `
                    <div class="job-card">
                        <div class="job-header">
                            <div>
                                <div class="job-title">${jobTitle}</div>
                                <div class="job-company">
                                    <i class="fas fa-building"></i>
                                    ${company}
                                </div>
                            </div>
                            <div class="match-score">${matchPercent}%</div>
                        </div>
                        <div class="job-details">
                            <div class="job-detail">
                                <i class="fas fa-map-marker-alt"></i>
                                ${location}
                            </div>
                            <div class="job-detail">
                                <i class="fas fa-briefcase"></i>
                                ${job.Job_Category || job.job_category || job.Category || 'N/A'}
                            </div>
                            <div class="job-detail">
                                <i class="fas fa-clock"></i>
                                ${job.experience || job.Job_Experience_Required || 'N/A'}
                            </div>
                        </div>
                        ${job.Job_Description ? `<p class="job-description">${job.Job_Description.substring(0, 150)}...</p>` : ''}
                        <div class="job-skills">
                            ${(job.Skills || job.skills || '').toString().split(',').slice(0, 5).map(skill => 
                                `<span class="skill-tag">${skill.trim()}</span>`
                            ).join('')}
                        </div>
                        <div class="job-actions">
                            <a href="${naukriLink}" target="_blank" class="apply-btn naukri-btn" title="Search on Naukri">
                                <i class="fas fa-external-link-alt"></i> Naukri
                            </a>
                            <a href="${linkedinLink}" target="_blank" class="apply-btn linkedin-btn" title="Search on LinkedIn">
                                <i class="fas fa-external-link-alt"></i> LinkedIn
                            </a>
                            <a href="${indeedLink}" target="_blank" class="apply-btn indeed-btn" title="Search on Indeed">
                                <i class="fas fa-external-link-alt"></i> Indeed
                            </a>
                        </div>
                    </div>
                `;
            }).join('');
            $('#jobMatches').html(jobsHtml);
        } else {
            $('#jobMatches').html('<p style="text-align: center; color: var(--text-secondary); padding: 2rem;">No matching jobs found.</p>');
        }

        // Top Companies
        if (data.top_companies) {
            const companiesHtml = Object.entries(data.top_companies)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([company, count]) => `
                    <div class="insight-item">
                        <span>${company}</span>
                        <strong>${count} jobs</strong>
                    </div>
                `).join('');
            $('#topCompanies').html(companiesHtml);
        }

        // Top Locations
        if (data.top_locations) {
            const locationsHtml = Object.entries(data.top_locations)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([location, count]) => `
                    <div class="insight-item">
                        <span>${location}</span>
                        <strong>${count} jobs</strong>
                    </div>
                `).join('');
            $('#topLocations').html(locationsHtml);
        }
    }

    // New Analysis Button
    $('#newAnalysisBtn').click(function() {
        $('#resultsSection').hide();
        $('#uploadSection').show();
        $('#resumeFile').val('');
        $('#selectedFile').hide();
        $('#uploadBox i, #uploadBox h3, #uploadBox p, #uploadBox .file-info').show();
        uploadedFile = null;
        $('.progress-step').removeClass('active');
        $('html, body').animate({ scrollTop: 0 }, 800);
    });

    // Display AI Analysis
    function displayAIAnalysis(analysis) {
        // Overall Score
        if (analysis.overall_score !== undefined) {
            $('#overallScore').text(analysis.overall_score + '/100');
            $('#aiAnalysisCard').show();
        }
        
        // Summary Paragraph
        if (analysis.summary_paragraph) {
            $('#analysisSummary').text(analysis.summary_paragraph);
        }
        
        // Strengths
        if (analysis.strengths && analysis.strengths.length > 0) {
            $('#strengthsList').html(analysis.strengths.map(s => `<li>${s}</li>`).join(''));
            $('#strengthsWeaknesses').show();
        }
        
        // Weaknesses
        if (analysis.weaknesses && analysis.weaknesses.length > 0) {
            $('#weaknessesList').html(analysis.weaknesses.map(w => `<li>${w}</li>`).join(''));
            $('#strengthsWeaknesses').show();
        }
        
        // Suggestions
        if (analysis.suggestions && analysis.suggestions.length > 0) {
            $('#suggestionsList').html(analysis.suggestions.map(s => `<li>${s}</li>`).join(''));
            $('#suggestionsCard').show();
        }
        
        // AI Job Recommendations
        if (analysis.job_recommendations && analysis.job_recommendations.length > 0) {
            const jobsHtml = analysis.job_recommendations.map(job => `
                <div class="ai-job-recommendation">
                    <h4>${job.job_title || 'Position'}</h4>
                    <p class="match-reason">${job.match_reason || ''}</p>
                    <div class="job-details-mini">
                        ${job.salary_range ? `<span><i class="fas fa-dollar-sign"></i> ${job.salary_range}</span>` : ''}
                        ${job.growth_potential ? `<span><i class="fas fa-chart-line"></i> ${job.growth_potential}</span>` : ''}
                    </div>
                    ${job.required_skills && job.required_skills.length > 0 ? 
                        `<div class="required-skills"><strong>Required Skills:</strong> ${job.required_skills.join(', ')}</div>` : ''}
                </div>
            `).join('');
            $('#aiJobRecommendations').html(jobsHtml);
            $('#aiJobsCard').show();
        }
        
        // Skills Gap Analysis
        if (analysis.skills_gap_analysis && analysis.skills_gap_analysis.length > 0) {
            const gapHtml = analysis.skills_gap_analysis.map(gap => `
                <div class="skill-gap-item">
                    <div class="gap-header">
                        <strong>${gap.missing_skill || 'Skill'}</strong>
                        <span class="importance-badge ${gap.importance?.toLowerCase() || 'medium'}">${gap.importance || 'Medium'}</span>
                    </div>
                    <p>${gap.relevance || ''}</p>
                    <p class="how-to-acquire"><i class="fas fa-lightbulb"></i> ${gap.how_to_acquire || ''}</p>
                </div>
            `).join('');
            $('#skillsGapList').html(gapHtml);
            $('#skillsGapCard').show();
        }
        
        // Career Path Suggestions
        if (analysis.career_path_suggestions && analysis.career_path_suggestions.length > 0) {
            const pathHtml = analysis.career_path_suggestions.map(path => `
                <div class="career-path-item">
                    <h4>${path.path || 'Career Path'}</h4>
                    <p>${path.description || ''}</p>
                    ${path.timeline ? `<p class="timeline"><i class="fas fa-clock"></i> ${path.timeline}</p>` : ''}
                    ${path.next_steps && path.next_steps.length > 0 ? 
                        `<ul class="next-steps">${path.next_steps.map(step => `<li>${step}</li>`).join('')}</ul>` : ''}
                </div>
            `).join('');
            $('#careerPathList').html(pathHtml);
            $('#careerPathCard').show();
        }
        
        // ATS Optimization
        if (analysis.ats_optimization && analysis.ats_optimization.length > 0) {
            $('#atsTipsList').html(analysis.ats_optimization.map(tip => `<li>${tip}</li>`).join(''));
            $('#atsCard').show();
        }
        
        // Keywords to Add
        if (analysis.keywords_to_add && analysis.keywords_to_add.length > 0) {
            const keywordsHtml = analysis.keywords_to_add.map(kw => `<span class="tag keyword-tag">${kw}</span>`).join('');
            $('#keywordsList').html(keywordsHtml);
        }
    }

    // Notification System
    function showNotification(message, type = 'info') {
        const notification = $(`
            <div class="notification notification-${type}">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
                <span>${message}</span>
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(() => {
            notification.addClass('show');
        }, 100);
        
        setTimeout(() => {
            notification.removeClass('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // Add notification styles
    $('<style>')
        .text(`
            .notification {
                position: fixed;
                top: 100px;
                right: 20px;
                background: var(--dark-card);
                border: 1px solid var(--border-color);
                border-radius: 0.5rem;
                padding: 1rem 1.5rem;
                display: flex;
                align-items: center;
                gap: 1rem;
                box-shadow: var(--shadow-xl);
                transform: translateX(400px);
                transition: transform 0.3s ease;
                z-index: 10000;
            }
            .notification.show {
                transform: translateX(0);
            }
            .notification-error {
                border-left: 4px solid var(--danger-color);
            }
            .notification-success {
                border-left: 4px solid var(--success-color);
            }
            .notification i {
                font-size: 1.5rem;
            }
            .notification-error i {
                color: var(--danger-color);
            }
            .notification-success i {
                color: var(--success-color);
            }
        `)
        .appendTo('head');
});
