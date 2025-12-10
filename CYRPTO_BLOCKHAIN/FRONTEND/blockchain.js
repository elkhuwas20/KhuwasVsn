class BlockchainAPI {
    constructor(baseURL = 'http://localhost:8080') {
        this.baseURL = baseURL;
        this.apiBase = `${baseURL}/api`;
        this.walletAddress = localStorage.getItem('walletAddress') || '';
        this.walletPrivateKey = localStorage.getItem('walletPrivateKey') || '';
        
        console.log('BlockchainAPI initialized with base URL:', this.apiBase);
    }

    async fetchChain() {
        try {
            console.log('Fetching chain from:', `${this.apiBase}/chain`);
            const response = await fetch(`${this.apiBase}/chain`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Chain fetched successfully, blocks:', data.length);
            return data;
        } catch (error) {
            console.error('Error fetching chain:', error);
            showNotification('❌ Error connecting to blockchain server', 'error');
            return [];
        }
    }

    async createTransaction(sender, recipient, amount) {
        try {
            console.log('Creating transaction:', { sender, recipient, amount });
            
            const response = await fetch(`${this.apiBase}/transactions/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sender: sender,
                    recipient: recipient,
                    amount: parseFloat(amount)
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Transaction failed');
            }
            
            console.log('Transaction created successfully:', data);
            return data;
        } catch (error) {
            console.error('Error creating transaction:', error);
            return { 
                success: false, 
                message: error.message || 'Failed to create transaction' 
            };
        }
    }

    async mineBlock(minerAddress) {
        try {
            console.log('Mining block for address:', minerAddress);
            
            const response = await fetch(`${this.apiBase}/mine`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    miner_address: minerAddress
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Mining failed');
            }
            
            console.log('Block mined successfully:', data);
            return data;
        } catch (error) {
            console.error('Error mining block:', error);
            return { 
                success: false, 
                message: error.message || 'Failed to mine block' 
            };
        }
    }

    async createWallet() {
        try {
            console.log('Creating new wallet...');
            
            const response = await fetch(`${this.apiBase}/wallet/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const wallet = await response.json();
            console.log('Wallet created successfully:', wallet.address);
            
            if (wallet.success) {
                // Store wallet info
                localStorage.setItem('walletAddress', wallet.address);
                localStorage.setItem('walletPrivateKey', wallet.private_key);
                localStorage.setItem('walletPublicKey', wallet.public_key);
                
                this.walletAddress = wallet.address;
                this.walletPrivateKey = wallet.private_key;
                
                return wallet;
            } else {
                throw new Error(wallet.message || 'Failed to create wallet');
            }
        } catch (error) {
            console.error('Error creating wallet:', error);
            
            // Fallback: Generate wallet locally if server fails
            console.log('Trying fallback wallet creation...');
            return this.createFallbackWallet();
        }
    }

    // Fallback wallet creation (client-side only)
    createFallbackWallet() {
        try {
            // Generate a random address (for demo purposes)
            const chars = '0123456789abcdef';
            let address = '0x';
            for (let i = 0; i < 40; i++) {
                address += chars[Math.floor(Math.random() * chars.length)];
            }
            
            const wallet = {
                success: true,
                address: address,
                public_key: 'fallback_' + address,
                private_key: 'fallback_private_' + address,
                balance: 0,
                message: 'Wallet created (fallback mode)'
            };
            
            // Store wallet info
            localStorage.setItem('walletAddress', wallet.address);
            localStorage.setItem('walletPrivateKey', wallet.private_key);
            localStorage.setItem('walletPublicKey', wallet.public_key);
            
            this.walletAddress = wallet.address;
            this.walletPrivateKey = wallet.private_key;
            
            console.log('Fallback wallet created:', wallet.address);
            return wallet;
        } catch (error) {
            console.error('Error in fallback wallet creation:', error);
            return null;
        }
    }

    async getBalance(address) {
        try {
            console.log('Fetching balance for:', address);
            
            const response = await fetch(`${this.apiBase}/wallet/${address}/balance`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Balance fetched:', data.balance);
            return data;
        } catch (error) {
            console.error('Error fetching balance:', error);
            return { 
                success: false, 
                balance: 0,
                message: error.message 
            };
        }
    }

    async getTransactions() {
        try {
            console.log('Fetching transactions...');
            
            const response = await fetch(`${this.apiBase}/transactions`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Transactions fetched:', data.count);
            return data.transactions || [];
        } catch (error) {
            console.error('Error fetching transactions:', error);
            return [];
        }
    }

    async getStats() {
        try {
            console.log('Fetching stats...');
            
            const response = await fetch(`${this.apiBase}/stats`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Stats fetched:', data);
            return data;
        } catch (error) {
            console.error('Error fetching stats:', error);
            return {
                total_blocks: 0,
                total_transactions: 0,
                active_nodes: 1,
                total_wallets: 0,
                pending_transactions: 0
            };
        }
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            return response.ok;
        } catch (error) {
            console.error('Health check failed:', error);
            return false;
        }
    }
}

// Generate random color for wallet
function generateWalletColor(address) {
    if (!address) return '#8a2be2';
    
    const hash = address.split('').reduce((acc, char) => {
        return char.charCodeAt(0) + ((acc << 5) - acc);
    }, 0);
    
    const colors = [
        '#8a2be2', '#6a0dad', '#9d4edd', '#c77dff',
        '#7b2cbf', '#5a189a', '#240046', '#10002b'
    ];
    
    return colors[Math.abs(hash) % colors.length];
}

// Format address for display
function formatAddress(address) {
    if (!address) return 'No Address';
    if (address.length <= 12) return address;
    return `${address.substring(0, 6)}...${address.substring(address.length - 6)}`;
}

// Format date
function formatDate(timestamp) {
    try {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    } catch (error) {
        return timestamp;
    }
}

// Show notification function (global)
window.showNotification = function(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 
                           type === 'error' ? 'fa-exclamation-circle' : 
                           'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
};

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 25px;
    background: rgba(26, 15, 51, 0.95);
    border-left: 4px solid #8a2be2;
    border-radius: 10px;
    color: white;
    font-family: 'Roboto', sans-serif;
    z-index: 10000;
    animation: slideInRight 0.3s ease;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(138, 43, 226, 0.3);
    display: flex;
    align-items: center;
    gap: 15px;
    min-width: 300px;
    max-width: 400px;
}

.notification.success {
    border-left-color: #9d4edd;
    background: rgba(26, 15, 51, 0.95);
}

.notification.error {
    border-left-color: #ff6b6b;
    background: rgba(26, 15, 51, 0.95);
}

.notification.info {
    border-left-color: #8a2be2;
    background: rgba(26, 15, 51, 0.95);
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 10px;
}

.notification-content i {
    font-size: 1.2rem;
}

.notification.success .notification-content i {
    color: #9d4edd;
}

.notification.error .notification-content i {
    color: #ff6b6b;
}

.notification.info .notification-content i {
    color: #8a2be2;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;
document.head.appendChild(notificationStyles);