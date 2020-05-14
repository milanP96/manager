package com.example.planman.services

import android.content.Context

class TokenPreference(context: Context) {

    val PREFERENCE_NAME = "token_preference_main"
    val PREFERENCE_TOKEN = "TokenPreference"
    val preference = context.getSharedPreferences(PREFERENCE_NAME, Context.MODE_PRIVATE)

    fun getToken(): String? {
        return preference.getString(PREFERENCE_TOKEN, "")
    }

    fun setToken(token: String) {
        val editor = preference.edit()
        editor.putString(PREFERENCE_TOKEN, token)
        editor.apply()
    }

}