import React from "react"
import "../generic/genericEditStyles/editProfile.scss"
import EditFormCoordinator from "./modules/editFormCoordinator"
import FormPassword from "../modules/formPassword"
import Layout from "../../../components/layouts/layout"

function ProfileEditCoordinator(props) {
	return (
		<Layout>
			<div className="edit_container">
				<EditFormCoordinator />
				<FormPassword />
			</div>
		</Layout>
	)
}

export default ProfileEditCoordinator
