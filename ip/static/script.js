// script.js - Common JavaScript for all pages

// ==================== BRAND DATABASE ====================
const brandsByCategory = {
    'mobile': ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'Oppo', 'Vivo', 'Realme', 'Nokia', 'Motorola', 'Sony', 'LG', 'Huawei', 'Other'],
    'headset': ['Apple (AirPods)', 'Sony', 'Bose', 'Sennheiser', 'JBL', 'Samsung', 'Boat', 'Noise', 'OnePlus', 'Realme', 'Skullcandy', 'Other'],
    'waterbottle': ['Milton', 'Cello', 'Tupperware', 'Butterfly', 'Nalgene', 'Hydro Flask', 'Contigo', 'CamelBak', 'Other'],
    'idcard': ['College ID', 'Office ID', 'Aadhar Card', 'PAN Card', 'Driving License', 'Voter ID', 'Passport', 'Other'],
    'books': ['Academic', 'Novel', 'Notebook', 'Journal', 'Magazine', 'Other'],
    'laptop': ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft', 'MSI', 'Other'],
    'charger': ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Realme', 'Oppo', 'Vivo', 'Anker', 'Ambrane', 'Other'],
    'wallet': ['Wildcraft', 'Tommy Hilfiger', 'Caprese', 'Da Milano', 'Hidesign', 'Local Brand', 'Other'],
    'keys': ['House Keys', 'Car Keys', 'Bike Keys', 'Locker Keys', 'Other'],
    'bag': ['Skybags', 'American Tourister', 'Wildcraft', 'Nike', 'Adidas', 'Puma', 'Local Brand', 'Other'],
    'jewelry': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Fashion', 'Other'],
    'clothing': ['Shirt', 'Jacket', 'Sweater', 'Cap', 'Scarf', 'Gloves', 'Other'],
    'other': ['Not Applicable']
};

// ==================== COMMON FUNCTIONS ====================
function setupDynamicBrandDropdown(itemTypeId, brandSelectId, brandGroupId) {
    const itemTypeSelect = document.getElementById(itemTypeId);
    const brandSelect = document.getElementById(brandSelectId);
    const brandGroup = document.getElementById(brandGroupId);
    
    if (!itemTypeSelect || !brandSelect || !brandGroup) return;
    
    // Function to update brand dropdown
    function updateBrands() {
        const selectedType = itemTypeSelect.value;
        
        // Clear previous options but keep the first one
        const firstOption = brandSelect.options[0];
        brandSelect.innerHTML = '';
        brandSelect.appendChild(firstOption);
        
        if (selectedType && brandsByCategory[selectedType]) {
            // Add new options
            brandsByCategory[selectedType].forEach(brand => {
                const option = document.createElement('option');
                option.value = brand.toLowerCase().replace(/\s+/g, '-');
                option.textContent = brand;
                brandSelect.appendChild(option);
            });
            
            // Show brand dropdown
            brandGroup.style.display = 'block';
        } else {
            // Hide brand dropdown if not applicable
            brandGroup.style.display = 'none';
        }
    }
    
    // Initial setup
    updateBrands();
    
    // Update on change
    itemTypeSelect.addEventListener('change', updateBrands);
}

function setupPhotoUpload(uploadAreaId, fileInputId, previewContainerId, imagePreviewId, removeBtnId) {
    const uploadArea = document.getElementById(uploadAreaId);
    const fileInput = document.getElementById(fileInputId);
    const previewContainer = document.getElementById(previewContainerId);
    const imagePreview = document.getElementById(imagePreviewId);
    const removeImageBtn = document.getElementById(removeBtnId);
    
    if (!uploadArea || !fileInput) return;
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', function(e) {
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(event) {
                imagePreview.src = event.target.result;
                previewContainer.style.display = 'block';
                uploadArea.style.display = 'none';
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });
    
    if (removeImageBtn) {
        removeImageBtn.addEventListener('click', function() {
            previewContainer.style.display = 'none';
            uploadArea.style.display = 'flex';
            fileInput.value = '';
        });
    }
}

function setupColorSelection(containerClass, hiddenInputId) {
    const colorOptions = document.querySelectorAll(`.${containerClass} .color-option`);
    const selectedColorInput = document.getElementById(hiddenInputId);
    
    if (!colorOptions.length || !selectedColorInput) return;
    
    colorOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options in this container
            colorOptions.forEach(opt => opt.classList.remove('active'));
            // Add active class to clicked option
            this.classList.add('active');
            // Update hidden input
            selectedColorInput.value = this.dataset.color;
        });
    });
}

// ==================== INITIALIZE ON PAGE LOAD ====================
document.addEventListener('DOMContentLoaded', function() {
    
    // ========== LOST PAGE FUNCTIONALITY ==========
    if (document.getElementById('lostItemForm')) {
        // Photo upload for lost page
        setupPhotoUpload('uploadArea', 'itemPhoto', 'previewContainer', 'imagePreview', 'removeImage');
        
        // Dynamic brand dropdown for lost page
        setupDynamicBrandDropdown('itemType', 'brand', 'brandGroup');
        
        // Color selection for lost page
        setupColorSelection('lost-item-form', 'selectedColor');
        
        // Form submission for lost page
        const lostItemForm = document.getElementById('lostItemForm');
        if (lostItemForm) {
            lostItemForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                if (this.checkValidity()) {
                    // For demo - show success message
                    alert('Your lost item has been reported! Our AI will now search for matches. You will be notified if a match is found.');
                    
                    // In actual implementation, this would submit to backend
                    const formData = {
                        itemType: document.getElementById('itemType').value,
                        brand: document.getElementById('brand').value,
                        color: document.getElementById('selectedColor').value,
                        description: document.getElementById('description').value,
                        location: document.getElementById('lostLocation').value,
                        date: document.getElementById('lostDate').value,
                        name: document.getElementById('name').value,
                        email: document.getElementById('email').value
                    };
                    console.log('Lost Item Form Data:', formData);
                    
                    // Reset form after submission
                    this.reset();
                    const previewContainer = document.getElementById('previewContainer');
                    const uploadArea = document.getElementById('uploadArea');
                    if (previewContainer && uploadArea) {
                        previewContainer.style.display = 'none';
                        uploadArea.style.display = 'flex';
                    }
                    
                    // Clear color selection
                    const colorOptions = document.querySelectorAll('#lostItemForm .color-option');
                    colorOptions.forEach(opt => opt.classList.remove('active'));
                }
            });
        }
    }
    
    // ========== FOUND PAGE FUNCTIONALITY ==========
    if (document.getElementById('foundItemForm')) {
        // Photo upload for found page
        setupPhotoUpload('foundUploadArea', 'foundItemPhoto', 'foundPreviewContainer', 'foundImagePreview', 'foundRemoveImage');
        
        // Dynamic brand dropdown for found page
        setupDynamicBrandDropdown('foundItemType', 'foundBrand', 'foundBrandGroup');
        
        // Color selection for found page
        setupColorSelection('found-item-form', 'foundSelectedColor');
        
        // Storage location specific field
        const storageLocation = document.getElementById('storageLocation');
        const specificLocationGroup = document.getElementById('specificLocationGroup');
        
        if (storageLocation && specificLocationGroup) {
            storageLocation.addEventListener('change', function() {
                if (this.value === 'other-location') {
                    specificLocationGroup.style.display = 'block';
                    document.getElementById('specificLocation').required = true;
                } else {
                    specificLocationGroup.style.display = 'none';
                    document.getElementById('specificLocation').required = false;
                }
            });
        }
        
        // Current location button
        const useCurrentLocationBtn = document.getElementById('useCurrentLocation');
        const foundLocationInput = document.getElementById('foundLocation');
        
        if (useCurrentLocationBtn) {
            useCurrentLocationBtn.addEventListener('click', function() {
                if (navigator.geolocation) {
                    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Locating...';
                    this.disabled = true;
                    
                    navigator.geolocation.getCurrentPosition(function(position) {
                        // For demo, show coordinates
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        foundLocationInput.value = `Near coordinates: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;
                        
                        useCurrentLocationBtn.innerHTML = '<i class="fas fa-crosshairs"></i> Use Current Location';
                        useCurrentLocationBtn.disabled = false;
                        
                        // Show success message
                        showNotification('Location detected successfully!', 'success');
                    }, function(error) {
                        useCurrentLocationBtn.innerHTML = '<i class="fas fa-crosshairs"></i> Use Current Location';
                        useCurrentLocationBtn.disabled = false;
                        
                        let message = "Unable to get location. Please enter manually.";
                        if (error.code === error.PERMISSION_DENIED) {
                            message = "Location permission denied. Please enable location services or enter manually.";
                        }
                        showNotification(message, 'error');
                    });
                } else {
                    showNotification("Geolocation is not supported by your browser", 'error');
                }
            });
        }
        
        // Form submission for found page
        const foundItemForm = document.getElementById('foundItemForm');
        if (foundItemForm) {
            foundItemForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Check if photo is uploaded
                const fileInput = document.getElementById('foundItemPhoto');
                if (!fileInput.files[0]) {
                    showNotification('Please upload a photo of the found item', 'error');
                    return;
                }
                
                if (this.checkValidity()) {
                    // Success message
                    showNotification('Thank you! Found item report submitted successfully. Our AI is now searching for the owner.', 'success');
                    
                    // Log data for demo
                    const formData = {
                        itemType: document.getElementById('foundItemType').value,
                        brand: document.getElementById('foundBrand').value,
                        color: document.getElementById('foundSelectedColor').value,
                        description: document.getElementById('foundDescription').value,
                        location: document.getElementById('foundLocation').value,
                        date: document.getElementById('foundDate').value,
                        storage: document.getElementById('storageLocation').value,
                        finderName: document.getElementById('finderName').value,
                        finderEmail: document.getElementById('finderEmail').value
                    };
                    console.log('Found Item Form Data:', formData);
                    
                    // Reset form
                    this.reset();
                    const previewContainer = document.getElementById('foundPreviewContainer');
                    const uploadArea = document.getElementById('foundUploadArea');
                    if (previewContainer && uploadArea) {
                        previewContainer.style.display = 'none';
                        uploadArea.style.display = 'flex';
                    }
                    
                    if (specificLocationGroup) {
                        specificLocationGroup.style.display = 'none';
                    }
                    
                    // Clear color selection
                    const colorOptions = document.querySelectorAll('#foundItemForm .color-option');
                    colorOptions.forEach(opt => opt.classList.remove('active'));
                    
                    // Show success modal
                    setTimeout(() => {
                        alert('✅ Found item successfully reported!\n\nOur AI is now searching for matching lost items. You will be contacted if we find a potential owner.\n\nThank you for your honesty!');
                    }, 500);
                }
            });
        }
    }
    
    // ========== NOTIFICATION FUNCTION ==========
    window.showNotification = function(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    };
});