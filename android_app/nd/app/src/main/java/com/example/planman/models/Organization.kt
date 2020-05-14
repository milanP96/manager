package com.example.planman.models

class Organization(val name: String, val description: String, val hasWallet: Boolean, val participants: Number, val notes: Number ) {
    override fun toString(): String {
        return name
    }
}