package blockchain

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"time"
)

type Blockchain struct {
	Chain               []Block           `json:"chain"`
	CurrentTransactions []Transaction     `json:"current_transactions"`
	Nodes               map[string]bool   `json:"nodes"`
	WalletBalances      map[string]float64 `json:"wallet_balances"`
}

func NewBlockchain() *Blockchain {
	bc := &Blockchain{
		Chain:               []Block{},
		CurrentTransactions: []Transaction{},
		Nodes:               make(map[string]bool),
		WalletBalances:      make(map[string]float64),
	}
	
	// Create genesis block
	bc.CreateBlock(100, "0")
	
	return bc
}

func (bc *Blockchain) CreateBlock(proof int64, previousHash string) Block {
	var prevHash string
	if previousHash == "" {
		prevHash = bc.GetLastBlock().Hash
	} else {
		prevHash = previousHash
	}

	block := CreateBlock(len(bc.Chain)+1, bc.CurrentTransactions, proof, prevHash)
	
	// Update balances
	for _, tx := range bc.CurrentTransactions {
		if tx.Sender != "0" {
			bc.WalletBalances[tx.Sender] -= tx.Amount
		}
		bc.WalletBalances[tx.Recipient] += tx.Amount
	}
	
	bc.Chain = append(bc.Chain, *block)
	bc.CurrentTransactions = []Transaction{}
	
	return *block
}

func (bc *Blockchain) AddTransaction(sender, recipient string, amount float64) int {
	// Validate sender balance
	if sender != "0" && bc.WalletBalances[sender] < amount {
		return -1
	}
	
	tx := NewTransaction(sender, recipient, amount)
	bc.CurrentTransactions = append(bc.CurrentTransactions, tx)
	
	return bc.GetLastBlock().Index + 1
}

func (bc *Blockchain) GetLastBlock() Block {
	return bc.Chain[len(bc.Chain)-1]
}

func (bc *Blockchain) ProofOfWork(lastProof int64) int64 {
	var proof int64 = 0
	for !bc.ValidProof(lastProof, proof) {
		proof++
	}
	return proof
}

func (bc *Blockchain) ValidProof(lastProof, proof int64) bool {
	guess := string(lastProof) + string(proof)
	h := sha256.New()
	h.Write([]byte(guess))
	guessHash := hex.EncodeToString(h.Sum(nil))
	return guessHash[:4] == "0000"
}

func (bc *Blockchain) MineBlock(minerAddress string) (Block, error) {
	lastBlock := bc.GetLastBlock()
	lastProof := lastBlock.Proof
	proof := bc.ProofOfWork(lastProof)
	
	// Reward miner
	bc.AddTransaction("0", minerAddress, 1.0)
	
	previousHash := lastBlock.Hash
	block := bc.CreateBlock(proof, previousHash)
	
	return block, nil
}

func (bc *Blockchain) GetBalance(address string) float64 {
	return bc.WalletBalances[address]
}