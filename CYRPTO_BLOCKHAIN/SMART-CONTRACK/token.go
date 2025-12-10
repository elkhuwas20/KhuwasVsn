package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"
)

// CryptoChainToken - Simple ERC20-like token
type CryptoChainToken struct {
	Name        string
	Symbol      string
	Decimals    uint8
	TotalSupply float64
	Balances    map[string]float64
	Allowances  map[string]map[string]float64
	Owner       string
}

func NewCryptoChainToken(owner string) *CryptoChainToken {
	token := &CryptoChainToken{
		Name:        "CryptoChain Token",
		Symbol:      "CTC",
		Decimals:    18,
		TotalSupply: 1000000,
		Balances:    make(map[string]float64),
		Allowances:  make(map[string]map[string]float64),
		Owner:       owner,
	}
	
	// Mint initial supply to owner
	token.Balances[owner] = token.TotalSupply
	
	return token
}

func (t *CryptoChainToken) Transfer(from, to string, amount float64) bool {
	if t.Balances[from] < amount {
		return false
	}
	
	t.Balances[from] -= amount
	t.Balances[to] += amount
	
	// Emit transfer event
	fmt.Printf("Transfer: %s -> %s, Amount: %.2f CTC\n", from[:8], to[:8], amount)
	return true
}

func (t *CryptoChainToken) BalanceOf(address string) float64 {
	return t.Balances[address]
}

func (t *CryptoChainToken) Approve(owner, spender string, amount float64) bool {
	if t.Allowances[owner] == nil {
		t.Allowances[owner] = make(map[string]float64)
	}
	
	t.Allowances[owner][spender] = amount
	
	// Emit approval event
	fmt.Printf("Approval: %s approved %s for %.2f CTC\n", 
		owner[:8], spender[:8], amount)
	return true
}

func (t *CryptoChainToken) TransferFrom(from, to, spender string, amount float64) bool {
	if t.Allowances[from][spender] < amount {
		return false
	}
	
	if t.Balances[from] < amount {
		return false
	}
	
	t.Balances[from] -= amount
	t.Balances[to] += amount
	t.Allowances[from][spender] -= amount
	
	return true
}

func (t *CryptoChainToken) Mint(to string, amount float64) {
	t.Balances[to] += amount
	t.TotalSupply += amount
}

func (t *CryptoChainToken) Burn(from string, amount float64) bool {
	if t.Balances[from] < amount {
		return false
	}
	
	t.Balances[from] -= amount
	t.TotalSupply -= amount
	return true
}

// SmartContract - Main contract container
type SmartContract struct {
	Tokens    map[string]*CryptoChainToken
	Address   string
	Timestamp time.Time
}

func NewSmartContract() *SmartContract {
	contractHash := sha256.Sum256([]byte(time.Now().String()))
	contractAddress := hex.EncodeToString(contractHash[:20])
	
	return &SmartContract{
		Tokens:    make(map[string]*CryptoChainToken),
		Address:   contractAddress,
		Timestamp: time.Now(),
	}
}

func (sc *SmartContract) DeployToken(owner, name, symbol string) string {
	token := NewCryptoChainToken(owner)
	token.Name = name
	token.Symbol = symbol
	
	tokenHash := sha256.Sum256([]byte(name + symbol + owner))
	tokenAddress := hex.EncodeToString(tokenHash[:20])
	
	sc.Tokens[tokenAddress] = token
	
	fmt.Printf("Token deployed: %s (%s) at address: %s\n", 
		name, symbol, tokenAddress)
	
	return tokenAddress
}