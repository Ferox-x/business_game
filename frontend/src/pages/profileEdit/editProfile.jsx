import React from "react"
import "./generic/genericEditStyles/editProfile.scss"
import EditForm from "./modules/editForm"
import FormPassword from "./modules/formPassword"
import Layout from "../../components/layouts/layout"

function EditProfile(props) {
	return (
		<Layout>
			<div className="edit_container">
				<EditForm />
				<FormPassword />
			</div>
		</Layout>
	)
}

export default EditProfile
