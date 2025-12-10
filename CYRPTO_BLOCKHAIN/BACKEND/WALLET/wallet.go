package wallet

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"math/big"
)

type Wallet struct {
	PrivateKey *ecdsa.PrivateKey
	PublicKey  []byte
	Address    string
}

func NewWallet() (*Wallet, error) {
	// Generate private key
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return nil, fmt.Errorf("failed to generate private key: %v", err)
	}

	// Convert public key to bytes
	publicKey := append(
		privateKey.PublicKey.X.Bytes(),
		privateKey.PublicKey.Y.Bytes()...
	)

	// Generate address
	address := generateAddress(publicKey)

	return &Wallet{
		PrivateKey: privateKey,
		PublicKey:  publicKey,
		Address:    address,
	}, nil
}

func generateAddress(publicKey []byte) string {
	// Double SHA256 hash
	hash1 := sha256.Sum256(publicKey)
	hash2 := sha256.Sum256(hash1[:])
	
	// Take first 20 bytes (like Ethereum)
	addressBytes := hash2[:20]
	
	// Convert to hex string
	return "0x" + hex.EncodeToString(addressBytes)
}

func (w *Wallet) Sign(data []byte) (string, error) {
	if w.PrivateKey == nil {
		return "", fmt.Errorf("private key is nil")
	}
	
	hash := sha256.Sum256(data)
	r, s, err := ecdsa.Sign(rand.Reader, w.PrivateKey, hash[:])
	if err != nil {
		return "", fmt.Errorf("failed to sign data: %v", err)
	}
	
	// Encode signature
	signature := append(r.Bytes(), s.Bytes()...)
	return hex.EncodeToString(signature), nil
}

func (w *Wallet) VerifySignature(data []byte, signature string) (bool, error) {
	sigBytes, err := hex.DecodeString(signature)
	if err != nil {
		return false, fmt.Errorf("failed to decode signature: %v", err)
	}
	
	if len(sigBytes) != 64 {
		return false, fmt.Errorf("invalid signature length")
	}
	
	// Split signature into r and s
	r := new(big.Int).SetBytes(sigBytes[:32])
	s := new(big.Int).SetBytes(sigBytes[32:])
	
	hash := sha256.Sum256(data)
	return ecdsa.Verify(&w.PrivateKey.PublicKey, hash[:], r, s), nil
}

// GetPrivateKeyHex returns private key as hex string
func (w *Wallet) GetPrivateKeyHex() string {
	if w.PrivateKey == nil || w.PrivateKey.D == nil {
		return ""
	}
	return fmt.Sprintf("%x", w.PrivateKey.D.Bytes())
}

// GetPublicKeyHex returns public key as hex string
func (w *Wallet) GetPublicKeyHex() string {
	return hex.EncodeToString(w.PublicKey)
}