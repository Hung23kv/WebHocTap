document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const cards = document.querySelectorAll('.card');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Filter cards based on selected tab
            const filterValue = button.textContent.trim();
            
            cards.forEach(card => {
                const cardTag = card.querySelector('.card-tag').textContent.trim();
                
                if (filterValue === 'Tất cả' || filterValue === cardTag) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Navigation arrows
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    const cardGrid = document.querySelector('.card-grid');
    
    prevBtn.addEventListener('click', () => {
        cardGrid.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });
    
    nextBtn.addEventListener('click', () => {
        cardGrid.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });
    
    // Card click event
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Simulate starting a conversation
            alert('Bắt đầu cuộc trò chuyện: ' + card.querySelector('.card-content p').textContent);
        });
    });
    
    // Navigation menu
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all items
            navItems.forEach(navItem => navItem.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
        });
    });
});