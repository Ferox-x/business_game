import React from "react"
import "../generic/genericEditStyles/editProfile.scss"
import EditFormCoordinator from "./modules/editFormCoordinator"
import FormPasswordCoordinator from "./modules/formPasswordCoordinator"
import Layout from "../../../components/layouts/layout"

function ProfileEditCoordinator(props) {
	return (
		<Layout>
			<div className="edit_container">
				<EditFormCoordinator />
				<FormPasswordCoordinator />
			</div>
		</Layout>
	)
}

export default ProfileEditCoordinator
