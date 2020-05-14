package com.example.planman

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import com.example.planman.services.AuthService
import kotlinx.android.synthetic.main.activity_login.*

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        loginbtn.setOnClickListener() {
            AuthService.loginUser(this, loginemail.text.toString(), loginpassword.text.toString()){ complete ->
                if (complete) {
                    AuthService.fetchUser(this) {
                        if (it) {
                            val homeIntent = Intent(this, MainActivity::class.java)
                            startActivity(homeIntent)
                        } else {
                            println("OVDE NIJE USPLEOELE")
                        }
                    }
                } else {
                    Toast.makeText(this, "Wrong email or password", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}
