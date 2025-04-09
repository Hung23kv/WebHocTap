document.addEventListener('DOMContentLoaded', function() {
    // Audio buttons
    const audioButtons = document.querySelectorAll('.audio-btn');
    
    audioButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Simulate playing audio
            const messageText = button.parentElement.querySelector('p').textContent;
            console.log('Playing audio:', messageText);
            
            // Visual feedback
            button.classList.add('playing');
            setTimeout(() => {
                button.classList.remove('playing');
            }, 2000);
        });
    });
    
    // Translate button
    const translateBtn = document.querySelector('.translate-btn');
    
    translateBtn.addEventListener('click', () => {
        const messageElement = translateBtn.closest('.message');
        const messageText = messageElement.querySelector('p').textContent;
        
        // Toggle translation
        if (!messageElement.querySelector('.translation')) {
            const translationElement = document.createElement('p');
            translationElement.className = 'translation';
            translationElement.textContent = 'Nghe có vẻ tuyệt! Bạn có muốn thêm đường vào ly latte của bạn không?';
            messageElement.querySelector('.message-content').appendChild(translationElement);
            translateBtn.querySelector('span').textContent = 'Ẩn bản dịch';
        } else {
            messageElement.querySelector('.translation').remove();
            translateBtn.querySelector('span').textContent = 'Dịch';
        }
    });
    
    // Feedback buttons
    const likeBtn = document.querySelector('.like-btn');
    const dislikeBtn = document.querySelector('.dislike-btn');
    
    likeBtn.addEventListener('click', () => {
        likeBtn.style.color = '#4CAF50';
        dislikeBtn.style.color = '#666';
    });
    
    dislikeBtn.addEventListener('click', () => {
        dislikeBtn.style.color = '#F44336';
        likeBtn.style.color = '#666';
    });
    
    // Suggestion panel
    const suggestionBtn = document.querySelector('.suggestion-btn');
    const suggestionPanel = document.getElementById('suggestionPanel');
    const suggestionItems = document.querySelectorAll('.suggestion-item');
    const inputField = document.querySelector('.input-field input');
    
    // Toggle suggestion panel
    suggestionBtn.addEventListener('click', () => {
        suggestionBtn.classList.toggle('active');
        
        if (suggestionPanel.style.display === 'block') {
            suggestionPanel.style.display = 'none';
        } else {
            suggestionPanel.style.display = 'block';
        }
    });
    
    // Handle suggestion item click
    suggestionItems.forEach(item => {
        item.addEventListener('click', () => {
            const suggestionText = item.querySelector('p').textContent;
            inputField.value = suggestionText;
            suggestionPanel.style.display = 'none';
            suggestionBtn.classList.remove('active');
            
            // Auto focus on input field
            inputField.focus();
        });
    });
    
    // Translate suggestion buttons
    const translateSuggestionBtns = document.querySelectorAll('.translate-suggestion-btn');
    
    translateSuggestionBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering the parent click event
            
            const suggestionItem = btn.closest('.suggestion-item');
            const suggestionText = suggestionItem.querySelector('p').textContent;
            
            // Toggle translation
            if (!suggestionItem.querySelector('.suggestion-translation')) {
                const translationElement = document.createElement('p');
                translationElement.className = 'suggestion-translation';
                
                // Set translation based on the suggestion text
                if (suggestionText.includes('please')) {
                    translationElement.textContent = 'Không, cảm ơn. Chỉ cần ly latte thôi, làm ơn.';
                } else {
                    translationElement.textContent = 'Không, cảm ơn. Chỉ cần ly latte thôi.';
                }
                
                suggestionItem.appendChild(translationElement);
                
                // Style the translation
                translationElement.style.fontSize = '13px';
                translationElement.style.color = '#666';
                translationElement.style.marginTop = '5px';
            } else {
                suggestionItem.querySelector('.suggestion-translation').remove();
            }
        });
    });
    
    // Send message
    const sendBtn = document.querySelector('.send-btn');
    
    function sendMessage() {
        const messageText = inputField.value.trim();
        
        if (messageText) {
            // Create new message element
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            
            // Determine if we need to add translation (for the suggestions)
            let translationText = '';
            if (messageText.includes('No, thank you. Just the latte, please.')) {
                translationText = 'Không, cảm ơn. Chỉ cần ly latte thôi, làm ơn.';
            } else if (messageText.includes('No, thank you. Just the latte.')) {
                translationText = 'Không, cảm ơn. Chỉ cần ly latte thôi.';
            }
            
            const translationHtml = translationText ? 
                `<p class="vietnamese">${translationText}</p>` : '';
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    <p class="english">${messageText}</p>
                    ${translationHtml}
                    <button class="edit-btn"><i class="fas fa-pen"></i></button>
                </div>
            `;
            
            // Add to chat
            document.querySelector('.chat-messages').appendChild(messageDiv);
            
            // Hide suggestion panel if visible
            suggestionPanel.style.display = 'none';
            suggestionBtn.classList.remove('active');
            
            // Clear input
            inputField.value = '';
            
            // Simulate bot response after a delay
            setTimeout(() => {
                const botResponse = document.createElement('div');
                botResponse.className = 'message bot-message';
                
                botResponse.innerHTML = `
                    <div class="message-content">
                        <p>Perfect! Your latte will be ready in a moment. Would you like anything else?</p>
                        <button class="audio-btn"><i class="fas fa-volume-up"></i></button>
                    </div>
                    <div class="message-actions">
                        <button class="translate-btn">
                            <i class="fas fa-language"></i>
                            <span>Dịch</span>
                        </button>
                        <div class="feedback-buttons">
                            <button class="like-btn"><i class="fas fa-thumbs-up"></i></button>
                            <button class="dislike-btn"><i class="fas fa-thumbs-down"></i></button>
                        </div>
                    </div>
                `;
                
                document.querySelector('.chat-messages').appendChild(botResponse);
                
                // Update remaining messages counter
                const counter = document.querySelector('.message-counter span');
                const currentCount = parseInt(counter.textContent.match(/\d+/)[0]);
                counter.textContent = `Tin nhắn còn lại: ${currentCount - 1}`;
                
                // Add event listener to new audio button
                const newAudioBtn = botResponse.querySelector('.audio-btn');
                newAudioBtn.addEventListener('click', () => {
                    console.log('Playing audio:', newAudioBtn.parentElement.querySelector('p').textContent);
                    newAudioBtn.classList.add('playing');
                    setTimeout(() => {
                        newAudioBtn.classList.remove('playing');
                    }, 2000);
                });
                
                // Add event listener to new translate button
                const newTranslateBtn = botResponse.querySelector('.translate-btn');
                newTranslateBtn.addEventListener('click', () => {
                    if (!botResponse.querySelector('.translation')) {
                        const translationElement = document.createElement('p');
                        translationElement.className = 'translation';
                        translationElement.textContent = 'Tuyệt! Ly latte của bạn sẽ sẵn sàng trong giây lát. Bạn có muốn gì thêm không?';
                        botResponse.querySelector('.message-content').appendChild(translationElement);
                        newTranslateBtn.querySelector('span').textContent = 'Ẩn bản dịch';
                    } else {
                        botResponse.querySelector('.translation').remove();
                        newTranslateBtn.querySelector('span').textContent = 'Dịch';
                    }
                });
                
                // Add event listeners to new feedback buttons
                const newLikeBtn = botResponse.querySelector('.like-btn');
                const newDislikeBtn = botResponse.querySelector('.dislike-btn');
                
                newLikeBtn.addEventListener('click', () => {
                    newLikeBtn.style.color = '#4CAF50';
                    newDislikeBtn.style.color = '#666';
                });
                
                newDislikeBtn.addEventListener('click', () => {
                    newDislikeBtn.style.color = '#F44336';
                    newLikeBtn.style.color = '#666';
                });
                
                // Scroll to bottom
                const chatMessages = document.querySelector('.chat-messages');
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        }
    }
    
    sendBtn.addEventListener('click', sendMessage);
    
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Show suggestion panel by default for demo purposes
    suggestionPanel.style.display = 'block';
    suggestionBtn.classList.add('active');
});