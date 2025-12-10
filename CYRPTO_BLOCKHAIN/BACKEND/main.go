package main

import (
	"crypto-blockchain/blockchain"
	"crypto-blockchain/wallet"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
)

var (
	bc      *blockchain.Blockchain
	wallets = make(map[string]*wallet.Wallet)
	mu      sync.RWMutex
)

func main() {
	// Initialize blockchain
	bc = blockchain.NewBlockchain()
	
	// Create initial wallets
	initWallets()
	
	r := mux.NewRouter()
	
	// API Routes - FIXED ENDPOINTS
	r.HandleFunc("/api/chain", GetChain).Methods("GET")
	r.HandleFunc("/api/transactions/new", NewTransaction).Methods("POST")
	r.HandleFunc("/api/mine", MineBlock).Methods("POST")
	r.HandleFunc("/api/wallet/new", CreateWallet).Methods("GET", "POST") // Allow both GET and POST
	r.HandleFunc("/api/wallet/{address}/balance", GetBalance).Methods("GET")
	r.HandleFunc("/api/transactions", GetTransactions).Methods("GET")
	r.HandleFunc("/api/nodes/register", RegisterNodes).Methods("POST")
	r.HandleFunc("/api/stats", GetStats).Methods("GET")
	
	// Health check
	r.HandleFunc("/api/health", HealthCheck).Methods("GET")
	
	// Serve frontend files
	r.PathPrefix("/").Handler(http.FileServer(http.Dir("../frontend/")))
	
	// CORS configuration
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Content-Type", "Authorization"},
		AllowCredentials: true,
		Debug:            true,
	})
	
	handler := c.Handler(r)
	
	fmt.Println("🚀 CryptoChain Server started successfully!")
	fmt.Println("🌐 URL: http://localhost:8080")
	fmt.Println("📱 API Base URL: http://localhost:8080/api")
	fmt.Println("👛 Initial wallets created with 100 CTC each")
	
	log.Fatal(http.ListenAndServe(":8080", handler))
}

func initWallets() {
	mu.Lock()
	defer mu.Unlock()
	
	// Create 5 initial wallets
	for i := 0; i < 5; i++ {
		w, err := wallet.NewWallet()
		if err != nil {
			log.Printf("Error creating wallet %d: %v", i, err)
			continue
		}
		
		wallets[w.Address] = w
		// Give initial balance
		bc.WalletBalances[w.Address] = 100.0
		
		log.Printf("Created wallet %d: %s (Balance: 100 CTC)", i+1, w.Address)
	}
}

func HealthCheck(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"status":    "healthy",
		"timestamp": time.Now().Format(time.RFC3339),
		"blocks":    len(bc.Chain),
		"wallets":   len(wallets),
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func GetStats(w http.ResponseWriter, r *http.Request) {
	allTransactions := []blockchain.Transaction{}
	for _, block := range bc.Chain {
		allTransactions = append(allTransactions, block.Transactions...)
	}
	
	stats := map[string]interface{}{
		"total_blocks":       len(bc.Chain),
		"total_transactions": len(allTransactions),
		"active_nodes":       len(bc.Nodes),
		"total_wallets":      len(wallets),
		"pending_transactions": len(bc.CurrentTransactions),
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(stats)
}

func CreateWallet(w http.ResponseWriter, r *http.Request) {
	wlt, err := wallet.NewWallet()
	if err != nil {
		http.Error(w, fmt.Sprintf("Failed to create wallet: %v", err), http.StatusInternalServerError)
		return
	}
	
	mu.Lock()
	wallets[wlt.Address] = wlt
	bc.WalletBalances[wlt.Address] = 0.0
	mu.Unlock()
	
	response := map[string]interface{}{
		"success":      true,
		"message":      "New wallet created successfully",
		"address":      wlt.Address,
		"public_key":   wlt.GetPublicKeyHex(),
		"private_key":  wlt.GetPrivateKeyHex(),
		"balance":      0.0,
		"created_at":   time.Now().Format(time.RFC3339),
	}
	
	// Log for debugging
	log.Printf("New wallet created: %s", wlt.Address)
	
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(response)
}

// ... (Keep other functions the same, just update the endpoint paths)
func GetChain(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(bc.Chain)
}

func NewTransaction(w http.ResponseWriter, r *http.Request) {
	var tx struct {
		Sender    string  `json:"sender"`
		Recipient string  `json:"recipient"`
		Amount    float64 `json:"amount"`
	}
	
	if err := json.NewDecoder(r.Body).Decode(&tx); err != nil {
		http.Error(w, "Invalid request body: "+err.Error(), http.StatusBadRequest)
		return
	}
	
	// Validate addresses
	if tx.Sender == "" || tx.Recipient == "" {
		http.Error(w, "Sender and recipient addresses are required", http.StatusBadRequest)
		return
	}
	
	if tx.Amount <= 0 {
		http.Error(w, "Amount must be greater than 0", http.StatusBadRequest)
		return
	}
	
	index := bc.AddTransaction(tx.Sender, tx.Recipient, tx.Amount)
	if index == -1 {
		http.Error(w, "Insufficient balance", http.StatusBadRequest)
		return
	}
	
	response := map[string]interface{}{
		"success": true,
		"message": fmt.Sprintf("Transaction will be added to Block %d", index),
		"transaction": map[string]interface{}{
			"sender":    tx.Sender,
			"recipient": tx.Recipient,
			"amount":    tx.Amount,
			"timestamp": time.Now().Format(time.RFC3339),
		},
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func MineBlock(w http.ResponseWriter, r *http.Request) {
	var req struct {
		MinerAddress string `json:"miner_address"`
	}
	
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}
	
	if req.MinerAddress == "" {
		http.Error(w, "Miner address is required", http.StatusBadRequest)
		return
	}
	
	block, err := bc.MineBlock(req.MinerAddress)
	if err != nil {
		http.Error(w, fmt.Sprintf("Failed to mine block: %v", err), http.StatusInternalServerError)
		return
	}
	
	response := map[string]interface{}{
		"success": true,
		"message": "New Block Forged Successfully",
		"block": map[string]interface{}{
			"index":         block.Index,
			"timestamp":     block.Timestamp,
			"transactions":  block.Transactions,
			"proof":         block.Proof,
			"previous_hash": block.PreviousHash,
			"hash":          block.Hash,
			"miner_reward":  1.0,
		},
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func GetBalance(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	address := vars["address"]
	
	if address == "" {
		http.Error(w, "Address is required", http.StatusBadRequest)
		return
	}
	
	balance := bc.GetBalance(address)
	
	response := map[string]interface{}{
		"success": true,
		"address": address,
		"balance": balance,
		"currency": "CTC",
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func GetTransactions(w http.ResponseWriter, r *http.Request) {
	allTransactions := []blockchain.Transaction{}
	for _, block := range bc.Chain {
		allTransactions = append(allTransactions, block.Transactions...)
	}
	
	// Add pending transactions
	allTransactions = append(allTransactions, bc.CurrentTransactions...)
	
	response := map[string]interface{}{
		"success":       true,
		"count":         len(allTransactions),
		"transactions":  allTransactions,
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func RegisterNodes(w http.ResponseWriter, r *http.Request) {
	var nodes []string
	if err := json.NewDecoder(r.Body).Decode(&nodes); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}
	
	for _, node := range nodes {
		bc.Nodes[node] = true
	}
	
	response := map[string]interface{}{
		"success":     true,
		"message":     "New nodes have been added",
		"total_nodes": len(bc.Nodes),
		"nodes":       nodes,
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}