package blockchain

type Transaction struct {
	Sender    string  `json:"sender"`
	Recipient string  `json:"recipient"`
	Amount    float64 `json:"amount"`
	Timestamp string  `json:"timestamp"`
	Signature string  `json:"signature,omitempty"`
}

type TransactionPool struct {
	Transactions []Transaction `json:"transactions"`
}

func NewTransaction(sender, recipient string, amount float64) Transaction {
	return Transaction{
		Sender:    sender,
		Recipient: recipient,
		Amount:    amount,
		Timestamp: time.Now().Format(time.RFC3339),
	}
}