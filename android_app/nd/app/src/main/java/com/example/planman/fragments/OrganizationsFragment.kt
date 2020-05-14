package com.example.planman.fragments

import android.app.AlertDialog
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter

import com.example.planman.R
import com.example.planman.adapters.OrganizationAdapter
import com.example.planman.models.Organization
import com.example.planman.services.ManagerService
import kotlinx.android.synthetic.main.fragment_organizations.*

/**
 * A simple [Fragment] subclass.
 */
class OrganizationsFragment : Fragment() {

    lateinit var adapter: OrganizationAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_organizations, container, false)
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        context?.let { ctx ->
            ManagerService.fetchMyOrganizations(ctx) { complete ->
                if (complete) {
                    adapter = context?.let { OrganizationAdapter(it, ManagerService.organizations) }!!
                    organizationsListView.adapter = adapter
                }
            }
        }

        float_btn_create_org.setOnClickListener() {
            val dialogView = LayoutInflater.from(context).inflate(R.layout.create_new_organization, null)

            val dBuilder = AlertDialog.Builder(context).setView(dialogView).setTitle("Create organization")

            val myDialog = dBuilder.show()
        }
    }
}
