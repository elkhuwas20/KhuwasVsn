package blockchain

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"time"
)

type Block struct {
	Index        int           `json:"index"`
	Timestamp    string        `json:"timestamp"`
	Transactions []Transaction `json:"transactions"`
	Proof        int64         `json:"proof"`
	PreviousHash string        `json:"previous_hash"`
	Hash         string        `json:"hash"`
}

func (b *Block) CalculateHash() string {
	blockData, _ := json.Marshal(b.Transactions)
	record := string(b.Index) + b.Timestamp + string(blockData) + string(b.Proof) + b.PreviousHash
	h := sha256.New()
	h.Write([]byte(record))
	hashed := h.Sum(nil)
	return hex.EncodeToString(hashed)
}

func CreateBlock(index int, transactions []Transaction, proof int64, previousHash string) *Block {
	block := &Block{
		Index:        index,
		Timestamp:    time.Now().Format(time.RFC3339),
		Transactions: transactions,
		Proof:        proof,
		PreviousHash: previousHash,
	}
	block.Hash = block.CalculateHash()
	return block
}