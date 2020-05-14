package com.example.planman.adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.TextView
import com.example.planman.R
import com.example.planman.models.Organization

class OrganizationAdapter(context: Context, organizations: List<Organization>): BaseAdapter() {
    val context = context
    val organizations = organizations
    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        val organizationView: View
        organizationView = LayoutInflater.from(context).inflate(R.layout.organization_list_item, null)
        val orgName : TextView = organizationView.findViewById(R.id.org_list_name)
        val orgDesc : TextView = organizationView.findViewById(R.id.organization_description_list_adapter)
        val orgPartCount : TextView = organizationView.findViewById(R.id.participans_count_list_adapter)
        val notesCount : TextView = organizationView.findViewById(R.id.notes_count_list_adapter)
        val walletImg : ImageView = organizationView.findViewById(R.id.red_wallet_icon_list_org)
        val organization = organizations[position]
        orgName.text = organization.name
        orgDesc.text = if (organization.description == "null".toString()) context.getString(R.string.list_org_desc) else organization.description
        orgPartCount.text = organization.participants.toString()
        notesCount.text = organization.notes.toString()
        walletImg.visibility = if (organization.hasWallet) View.VISIBLE else View.INVISIBLE
        return organizationView
    }

    override fun getItem(position: Int): Any {
        return organizations[position]
    }

    override fun getItemId(position: Int): Long {
        return 0
    }

    override fun getCount(): Int {
        return organizations.count()
    }

}