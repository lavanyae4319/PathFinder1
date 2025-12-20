// Resume Generator Page JavaScript

$(document).ready(function () {
    console.log('Generator.js loaded successfully');

    let skills = [];
    let certifications = [];
    let experienceCount = 0;
    let educationCount = 0;

    // Character Counter
    $('#summary').on('input', function () {
        const count = $(this).val().length;
        $('#summaryCount').text(count);
        if (count > 500) {
            $(this).val($(this).val().substring(0, 500));
            $('#summaryCount').text(500);
        }
    });

    // Add Skill
    $('#addSkillBtn').click(function () {
        const skillInput = $('#skillInput');
        const skill = skillInput.val().trim();

        if (skill && !skills.includes(skill)) {
            skills.push(skill);
            addSkillTag(skill);
            skillInput.val('');
        }
    });

    $('#skillInput').keypress(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            $('#addSkillBtn').click();
        }
    });

    function addSkillTag(skill) {
        const tag = $(`
            <span class="tag">
                ${skill}
                <span class="remove-tag" data-skill="${skill}">
                    <i class="fas fa-times"></i>
                </span>
            </span>
        `);
        $('#skillsContainer').append(tag);
    }

    // Remove Skill
    $(document).on('click', '.remove-tag', function () {
        const skill = $(this).data('skill');
        skills = skills.filter(s => s !== skill);
        $(this).parent().remove();
    });

    // Add Certification
    $('#addCertBtn').click(function () {
        const certInput = $('#certInput');
        const cert = certInput.val().trim();

        if (cert && !certifications.includes(cert)) {
            certifications.push(cert);
            addCertTag(cert);
            certInput.val('');
        }
    });

    $('#certInput').keypress(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            $('#addCertBtn').click();
        }
    });

    function addCertTag(cert) {
        const tag = $(`
            <span class="tag">
                ${cert}
                <span class="remove-tag" data-cert="${cert}">
                    <i class="fas fa-times"></i>
                </span>
            </span>
        `);
        $('#certificationsContainer').append(tag);
    }

    // Remove Certification
    $(document).on('click', '.remove-tag[data-cert]', function () {
        const cert = $(this).data('cert');
        certifications = certifications.filter(c => c !== cert);
        $(this).parent().remove();
    });

    // Add Experience
    $('#addExperienceBtn').click(function () {
        experienceCount++;
        const expHtml = `
            <div class="experience-item" data-index="${experienceCount}">
                <div class="item-header">
                    <span class="item-number">Experience #${experienceCount}</span>
                    <button type="button" class="remove-item remove-experience" data-index="${experienceCount}">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Job Title *</label>
                        <input type="text" class="exp-title" required placeholder="e.g., Senior Software Engineer">
                    </div>
                    <div class="form-group">
                        <label>Company *</label>
                        <input type="text" class="exp-company" required placeholder="e.g., Google">
                    </div>
                    <div class="form-group full-width">
                        <label>Duration *</label>
                        <input type="text" class="exp-duration" required placeholder="e.g., Jan 2020 - Present">
                    </div>
                </div>
                <div class="responsibilities-list">
                    <label>Responsibilities</label>
                    <div class="responsibility-item">
                        <input type="text" class="exp-resp" placeholder="Describe your key responsibility">
                        <button type="button" class="btn btn-secondary add-resp-btn">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        $('#experienceContainer').append(expHtml);
    });

    // Remove Experience
    $(document).on('click', '.remove-experience', function () {
        const index = $(this).data('index');
        $(`.experience-item[data-index="${index}"]`).remove();
    });

    // Add Responsibility
    $(document).on('click', '.add-resp-btn', function () {
        const respItem = $(`
            <div class="responsibility-item">
                <input type="text" class="exp-resp" placeholder="Describe your key responsibility">
                <button type="button" class="btn-remove remove-resp-btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `);
        $(this).closest('.responsibilities-list').append(respItem);
    });

    // Remove Responsibility
    $(document).on('click', '.remove-resp-btn', function () {
        $(this).closest('.responsibility-item').remove();
    });

    // Add Education
    $('#addEducationBtn').click(function () {
        educationCount++;
        const eduHtml = `
            <div class="education-item" data-index="${educationCount}">
                <div class="item-header">
                    <span class="item-number">Education #${educationCount}</span>
                    <button type="button" class="remove-item remove-education" data-index="${educationCount}">
                        <i class="fas fa-trash"></i> Remove
                    </button>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Degree *</label>
                        <input type="text" class="edu-degree" required placeholder="e.g., Bachelor of Science">
                    </div>
                    <div class="form-group">
                        <label>Field of Study *</label>
                        <input type="text" class="edu-field" required placeholder="e.g., Computer Science">
                    </div>
                    <div class="form-group">
                        <label>Institution *</label>
                        <input type="text" class="edu-institution" required placeholder="e.g., MIT">
                    </div>
                    <div class="form-group">
                        <label>Year</label>
                        <input type="text" class="edu-year" placeholder="e.g., 2020">
                    </div>
                    <div class="form-group">
                        <label>GPA</label>
                        <input type="text" class="edu-gpa" placeholder="e.g., 3.8/4.0">
                    </div>
                </div>
            </div>
        `;
        $('#educationContainer').append(eduHtml);
    });

    // Remove Education
    $(document).on('click', '.remove-education', function () {
        const index = $(this).data('index');
        $(`.education-item[data-index="${index}"]`).remove();
    });

    // Preview Button
    $('#previewBtn').click(function () {
        console.log('Preview button clicked');
        const data = collectFormData();
        console.log('Collected data:', data);
        if (!validateFormData(data)) {
            console.log('Validation failed');
            showNotification('Please fill in all required fields', 'error');
            return;
        }

        console.log('Displaying preview');
        displayPreview(data);
        $('#previewModal').fadeIn();
    });

    // Close Modal
    $('.modal-close').click(function () {
        $('#previewModal').fadeOut();
    });

    $(window).click(function (e) {
        if ($(e.target).is('#previewModal')) {
            $('#previewModal').fadeOut();
        }
    });

    // Generate Button Click
    $('#generateBtn').click(function () {
        console.log('Generate button clicked');

        const data = collectFormData();
        console.log('Form data:', data);
        if (!validateFormData(data)) {
            console.log('Validation failed');
            showNotification('Please fill in all required fields', 'error');
            return;
        }

        // Show loading notification
        showNotification('Generating your resume...', 'info');

        // Submit to API
        $.ajax({
            url: '/api/generate-resume',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob, status, xhr) {
                // Get filename from Content-Disposition header
                const disposition = xhr.getResponseHeader('Content-Disposition');
                let filename = 'resume.docx';
                if (disposition) {
                    const filenameMatch = disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                    if (filenameMatch && filenameMatch[1]) {
                        filename = filenameMatch[1].replace(/['"]/g, '');
                    }
                }

                // Create download link
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                showNotification('Resume generated successfully!', 'success');
            },
            error: function (xhr) {
                console.error('Error generating resume:', xhr);
                const error = 'Failed to generate resume. Please try again.';
                showNotification(error, 'error');
            }
        });
    });

    // Collect Form Data
    function collectFormData() {
        const data = {
            personal_info: {
                name: $('#fullName').val().trim(),
                email: $('#email').val().trim(),
                phone: $('#phone').val().trim(),
                location: $('#location').val().trim(),
                linkedin: $('#linkedin').val().trim()
            },
            summary: $('#summary').val().trim(),
            skills: skills,
            experience: [],
            education: [],
            certifications: certifications,
            format: $('input[name="format"]:checked').val()
        };

        // Collect Experience
        $('.experience-item').each(function () {
            const responsibilities = [];
            $(this).find('.exp-resp').each(function () {
                const resp = $(this).val().trim();
                if (resp) responsibilities.push(resp);
            });

            const exp = {
                title: $(this).find('.exp-title').val().trim(),
                company: $(this).find('.exp-company').val().trim(),
                duration: $(this).find('.exp-duration').val().trim(),
                responsibilities: responsibilities
            };

            if (exp.title && exp.company) {
                data.experience.push(exp);
            }
        });

        // Collect Education
        $('.education-item').each(function () {
            const edu = {
                degree: $(this).find('.edu-degree').val().trim(),
                field: $(this).find('.edu-field').val().trim(),
                institution: $(this).find('.edu-institution').val().trim(),
                year: $(this).find('.edu-year').val().trim(),
                gpa: $(this).find('.edu-gpa').val().trim()
            };

            if (edu.degree && edu.field && edu.institution) {
                data.education.push(edu);
            }
        });

        return data;
    }

    // Validate Form Data
    function validateFormData(data) {
        if (!data.personal_info.name || !data.personal_info.email || !data.personal_info.phone) {
            return false;
        }
        if (!data.summary) {
            return false;
        }
        if (skills.length === 0) {
            return false;
        }
        return true;
    }

    // Display Preview
    function displayPreview(data) {
        let previewHtml = `
            <div class="resume-preview">
                <div class="preview-header">
                    <h2>${data.personal_info.name}</h2>
                    <p>${data.personal_info.email} | ${data.personal_info.phone}</p>
                    ${data.personal_info.location ? `<p>${data.personal_info.location}</p>` : ''}
                </div>
                
                <div class="preview-section">
                    <h3>Professional Summary</h3>
                    <p>${data.summary}</p>
                </div>
                
                <div class="preview-section">
                    <h3>Skills</h3>
                    <p>${data.skills.join(', ')}</p>
                </div>
        `;

        if (data.experience.length > 0) {
            previewHtml += '<div class="preview-section"><h3>Work Experience</h3>';
            data.experience.forEach(exp => {
                previewHtml += `
                    <div class="preview-item">
                        <h4>${exp.title} at ${exp.company}</h4>
                        <p><em>${exp.duration}</em></p>
                        <ul>
                            ${exp.responsibilities.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            previewHtml += '</div>';
        }

        if (data.education.length > 0) {
            previewHtml += '<div class="preview-section"><h3>Education</h3>';
            data.education.forEach(edu => {
                previewHtml += `
                    <div class="preview-item">
                        <h4>${edu.degree} in ${edu.field}</h4>
                        <p>${edu.institution} ${edu.year ? `(${edu.year})` : ''}</p>
                        ${edu.gpa ? `<p>GPA: ${edu.gpa}</p>` : ''}
                    </div>
                `;
            });
            previewHtml += '</div>';
        }

        if (data.certifications.length > 0) {
            previewHtml += `
                <div class="preview-section">
                    <h3>Certifications</h3>
                    <ul>
                        ${data.certifications.map(c => `<li>${c}</li>`).join('')}
                    </ul>
                </div>
            `;
        }

        previewHtml += '</div>';
        $('#previewContent').html(previewHtml);
    }

    // Notification System
    function showNotification(message, type = 'info') {
        const notification = $(`
            <div class="notification notification-${type}">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
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

    // Add preview styles
    $('<style>')
        .text(`
            .resume-preview {
                background: white;
                color: #333;
                padding: 2rem;
                line-height: 1.6;
            }
            .preview-header {
                text-align: center;
                border-bottom: 2px solid #333;
                padding-bottom: 1rem;
                margin-bottom: 2rem;
            }
            .preview-header h2 {
                font-size: 2rem;
                margin-bottom: 0.5rem;
                color: #003366;
            }
            .preview-section {
                margin-bottom: 2rem;
            }
            .preview-section h3 {
                color: #003366;
                border-bottom: 1px solid #ccc;
                padding-bottom: 0.5rem;
                margin-bottom: 1rem;
            }
            .preview-item {
                margin-bottom: 1.5rem;
            }
            .preview-item h4 {
                margin-bottom: 0.25rem;
            }
            .preview-item ul {
                margin-left: 1.5rem;
                margin-top: 0.5rem;
            }
        `)
        .appendTo('head');

    // Initialize with one experience and education
    $('#addExperienceBtn').click();
    $('#addEducationBtn').click();
});
