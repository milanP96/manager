package com.example.planman.services

import android.content.Context
import android.util.Log
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import com.example.planman.Utils.URL_LOGIN
import com.example.planman.Utils.URL_ME
import com.example.planman.Utils.URL_REGISTER
import org.json.JSONException
import org.json.JSONObject


object AuthService {

    var isAuth = false
    var usrEmail = ""
    var token = ""
    var usrName = ""
    
    fun is_auth(context: Context) : Boolean {
        val tokenPref = TokenPreference(context)
        val token = tokenPref.getToken()
        return token != ""
    }

    fun registerUser(context: Context, email: String, password: String, name: String, complete: (Boolean) -> Unit) {
        val url = URL_REGISTER

        val jsonBody = JSONObject()
        println("$email, $password, $name")
        jsonBody.put("email", email)
        jsonBody.put("password", password)
        jsonBody.put("name", password)
        val requestBody = jsonBody.toString()

        val registerRequest = object : StringRequest(Method.POST, URL_REGISTER, Response.Listener { response ->
            println(response)
            complete(true)
        }, Response.ErrorListener { error ->
            Log.d("ERROR", "Could not register user: $error")
            complete(false)
        }) {
            override fun getBodyContentType(): String {
                return "application/json; charset=utf-8"
            }

            override fun getBody(): ByteArray {
                return requestBody.toByteArray()
            }
        }

        Volley.newRequestQueue(context).add(registerRequest)

    }

    fun loginUser(context: Context, email: String, password: String, complete: (Boolean) -> Unit) {
        val jsonBody = JSONObject()
        jsonBody.put("email", email)
        jsonBody.put("password", password)
        val requestBody = jsonBody.toString()

        val loginRequest = object : JsonObjectRequest(Method.POST, URL_LOGIN, null, Response.Listener {response ->
            try {
                token = response.getString("token")
                isAuth = true
                val tokenPref = TokenPreference(context)
                tokenPref.setToken(token)
                complete(true)
            } catch (e: JSONException) {
                Log.d("JSON", "EXC: ${e.localizedMessage}")
                complete(false)
            }
        }, Response.ErrorListener {error ->
            Log.d("ERROR", "Could not register user: $error")
            complete(false)
        }) {
            override fun getBodyContentType(): String {
                return "application/json; charset=utf-8"
            }
            override fun getBody(): ByteArray {
                return requestBody.toByteArray()
            }
        }

        Volley.newRequestQueue(context).add(loginRequest)
    }

    fun fetchUser(context: Context, complete: (Boolean) -> Unit) {
        val tokenPref = TokenPreference(context)
        val token = tokenPref.getToken()
        val loginRequest = object : JsonObjectRequest(Method.GET, URL_ME, null, Response.Listener {response ->
            complete(true)
            try {
                usrEmail = response.getString("email")
                usrName = response.getString("name")
                complete(true)
            } catch (e: JSONException) {
                val tokenPref = TokenPreference(context)
                tokenPref.setToken("")
                Log.d("JSON", "EXC: ${e.localizedMessage}")
                complete(false)
            }
        }, Response.ErrorListener {error ->
            Log.d("ERROR", "Could not fetch user: $error")
            complete(false)
        }) {
            override fun getBodyContentType(): String {
                return "application/json; charset=utf-8"
            }

            override fun getHeaders(): HashMap<String, String?> {
                val headers = HashMap<String, String?>()
                headers["Authorization"] = "Token $token"
                return headers
            }
        }

        Volley.newRequestQueue(context).add(loginRequest)
    }

    fun LogOut(context: Context,complete: (Boolean) -> Unit) {
        val tokenPref = TokenPreference(context)
        tokenPref.setToken("")
        complete(true)
    }
}