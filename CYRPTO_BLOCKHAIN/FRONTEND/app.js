document.addEventListener('DOMContentLoaded', function() {
    const blockchain = new BlockchainAPI();
    let currentWallet = null;
    
    // DOM Elements
    const walletAddressInput = document.getElementById('walletAddress');
    const balanceDisplay = document.getElementById('balance');
    const blocksContainer = document.getElementById('blocksContainer');
    const transactionsList = document.getElementById('transactionsList');
    const totalBlocksElement = document.getElementById('totalBlocks');
    const totalTransactionsElement = document.getElementById('totalTransactions');
    const activeNodesElement = document.getElementById('activeNodes');
    const blockCountElement = document.getElementById('blockCount');
    
    // Modal elements
    const transactionModal = document.getElementById('transactionModal');
    const blockModal = document.getElementById('blockModal');
    const closeButtons = document.querySelectorAll('.close');
    
    // Initialize
    init();
    
    async function init() {
        // Load existing wallet
        const savedAddress = localStorage.getItem('walletAddress');
        if (savedAddress) {
            currentWallet = savedAddress;
            walletAddressInput.value = savedAddress;
            await updateBalance(savedAddress);
            document.getElementById('senderAddress').value = savedAddress;
        }
        
        // Load blockchain data
        await loadChain();
        await loadTransactions();
        await updateStats();
        
        // Auto-refresh every 10 seconds
        setInterval(async () => {
            await updateStats();
            await updateBalance(currentWallet);
        }, 10000);
    }
    
    async function loadChain() {
        try {
            const chain = await blockchain.fetchChain();
            renderBlocks(chain);
            blockCountElement.textContent = chain.length;
        } catch (error) {
            console.error('Error loading chain:', error);
        }
    }
    
    async function loadTransactions() {
        try {
            const transactions = await blockchain.getTransactions();
            renderTransactions(transactions.slice(-10)); // Show last 10 transactions
        } catch (error) {
            console.error('Error loading transactions:', error);
        }
    }
    
    async function updateStats() {
        try {
            const stats = await blockchain.getStats();
            totalBlocksElement.textContent = stats.totalBlocks;
            totalTransactionsElement.textContent = stats.totalTransactions;
            activeNodesElement.textContent = stats.activeNodes;
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    }
    
    async function updateBalance(address) {
        if (!address) return;
        
        try {
            const balanceData = await blockchain.getBalance(address);
            balanceDisplay.textContent = `${balanceData.balance.toFixed(2)} CTC`;
        } catch (error) {
            console.error('Error updating balance:', error);
        }
    }
    
    function renderBlocks(chain) {
        blocksContainer.innerHTML = '';
        
        chain.forEach(block => {
            const blockElement = document.createElement('div');
            blockElement.className = 'block';
            blockElement.style.borderColor = generateWalletColor(block.hash);
            
            blockElement.innerHTML = `
                <div class="block-header">
                    <div class="block-number">#${block.index}</div>
                    <div class="block-time">${new Date(block.timestamp).toLocaleTimeString()}</div>
                </div>
                <div class="block-hash" title="${block.hash}">
                    ${formatAddress(block.hash)}
                </div>
                <div class="block-transactions">
                    <i class="fas fa-exchange-alt"></i>
                    ${block.transactions.length} transactions
                </div>
                <div class="block-proof">
                    Proof: ${block.proof}
                </div>
            `;
            
            blockElement.addEventListener('click', () => showBlockDetails(block));
            blocksContainer.appendChild(blockElement);
        });
    }
    
    function renderTransactions(transactions) {
        transactionsList.innerHTML = '';
        
        transactions.reverse().forEach(tx => {
            const txElement = document.createElement('div');
            txElement.className = 'transaction-item';
            
            txElement.innerHTML = `
                <div class="transaction-header">
                    <div class="transaction-amount">
                        ${tx.amount.toFixed(2)} CTC
                    </div>
                    <div class="transaction-time">
                        ${formatDate(tx.timestamp)}
                    </div>
                </div>
                <div class="transaction-addresses">
                    <div class="from-address">
                        <i class="fas fa-arrow-up"></i>
                        From: ${formatAddress(tx.sender)}
                    </div>
                    <div class="to-address">
                        <i class="fas fa-arrow-down"></i>
                        To: ${formatAddress(tx.recipient)}
                    </div>
                </div>
            `;
            
            txElement.addEventListener('click', () => showTransactionDetails(tx));
            transactionsList.appendChild(txElement);
        });
    }
    
    // Event Handlers
    window.createWallet = async function() {
        try {
            const newWallet = await blockchain.createWallet();
            if (newWallet) {
                currentWallet = newWallet.address;
                walletAddressInput.value = newWallet.address;
                document.getElementById('senderAddress').value = newWallet.address;
                
                await updateBalance(newWallet.address);
                
                // Show success message
                showNotification('🎉 New wallet created successfully!', 'success');
            }
        } catch (error) {
            console.error('Error creating wallet:', error);
            showNotification('❌ Error creating wallet', 'error');
        }
    };
    
    window.sendTransaction = async function() {
        const sender = document.getElementById('senderAddress').value;
        const recipient = document.getElementById('recipientAddress').value;
        const amount = document.getElementById('amount').value;
        
        if (!sender || !recipient || !amount || parseFloat(amount) <= 0) {
            showNotification('❌ Please fill all fields with valid values', 'error');
            return;
        }
        
        try {
            const result = await blockchain.createTransaction(sender, recipient, amount);
            
            if (result.success) {
                showNotification('✅ Transaction submitted successfully!', 'success');
                document.getElementById('amount').value = '';
                
                // Refresh data
                await Promise.all([
                    loadChain(),
                    loadTransactions(),
                    updateBalance(sender),
                    updateStats()
                ]);
            } else {
                showNotification(`❌ ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Error sending transaction:', error);
            showNotification('❌ Error sending transaction', 'error');
        }
    };
    
    window.mineBlock = async function() {
        if (!currentWallet) {
            showNotification('❌ Please create a wallet first', 'error');
            return;
        }
        
        try {
            showNotification('⛏️ Mining block...', 'info');
            
            const result = await blockchain.mineBlock(currentWallet);
            
            if (result.message) {
                showNotification(`✅ ${result.message}! Reward: 1.0 CTC`, 'success');
                
                // Refresh all data
                await Promise.all([
                    loadChain(),
                    loadTransactions(),
                    updateBalance(currentWallet),
                    updateStats()
                ]);
            }
        } catch (error) {
            console.error('Error mining block:', error);
            showNotification('❌ Error mining block', 'error');
        }
    };
    
    window.copyAddress = function() {
        if (!currentWallet) return;
        
        navigator.clipboard.writeText(currentWallet)
            .then(() => showNotification('📋 Address copied to clipboard!', 'success'))
            .catch(err => console.error('Error copying address:', err));
    };
    
    // Modal functions
    function showBlockDetails(block) {
        const details = document.getElementById('blockDetails');
        details.innerHTML = `
            <div class="block-detail-item">
                <strong>Index:</strong> ${block.index}
            </div>
            <div class="block-detail-item">
                <strong>Timestamp:</strong> ${formatDate(block.timestamp)}
            </div>
            <div class="block-detail-item">
                <strong>Hash:</strong> <code>${block.hash}</code>
            </div>
            <div class="block-detail-item">
                <strong>Previous Hash:</strong> <code>${block.previous_hash}</code>
            </div>
            <div class="block-detail-item">
                <strong>Proof:</strong> ${block.proof}
            </div>
            <div class="block-detail-item">
                <strong>Transactions:</strong> ${block.transactions.length}
            </div>
            <div class="transactions-details">
                ${block.transactions.map(tx => `
                    <div class="transaction-detail">
                        <div>From: ${formatAddress(tx.sender)}</div>
                        <div>To: ${formatAddress(tx.recipient)}</div>
                        <div>Amount: ${tx.amount} CTC</div>
                    </div>
                `).join('')}
            </div>
        `;
        
        blockModal.style.display = 'block';
    }
    
    function showTransactionDetails(transaction) {
        const details = document.getElementById('transactionDetails');
        details.innerHTML = `
            <div class="transaction-detail-item">
                <strong>Sender:</strong> ${transaction.sender}
            </div>
            <div class="transaction-detail-item">
                <strong>Recipient:</strong> ${transaction.recipient}
            </div>
            <div class="transaction-detail-item">
                <strong>Amount:</strong> <span class="amount">${transaction.amount} CTC</span>
            </div>
            <div class="transaction-detail-item">
                <strong>Timestamp:</strong> ${formatDate(transaction.timestamp)}
            </div>
            <div class="transaction-detail-item">
                <strong>Status:</strong> <span class="status confirmed">Confirmed</span>
            </div>
        `;
        
        transactionModal.style.display = 'block';
    }
    
    // Close modals
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            transactionModal.style.display = 'none';
            blockModal.style.display = 'none';
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === transactionModal) {
            transactionModal.style.display = 'none';
        }
        if (event.target === blockModal) {
            blockModal.style.display = 'none';
        }
    });
    
    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notification
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                ${message}
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'success' ? 'rgba(0, 255, 136, 0.2)' : 
                          type === 'error' ? 'rgba(255, 0, 85, 0.2)' : 
                          'rgba(0, 212, 255, 0.2)'};
            border: 1px solid ${type === 'success' ? '#00ff88' : 
                               type === 'error' ? '#ff0055' : 
                               '#00d4ff'};
            border-radius: 10px;
            color: white;
            font-family: 'Orbitron', sans-serif;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            backdrop-filter: blur(10px);
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .transaction-detail-item {
            margin: 10px 0;
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        .transaction-detail-item .amount {
            color: #00ff88;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .transaction-detail-item .status {
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        
        .transaction-detail-item .confirmed {
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
        }
    `;
    document.head.appendChild(style);
});