package com.example.planman.services

import android.content.Context
import android.util.Log
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.example.planman.R
import com.example.planman.Utils.URL_ORGANIZATIONS
import com.example.planman.models.Organization
import org.json.JSONException
import kotlin.reflect.typeOf

object ManagerService {
    var organizations = listOf<Organization>()

    fun fetchMyOrganizations(context: Context, complete: (Boolean) -> Unit) {
        val tokenPref = TokenPreference(context)
        val token = tokenPref.getToken()
        val loginRequest = object : JsonObjectRequest(Method.GET, URL_ORGANIZATIONS, null, Response.Listener { response ->
            println(response)

            try {
                val orgs = mutableListOf<Organization>()
                val organizations_list = response.getJSONArray("results")
                for (i in 0 until  response.getJSONArray("results").length()) {
                    println(response)
                    val name = if (response.getJSONArray("results").getJSONObject(i).getString("name") != AuthService.usrName) response.getJSONArray("results").getJSONObject(i).getString("name") else context.getString(
                        R.string.personal)
                    println(organizations_list.getJSONObject(i).getString("information") != null)
                    println("OJINOINONOKNMOKMOMNOK")
                    val description : String = organizations_list.getJSONObject(i).getString("information")
                    orgs.add(Organization(name, description, true, organizations_list.getJSONObject(i).getInt("participants"), organizations_list.getJSONObject(i).getInt("notes_count")))
                }
                organizations = orgs
                complete(true)
            } catch (e: JSONException) {
                val tokenPref = TokenPreference(context)
                tokenPref.setToken("")
                Log.d("JSON", "EXC: ${e.localizedMessage}")
                complete(false)
            }
        }, Response.ErrorListener { error ->
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
}